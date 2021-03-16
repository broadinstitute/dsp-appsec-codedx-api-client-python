from unittest.mock import Mock


class SuccessMock(object):
    status_code = 200


class JSONMock(SuccessMock):
    headers = {
        "Content-Type": 'application/json;charset=utf-8'
    }
    data = {
        "test" : "data"
    }

    def json(self):
        return self.data


class DataMock(SuccessMock):
    def __init__(self, content_type: str, data: str):
        self.headers = {
            "Content-Type": content_type
        }
        self.content = data
