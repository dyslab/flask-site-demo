import os
import json
from flask import current_app, make_response, url_for
from datetime import datetime
from sqlalchemy import extract
from fsdemo.pagedata.base import PageData
from fsdemo.models import GTags, Gallery
from fsdemo.db import db_session
from fsdemo.basefunc import GetGalleryResponseList, GetYearListFromDatatimeList


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
            gitems = Gallery.query.order_by(
                Gallery.addtime.asc()
            )
            return_list = GetYearListFromDatatimeList([gitem.addtime for gitem in gitems])
        except Exception:
            pass
        return return_list

    def load_all(self, page=1, off=0, per_page=12):
        return_list = []
        if page > 0 and per_page > 0:
            itemscount = Gallery.query.count()
            if (page * per_page + off) < itemscount:
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
        return {
            'nextpage': nextpage,
            'offset': off,
            'count': itemscount,
            'photolist': return_list
        }

    def load_by_tag(self, page=1, off=0, per_page=12, tag=''):
        return_list = []
        if page > 0 and per_page > 0:
            try:
                tag = tag.strip()
                if tag == '':  # '[]' means no tags.
                    filter_tag = '[]'
                else:
                    filter_tag = '%' + tag + '%'
                pageitems = Gallery.query.order_by(
                    Gallery.updatetime.desc()
                ).filter(
                    Gallery.tags.like(filter_tag)
                ).limit(
                    per_page
                ).offset(
                    (page-1)*per_page+off
                ).all()
                print(pageitems)
                return_list = GetGalleryResponseList(pageitems)
                itemscount = Gallery.query.filter(
                    Gallery.tags.like(filter_tag)
                ).count()
                if (page * per_page + off) < itemscount:
                    nextpage = page + 1
                else:
                    nextpage = -1
            except Exception:
                pass
        return {
            'nextpage': nextpage,
            'offset': off,
            'count': itemscount,
            'photolist': return_list
        }

    def load_by_year(
        self, page=1, off=0, per_page=12, year=datetime.now().year
    ):
        return_list = []
        if page > 0 and per_page > 0:
            try:
                pageitems = Gallery.query.order_by(
                    Gallery.updatetime.desc()
                ).filter(
                    extract('year', Gallery.addtime) == year
                ).limit(
                    per_page
                ).offset(
                    (page-1)*per_page+off
                ).all()
                print(pageitems)
                return_list = GetGalleryResponseList(pageitems)
                itemscount = Gallery.query.filter(
                    extract('year', Gallery.addtime) == year
                ).count()
                if (page * per_page + off) < itemscount:
                    nextpage = page + 1
                else:
                    nextpage = -1
            except Exception:
                pass
        return {
            'nextpage': nextpage,
            'offset': off,
            'count': itemscount,
            'photolist': return_list
        }

    def load_by_id(self, id):
        if id > 0:
            gitem = Gallery.query.filter_by(id=id).first()
            if gitem is not None:
                return {
                    'id': gitem.id,
                    'link': gitem.link,
                    'tags': json.loads(gitem.tags),
                    'caption': gitem.caption
                }
        return None

    def delete_by_id(self, id):
        rflag = False
        if id > 0:
            gitem = Gallery.query.filter_by(id=id).first()
            if gitem is not None:
                fname = self.getFilenameByLink(gitem.link)
                fullpath = self.getPhotoFullPath(fname)
                print(fullpath)
                try:
                    os.remove(fullpath)
                except Exception:
                    pass
                try:
                    db_session.delete(gitem)
                    db_session.commit()
                    # try to delete the upload files.
                    rflag = True
                except Exception:
                    db_session.rollback()
                    pass
        return rflag

    def getFilenameByLink(self, link):
        try:
            fnarray = link.split('/')
            return fnarray[len(fnarray) - 1]
        except Exception:
            pass
        return None

    def getPhotoFullPath(self, fname):
        return os.path.join(
            os.getcwd(), current_app.config['UPLOADED_PHOTOS_DEST'], fname
        )

    def getFileContentByFilename(self, fname):
        content_type = None
        content_body = None
        try:
            fnarray = fname.split('.')
            lowertype = fnarray[len(fnarray) - 1].lower()
            fullpath = self.getPhotoFullPath(fname)
            if lowertype == 'jpg' or lowertype == 'jpeg':
                content_type = 'image/jpeg'
            elif lowertype == 'gif':
                content_type = 'image/gif'
            elif lowertype == 'png':
                content_type = 'image/png'
            elif lowertype == 'svg':
                content_type = 'text/xml'
            if content_type is not None:
                with open(fullpath, mode='rb') as file:
                    content_body = file.read()
        except Exception:
            pass
        return {
            'type': content_type,
            'body': content_body
        }

    def downloadByID(self, id=0):
        resp = 'no data.'
        if id > 0:
            try:
                gitem = self.load_by_id(id)
                filename = self.getFilenameByLink(gitem['link'])
                content = self.getFileContentByFilename(filename)
                # Get a response object and set its attributes
                # before return a response object.
                if content['type'] is not None:
                    resp = make_response()
                    resp.content_type = content['type']
                    resp.headers['Content-disposition'] = \
                        'attachment;filename={0}'.format(filename)
                    resp.data = content['body']
            except Exception:
                pass
        return resp

    def save_by_id(self, id=0, link='', tags=None, caption=''):
        rflag = False
        if id > 0:
            try:
                tags_str = json.dumps(tags, ensure_ascii=False)
                gitem = Gallery.query.filter_by(id=id).first()
                if link != '':
                    gitem.link = link
                gitem.tags = tags_str
                gitem.caption = caption
                gitem.updatetime = datetime.now()
                db_session.commit()
                # Update tags time.
                GTagsMiddleware().update_tags(tags)
                rflag = True
            except Exception:
                db_session.rollback()
                pass
        return rflag


# Generate page data for 'gallery/upload'
class GalleryUploadPageData(PageData):
    def __init__(self):
        '''
            Initialize upload page data.
        '''
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Gallery Upload Page'
        # eg. self.allTagList = ['Tag name #1', 'Tag name #2', 'Tag name #2']
        self.tagsList = GTagsMiddleware().load_all()
        self.manageTagsLink = '/gallery/save/tags'
        self.objectID = 0
        self.objectPhotoLink = url_for('static', filename='imgs/whatisit.svg')
        # eg. self.objectTags = ['Tag name #1', 'Tag name #2']
        self.objectTags = []
        # eg. self.objectDesc = 'This is the picture description.'
        self.objectDesc = ''


# Generate page data for 'gallery/upload'
class GalleryEditPageData(GalleryUploadPageData):
    def __init__(self, id=0):
        '''
            Initialize edit page data.
        '''
        GalleryUploadPageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Gallery Edit Page'
        self.objectID = id
        if id > 0:
            gitem = GalleryMiddleware().load_by_id(id)
            if gitem is not None:
                self.objectPhotoLink = gitem['link']
                self.objectTags = gitem['tags']
                self.objectDesc = gitem['caption']


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
