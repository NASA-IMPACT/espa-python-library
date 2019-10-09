
'''
    A very simple implementation which provides access to a dictionaries
    properties using dot notation.
'''


class PropertyDict(dict):
    '''Enhances dict to be accessable using '.' notation.'''

    propertydict_version = '0.1.0'

    def __init__(self, *args, **kwargs):
        super(PropertyDict, self).__init__()
        for arg in args:
            if isinstance(arg, dict):
                for key, value in list(arg.items()):
                    self[key] = self.parse(value)
            else:
                raise TypeError('Unsupported argument {0}'.format(type(arg)))

        if kwargs:
            for key, value in list(kwargs.items()):
                self[key] = self.parse(value)

    @classmethod
    def parse(cls, data):
        '''A simple method to recursivley process through the input data and
           generate a PropertyDict object'''
        if isinstance(data, dict):
            return cls(data)
        elif isinstance(data, list):
            # Allows having lists of dictionaries
            return [cls.parse(item) for item in data]
        else:
            return data

    def __getattr__(self, attr):
        '''Returns attribute values
           Utilize get() instead of __getitem__ so that None is returned
           for attributes which do not exist'''
        return self.get(attr)

    def __setattr__(self, attr, data):
        '''Sets attrbitue values'''
        self.__setitem__(attr, self.parse(data))

    def __delattr__(self, attr):
        '''Deletes attrbitue values'''
        self.__delitem__(attr)
