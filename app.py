from flask import Flask, render_template
from datetime import date

app = Flask(__name__.split('.')[0])

###############################################################################
#
# PageData classes begin.
#
class PageData:
    def __init__(self):
        self.appTitle = 'Flask Site Demo'
        self.pageTitle = self.appTitle
        startYear = 2011
        thisYear = date.today().year
        if thisYear == startYear:
            self.copyrightYear = '{:d}'.format(startYear)
        else:
            self.copyrightYear = '{:d}-{:d}'.format(startYear, thisYear)

class IndexPageData(PageData):
    def __init__(self):
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Index Page'

class AboutPageData(PageData):
    def __init__(self):
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / About Page'
#
# PageData classes end.
#
###############################################################################

@app.route('/')
def index(pageTitle = None):
    indexData = IndexPageData()
    return render_template('index.html', pageData = indexData)

@app.route('/about')
def about(pageTitle = None):
    aboutData = AboutPageData()
    return render_template('about.html', pageData = aboutData)
