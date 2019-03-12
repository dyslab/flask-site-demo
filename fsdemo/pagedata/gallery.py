import json
from datetime import datetime
from fsdemo.pagedata.base import PageData
from fsdemo.models import GTags, Gallery
from fsdemo.db import db_session


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


# Generate page data
class GalleryUploadPageData(PageData):
    def __init__(self):
        '''
            Initialize page data.
        '''
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Gallery Upload Page'
        # eg. self.allTagList = ['Tag name #1', 'Tag name #2', 'Tag name #2']
        self.tagsList = GTagsMiddleware().load_all()
        # eg. self.objectTags = ['Tag name #1', 'Tag name #2']
        self.manageTagsLink = '/gallery/save/tags'
        self.objectTags = []
        # eg. self.objectDesc = 'This is the picture description.'
        self.objectDesc = ''
