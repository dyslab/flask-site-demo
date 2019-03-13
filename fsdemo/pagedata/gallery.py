import json
from datetime import datetime
from fsdemo.pagedata.base import PageData
from fsdemo.models import GTags, Gallery
from fsdemo.db import db_session
from fsdemo.basefunc import GetGalleryResponseList, GetYearList


# Database Access Middleware: For model 'GTags'.
class GTagsMiddleware(object):
    def load_all(self):
        db_tags = GTags.query.order_by(GTags.updatetime.desc()).all()
        tags = [record.name for record in db_tags]
        return tags

    def save_all(self, tags):
        # print(tags) # print for TEST
        rflag = True
        try:
            # Remove all old tags.
            old_tags = GTags.query.all()
            for olditem in old_tags:
                db_session.delete(olditem)
            db_session.commit()
            # Insert all new tags.
            new_tags = [GTags(tag) for tag in tags]
            db_session.add_all(new_tags)
            # Commit.
            db_session.commit()
        except Exception:
            db_session.rollback()
            rflag = False
            pass
        return rflag

    # Update the field 'updatetime' of all database records to the current
    # timestamp according to the list item of 'tags'.
    def update_tags(self, tags):
        # print(tags)  # print for TEST
        rflag = True
        try:
            # Remove all old tags.
            for tag in tags:
                gtagitem = GTags.query.filter_by(name=tag).first()
                if gtagitem is not None:
                    # print(gtagitem.name)  # print for TEST
                    gtagitem.updatetime = datetime.now()
                    db_session.commit()
        except Exception:
            db_session.rollback()
            rflag = False
            pass
        return rflag


# Database Access Middleware: For model 'Gallery'.
class GalleryMiddleware(object):
    def save_one(self, link='', tags=None, caption=''):
        rflag = True
        try:
            tags_str = json.dumps(tags, ensure_ascii=False)
            newitem = Gallery(
                link=link,
                tags=tags_str,
                caption=caption
            )
            db_session.add(newitem)
            db_session.commit()
            # Update tags time.
            GTagsMiddleware().update_tags(tags)
        except Exception:
            db_session.rollback()
            rflag = False
            pass
        return rflag

    def load_years(self):
        return_list = []
        try:
            gitem = Gallery.query.order_by(
                Gallery.addtime.asc()
            ).first()
            sdate = gitem.addtime
            gitem = Gallery.query.order_by(
                Gallery.addtime.asc()
            ).first()
            edate = gitem.addtime
            return_list = GetYearList(sdate, edate)
        except Exception:
            pass
        return return_list

    def load_all(self, page=1, off=0, per_page=12):
        return_list = []
        if page > 0 and per_page > 0:
            if (page * per_page + off) < Gallery.query.count():
                nextpage = page + 1
            else:
                nextpage = -1
            try:
                pageitems = Gallery.query.order_by(
                    Gallery.updatetime.desc()
                ).limit(
                    per_page
                ).offset(
                    (page-1)*per_page+off
                ).all()
                return_list = GetGalleryResponseList(pageitems)
            except Exception:
                pass
            print(nextpage)
        return {
            'nextpage': nextpage,
            'offset': off,
            'photolist': return_list
        }


# Generate page data for 'gallery/upload'
class GalleryUploadPageData(PageData):
    def __init__(self):
        '''
            Initialize page data.
        '''
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Gallery Upload Page'
        # eg. self.allTagList = ['Tag name #1', 'Tag name #2', 'Tag name #2']
        self.tagsList = GTagsMiddleware().load_all()
        self.manageTagsLink = '/gallery/save/tags'
        # eg. self.objectTags = ['Tag name #1', 'Tag name #2']
        self.objectTags = []
        # eg. self.objectDesc = 'This is the picture description.'
        self.objectDesc = ''


# Generate page data for 'gallery/list'
class GalleryListPageData(PageData):
    def __init__(self):
        '''
            Initialize page data.
        '''
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Gallery List Page'
        # eg. self.allTagList = ['Tag name #1', 'Tag name #2', 'Tag name #2']
        self.tagsList = GTagsMiddleware().load_all()
        self.yearList = GalleryMiddleware().load_years()
