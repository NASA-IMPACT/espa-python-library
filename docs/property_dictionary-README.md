## PropertyDict
Implements a dictionary which allows access to it's elements/attributes/properties using dot notation.

### Usage

```
>>> from espa import PropertyDict
>>> d = PropertyDict({'a': 1, 'b': 'tiger', 'c': [{'d': 3}, {'d': 4}]})
>>> d.a
1
>>> d.b
'tiger'
>>> d.c
[{'d': 3}, {'d': 4}]
>>> d.c[0].d
3
>>> d.c[1].d
4
>>> 
```

See [property_dictionary-test.py](../examples/property_dictionary-test.py) for additional example usage.

### Limitations
If you create a key containing dots, like ```{'a.a': 3}``` or ```var['a.a']``` you will not be able to access the property using dot notation.
