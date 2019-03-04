from fsdemo.pagedata.base import PageData

# Generate page data
class GalleryUploadPageData(PageData):
    def __init__(self):
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Gallery Upload Page'
