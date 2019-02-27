from fsdemo.pagedata.base import PageData
import os, markdown

class AboutPageData(PageData):
    def __init__(self):
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / About Page'
        try:
            with open(os.path.join('fsdemo/pagedata/md', 'about.md'), 'r') as f:
                mdtxt = f.read()
                self.aboutHtml = markdown.markdown(mdtxt, extensions=['extra'])
                f.close()
        except OSError:
            self.aboutHtml = '<h3>Read \'about.md\' error occurred.</h3>'
            pass
        try:
            with open(os.path.join('fsdemo/pagedata/md', 'author.md'), 'r') as f:
                mdtxt = f.read()
                self.authorHtml = markdown.markdown(mdtxt, extensions=['extra'])
                f.close()
        except OSError:
            self.authorHtml = '<h3>Read \'author.md\' error occurred.</h3>'
            pass
           
