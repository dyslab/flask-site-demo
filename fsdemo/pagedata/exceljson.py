from fsdemo.pagedata.base import PageData
from flask import make_response
from werkzeug.datastructures import Headers
import os, csv

# The field list class for test.
class TestFields:
    # The field list for test.
    __FIELD_LIST__ = ['COL1', 'COL2']

# Generate page data
class ExcelJsonPageData(PageData, TestFields):
    # The base path of input file.
    __BASE_PATH__ = 'fsdemo/test/'

    def __init__(self, filename):
        PageData.__init__(self)
        self.pageTitle = self.pageTitle + ' / Excel & CSV & JSON Text Page'
        self.inputFile = filename.lower()
        if self.inputFile.find('.csv') >= 0:
            # Read from CSV file
            self.contentDataList = self.readCSV2List(self.inputFile)
        elif self.inputFile.find('.xlsx') >= 0:
            # Read from XLSX file
            self.contentDataList = self.readXSLX2List(self.inputFile)
        elif self.inputFile.find('.json') >= 0:
            # Read from JSON file
            self.contentDataList = self.readJSON2List(self.inputFile)
        else:
            pass

    def readCSV2List(self, csvfile):
        returnList = []
        with open(os.path.join(self.__BASE_PATH__, csvfile), newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=TestFields().__FIELD_LIST__)
            for row in reader:
                returnList.append(row)
        return returnList

    def readXSLX2List(self, xslxfile):
        return [{'COL1': 'reading XSLX COL1...', 'COL2': 'reading XSLX COL2...'}]

    def readJSON2List(self, jsonfile):
        return [{'COL1': 'reading JSON COL1...', 'COL2': 'reading JSON COL2...'}]

# Output formatted file
class ExcelJsonOutput(TestFields):
    def autoOutputFile(self, req):
        import datetime
        rowList = []
        try:
            # read form data
            output_format = req.form['outputFormat']
            fieldlist = TestFields().__FIELD_LIST__
            for field in fieldlist:
                colList = req.form.getlist(field)
                index_no = 0
                for col in colList:
                    if index_no < len(rowList):
                        rowList[index_no].append(col)
                    else:
                        rowList.append([col])
                    index_no += 1
            # print(rowList) # console output for debug
        except KeyError:
            output_format = 'csv'
            pass
        output_filename = 'output_test_{0}.{1}'.format(datetime.datetime.utcnow().isoformat().replace('.', '_'), output_format)

        if output_filename.find('.csv') >= 0:
            # Output CSV file
            outputfile = self.outputCSV(output_filename, rowList)
        elif output_filename.find('.xlsx') >= 0:
            # Output XLSX file
            outputfile = self.outputXLSX(output_filename, rowList)
        elif output_filename.find('.json') >= 0:
            # Output JSON file
            outputfile = self.outputJSON(output_filename, rowList)
        else:
            pass
        return outputfile

    def outputCSV(self, filename, rowlist):
        # Generate CSV file content.
        contentBody = ''
        for row in rowlist:
            for colitem in row:
                contentBody += '{0},'.format(colitem)
            contentBody += '\n'
        # Get a response object and set its attributes before return a response object.
        resp = make_response()
        resp.content_type = 'text/csv'
        resp.headers['Content-disposition'] = 'attachment;filename={0}'.format(filename)
        resp.response = contentBody
        return resp

    def outputXLSX(self, filename, rowlist):
        return filename

    def outputJSON(self, filename, rowlist):
        return filename
