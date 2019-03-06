import json
from fsdemo.pagedata.base import PageData

# Generate page data
class GalleryUploadPageData(PageData):
    def __init__(self):
        '''
            Initialize page data.
        '''
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Gallery Upload Page'
        self.allTagList = json.loads(json.dumps(['Tag #1', 'Tag #2', 'Tag #3', 'Tag #4']))
        self.objectTags = json.loads(json.dumps(['Tag #2', 'Tag #3']))
        self.objectDesc = '' # 'This is the picture description.'
