from fsdemo.pagedata.base import PageData

class IndexPageData(PageData):
    def __init__(self):
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Index Page'
