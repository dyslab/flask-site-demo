from datetime import date

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
