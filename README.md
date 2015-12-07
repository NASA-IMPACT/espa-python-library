## PropertyDictionary
Implements a dictionary which allows access to it's elements/attributes/properties using dot notation.

See [test.py](test.py) for example usage.

## Limitations
If you create a key containing dots, like ```{'a.a': 3}``` or ```var['a.a']``` you will not be able to access the property using dot notation.
