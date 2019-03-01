from fsdemo.pagedata.base import PageData
import os, csv

class ExcelJsonPageData(PageData):
    # The base path of input file.
    __BASE_PATH__ = 'fsdemo/test/'

    def __init__(self, filename):
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Excel & CSV & JSON Text Page'
        self.inputFile = filename.lower()
        if self.inputFile.find('.csv') >= 0:
            # Read from CSV file
            self.contentData = self.readCSV2Dict(self.inputFile)
        elif self.inputFile.find('.xlsx') >= 0:
            # Read from XLSX file
            self.contentData = self.readXSLX2Dict(self.inputFile)
        elif self.inputFile.find('.json') >= 0:
            # Read from JSON file
            self.contentData = self.readJSON2Dict(self.inputFile)
        else:
            pass

    def readCSV2Dict(self, csvfile):
        returnStr = ''
        with open(os.path.join(self.__BASE_PATH__, csvfile), newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=['COL1', 'COL2'])
            for row in reader:
                returnStr += '{0}-{1} <br>'.format(row['COL1'], row['COL2'])
        return returnStr

    def readXSLX2Dict(self, xslxfile):
        return 'reading XSLX...'

    def readJSON2Dict(self, jsonfile):
        return 'reading JSON...'
