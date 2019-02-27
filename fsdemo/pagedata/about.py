from fsdemo.pagedata.base import PageData

class AboutPageData(PageData):
    def __init__(self):
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / About Page'
