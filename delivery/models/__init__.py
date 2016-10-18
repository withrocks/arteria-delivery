
import json


class BaseModel(object):

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
