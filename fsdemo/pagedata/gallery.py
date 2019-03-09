import json
from fsdemo.pagedata.base import PageData
from fsdemo.models import Gallery
from fsdemo.db import db_session


class GalleryMiddleware(object):
    def __init__(self, itemlink='', tags=None, caption=''):
        self.itemlink = itemlink
        self.tags = tags
        self.caption = caption

    def save_to_SQLite3(self):
        tags_str = json.dumps(self.tags, ensure_ascii=False)
        new = Gallery(link=self.itemlink, tags=tags_str, caption=self.caption)
        db_session.add(new)
        db_session.commit()
        return False

    def load_from_SQLite3(self, itemlink):
        return False

    def outputDict(self):
        return {
            'itemlink': self.itemlink,
            'tags': self.tags,
            'caption': self.caption
        }


# Generate page data
class GalleryUploadPageData(PageData):
    def __init__(self):
        '''
            Initialize page data.
        '''
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Gallery Upload Page'
        self.allTagList = json.loads(json.dumps(['Tag#1', 'Tag#2', 'Tag#3']))
        self.objectTags = json.loads(json.dumps(['Tag #2', 'Tag #3']))
        self.objectDesc = ''  # 'This is the picture description.'
