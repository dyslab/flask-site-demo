from fsdemo.pagedata.base import PageData
from fsdemo.pagedata.gallery import GalleryMiddleware
from fsdemo.pagedata.blog import BlogMiddleware


class IndexPageData(PageData):
    def __init__(self):
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Index Page'
        self.galleryList = GalleryMiddleware().load_all()
        self.blogList = BlogMiddleware().load_all()
