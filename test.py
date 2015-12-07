

from PropertyDictionary.collection import PropertyDict


if __name__ == '__main__':
    adict = {'a': 1, 'b': 2, 'c': [3, 4, 5], 'd': [{'a': 1}, {'b': 2}]}

    x = PropertyDict(adict)  # This performs a deep copy
    print('----------------------')
    # Test access to every part of the dictionary
    print(x)
    print(x.a)
    print(x.b)
    print(x.c)
    print(x.c[0])
    print(x.c[1])
    print(x.c[2])
    print(x.d)
    print(x.d[0])
    print(x.d[0].a)
    print(x.d[1])
    print(x.d[1].b)

    print('----------------------')
    # Check a non-existent attribute
    print(x.rock)
    # Now add one on the fly
    x.rock = [1, 2, 3]
    print(x.rock)
    # Now add one on the fly using traditional notation
    x['rock2'] = [1, 2, 3]
    print(x.rock2)

    print('----------------------')
    # Check adding a list of dictionaries on the fly
    x.rocky = [{'a': 4}, {'b': 5}, {'c': 6}]
    print(x.rocky)
    print(x.rocky[0])
    print(x.rocky[0].a)
    print(x.rocky[1])
    print(x.rocky[1].b)
    print(x.rocky[2])
    print(x.rocky[2].c)

    print('----------------------')
    # Test deleting an attribute
    del x.a
    print(x.a)

    print('----------------------')
    # Test dictionaries with dictionaries
    bdict = {'z': {'a': 7}, 'zz': {'b': 8}}
    y = PropertyDict(bdict)  # This performs a deep copy
    print(y.z)
    print(y.z.a)
    print(y.zz)
    print(y.zz.b)

    print('----------------------')
    # Test parsing method
    q = PropertyDict.parse(bdict)  # This performs a deep copy
    print(q)
    print(q.z)
    print(q.zz.b)

    print('----------------------')
    # Test copy
    r = PropertyDict.parse(q)  # This performs a deep copy
    print(r)
    del q.z
    print(q)
    print(r)

    q = PropertyDict(bdict)  # This performs a deep copy
    r = PropertyDict(q)  # This performs a deep copy
    print(q)
    print(r)
    del q.zz.b
    print(q)
    print(r)

    print('----------------------')
    # Test starting with an empty dictionary
    dd = PropertyDict()
    print(dd)
    dd.potato = adict
    dd.couch = bdict
    print(dd)

    print('----------------------')
    # Test args and kwargs
    t = PropertyDict(bdict, adict, peter={'d': 20}, pan=[40, 41, 42])  # This performs a deep copy
    print(t)
    print(t.peter)
    print(t.pan)

    print('----------------------')
    dd = t  # This is a reference assignment so no deep copy
    del t.pan
    print(t)
    print(dd)

    print('----------------------')
    print(t.dotabledict_version)
    # Test a non-supported argument to the class
    t = PropertyDict(bdict, 40)
