import json


class JsonResponse(object):
    def __init__(self, resCode=0, resMsg='', data=''):
        self.resCode = resCode
        self.resMsg = resMsg
        self.data = data

    def outputJsonString(self):
        return json.dumps({
            'resCode': self.resCode,
            'resMsg': self.resMsg,
            'data': self.data
        }, ensure_ascii=False)
