from fsdemo.pagedata.base import PageData
from flask import make_response
from io import StringIO, BytesIO
from pyexcel_xlsx import get_data, save_data
from collections import OrderedDict
import os
import csv
import json


# The field list class for test.
class TestFields(object):
    # The field list & worksheet's name for test.
    __FIELD_LIST__ = ['COL1', 'COL2']
    __WORKSHEET_NAME__ = 'TEST'


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

    def readCSV2List(self, csvfilename):
        with open(
            os.path.join(self.__BASE_PATH__, csvfilename),
            newline=''
        ) as csvfile:
            reader = csv.DictReader(
                csvfile,
                fieldnames=TestFields().__FIELD_LIST__
            )
            returnList = [row for row in reader]
        return returnList

    def readXSLX2List(self, xslxfilename):
        # We read XLSX file by module 'pyexcel_xlsx' in this app.
        # There're still another choices such as openpyxl, pandas...
        xlsx_data = get_data(os.path.join(self.__BASE_PATH__, xslxfilename))
        json_list = json.loads(json.dumps(xlsx_data, ensure_ascii=False))
        test_fields = TestFields().__FIELD_LIST__
        returnList = []
        # Convert to dict list for test.
        for json_item in json_list[TestFields().__WORKSHEET_NAME__]:
            temp_row = {}
            for fno in range(0, len(test_fields)):
                if fno < len(json_item):
                    temp_row.update({test_fields[fno]: json_item[fno]})
                else:
                    temp_row.update({test_fields[fno]: 'N/A'})
            returnList.append(temp_row)
        return returnList

    def readJSON2List(self, jsonfilename):
        returnList = []
        with open(
            os.path.join(self.__BASE_PATH__, jsonfilename),
            newline=''
        ) as jsonfile:
            returnList = json.load(jsonfile)
        # print(returnList) # console open for test
        return returnList


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
        output_filename = 'output_test_{0}.{1}'.format(
            datetime.datetime.utcnow().isoformat().replace('.', '_'),
            output_format
        )

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
        '''
        # Method 1: Manually construct string content.
        for row in rowlist:
            for colitem in row:
                contentBody += '"{0}",'.format(colitem.replace('"','""'))
            contentBody += '\n'
        '''
        # Method 2: Use module csv with its method csv.writer(f).writerow().
        tempstream = StringIO()
        for row in rowlist:
            csv.writer(tempstream).writerow(row)
        contentBody = tempstream.getvalue()

        # Get a response object and set its attributes
        # before return a response object.
        resp = make_response()
        resp.content_type = 'text/csv'
        resp.headers['Content-disposition'] = \
            'attachment;filename={0}'.format(filename)
        resp.data = contentBody
        return resp

    def outputXLSX(self, filename, rowlist):
        content_data = OrderedDict()
        content_data.update({TestFields().__WORKSHEET_NAME__: rowlist})
        data_io = BytesIO()
        save_data(data_io, content_data)

        # Get a response object and set its attributes
        # before return a response object.
        resp = make_response()
        resp.content_type = \
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        resp.headers['Content-disposition'] = \
            'attachment;filename={0}'.format(filename)
        resp.data = data_io.getvalue()
        return resp

    def outputJSON(self, filename, rowlist):
        # Convert rowlist to dictlist.
        dictlist = []
        for row in rowlist:
            indexno = 1
            ditem = {}
            for col in row:
                ditem['COL' + str(indexno)] = col
                indexno += 1
            dictlist.append(ditem)
        contentBody = json.JSONEncoder(
            ensure_ascii=False,
            indent=4
        ).encode(dictlist)

        # Get a response object and set its attributes
        # before return a response object.
        resp = make_response()
        resp.content_type = 'application/json'
        resp.headers['Content-disposition'] = \
            'attachment;filename={0}'.format(filename)
        resp.data = contentBody
        return resp
