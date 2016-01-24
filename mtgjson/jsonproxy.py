class JSONProxy(object):
    def __init__(self, data):
        self.__data = data

    def  __iter__(self):
        return self.__data.__iter__()

    def __getitem__(self, key):
        try:
            return self.__data[key]
        except KeyError as e:
            raise AttributeError(e)

    def __contains__(self, item):
        return self.__data.__contains__(item)

    def __getattr__(self, key):
        try:
            return self.__data[key]
        except KeyError as e:
            raise AttributeError(e)

    def _get_raw_data(self):
        return self.__data

