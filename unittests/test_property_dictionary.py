

import unittest


from espa import PropertyDict


class TestPropertyDict(unittest.TestCase):

    def setUp(self):
        self.dict_a = {'a': 1,
                       'b': 2,
                       'c': [3, 4, 5],
                       'd': [{'a': 1}, {'b': 2}]}
        self.dict_b = {'z': {'a': 7}, 'zz': {'b': 8}}

    def tearDown(self):
        pass

    def test_dict_with_lists(self):
        """Test dictionary with lists of dicts and general access"""

        x = PropertyDict(self.dict_a)  # This performs a deep copy

        self.assertEqual(x.a, 1)
        self.assertEqual(x['a'], 1)
        self.assertEqual(x.b, 2)
        self.assertEqual(x['b'], 2)
        self.assertEqual(x.c[0], 3)
        self.assertEqual(x.c[1], 4)
        self.assertEqual(x.c[2], 5)
        self.assertEqual(x['c'][0], 3)
        self.assertEqual(x['c'][1], 4)
        self.assertEqual(x['c'][2], 5)
        self.assertEqual(x.d[0].a, 1)
        self.assertEqual(x.d[1].b, 2)
        self.assertEqual(x.d[0]['a'], 1)
        self.assertEqual(x.d[1]['b'], 2)
        self.assertEqual(x['d'][0].a, 1)
        self.assertEqual(x['d'][1].b, 2)
        self.assertEqual(x['d'][0]['a'], 1)
        self.assertEqual(x['d'][1]['b'], 2)

        # Check a non-existent attribute
        self.assertIsNone(x.rock)

        # Now add one on the fly
        x.rock = [1, 2, 3]
        self.assertEqual(x.rock[0], 1)
        self.assertEqual(x.rock[1], 2)
        self.assertEqual(x.rock[2], 3)
        self.assertEqual(x['rock'][0], 1)
        self.assertEqual(x['rock'][1], 2)
        self.assertEqual(x['rock'][2], 3)

        # Now add one on the fly using traditional notation
        x['rock2'] = [1, 2, 3]
        self.assertEqual(x.rock2[0], 1)
        self.assertEqual(x.rock2[1], 2)
        self.assertEqual(x.rock2[2], 3)
        self.assertEqual(x['rock2'][0], 1)
        self.assertEqual(x['rock2'][1], 2)
        self.assertEqual(x['rock2'][2], 3)

        # Check adding a list of dictionaries on the fly
        x.rocky = [{'a': 4}, {'b': 5}, {'c': 6}]
        self.assertEqual(x.rocky[0].a, 4)
        self.assertEqual(x.rocky[1].b, 5)
        self.assertEqual(x.rocky[2].c, 6)
        self.assertEqual(x.rocky[0]['a'], 4)
        self.assertEqual(x.rocky[1]['b'], 5)
        self.assertEqual(x.rocky[2]['c'], 6)
        self.assertEqual(x['rocky'][0].a, 4)
        self.assertEqual(x['rocky'][1].b, 5)
        self.assertEqual(x['rocky'][2].c, 6)
        self.assertEqual(x['rocky'][0]['a'], 4)
        self.assertEqual(x['rocky'][1]['b'], 5)
        self.assertEqual(x['rocky'][2]['c'], 6)

        # Test deleting an attribute
        del x.a
        self.assertIsNone(x.a)

    def test_dict_with_dicts(self):
        """Test dictionaries with dictionaries"""

        #self.dict_b = {'z': {'a': 7}, 'zz': {'b': 8}}
        x = PropertyDict(self.dict_b)  # This performs a deep copy

        self.assertEqual(x.z.a, 7)
        self.assertEqual(x.zz.b, 8)
        self.assertEqual(x.z['a'], 7)
        self.assertEqual(x.zz['b'], 8)
        self.assertEqual(x['z'].a, 7)
        self.assertEqual(x['zz'].b, 8)
        self.assertEqual(x['z']['a'], 7)
        self.assertEqual(x['zz']['b'], 8)

    def test_parse(self):
        """Test the parse class method"""

        x = PropertyDict.parse(self.dict_b)  # This performs a deep copy

        self.assertEqual(x.z.a, 7)
        self.assertEqual(x.zz.b, 8)
        self.assertEqual(x.z['a'], 7)
        self.assertEqual(x.zz['b'], 8)
        self.assertEqual(x['z'].a, 7)
        self.assertEqual(x['zz'].b, 8)
        self.assertEqual(x['z']['a'], 7)
        self.assertEqual(x['zz']['b'], 8)

    def test_empty(self):
        """Start with an empty object"""

        x = PropertyDict()

        self.assertIsNone(x.couch)
        self.assertIsNone(x.potato)

        x.couch = self.dict_b
        x.potato = self.dict_a

        self.assertEqual(x.couch.z.a, 7)
        self.assertEqual(x.couch.zz.b, 8)
        self.assertEqual(x.couch.z['a'], 7)
        self.assertEqual(x.couch.zz['b'], 8)
        self.assertEqual(x.couch['z'].a, 7)
        self.assertEqual(x.couch['zz'].b, 8)
        self.assertEqual(x.couch['z']['a'], 7)
        self.assertEqual(x.couch['zz']['b'], 8)
        self.assertEqual(x['couch'].z.a, 7)
        self.assertEqual(x['couch'].zz.b, 8)
        self.assertEqual(x['couch'].z['a'], 7)
        self.assertEqual(x['couch'].zz['b'], 8)
        self.assertEqual(x['couch']['z'].a, 7)
        self.assertEqual(x['couch']['zz'].b, 8)
        self.assertEqual(x['couch']['z']['a'], 7)
        self.assertEqual(x['couch']['zz']['b'], 8)

        self.assertEqual(x.potato.a, 1)
        self.assertEqual(x.potato['a'], 1)
        self.assertEqual(x.potato.b, 2)
        self.assertEqual(x.potato['b'], 2)
        self.assertEqual(x.potato.c[0], 3)
        self.assertEqual(x.potato.c[1], 4)
        self.assertEqual(x.potato.c[2], 5)
        self.assertEqual(x.potato['c'][0], 3)
        self.assertEqual(x.potato['c'][1], 4)
        self.assertEqual(x.potato['c'][2], 5)
        self.assertEqual(x.potato.d[0].a, 1)
        self.assertEqual(x.potato.d[1].b, 2)
        self.assertEqual(x.potato.d[0]['a'], 1)
        self.assertEqual(x.potato.d[1]['b'], 2)
        self.assertEqual(x.potato['d'][0].a, 1)
        self.assertEqual(x.potato['d'][1].b, 2)
        self.assertEqual(x.potato['d'][0]['a'], 1)
        self.assertEqual(x.potato['d'][1]['b'], 2)
        self.assertEqual(x['potato'].a, 1)
        self.assertEqual(x['potato']['a'], 1)
        self.assertEqual(x['potato'].b, 2)
        self.assertEqual(x['potato']['b'], 2)
        self.assertEqual(x['potato'].c[0], 3)
        self.assertEqual(x['potato'].c[1], 4)
        self.assertEqual(x['potato'].c[2], 5)
        self.assertEqual(x['potato']['c'][0], 3)
        self.assertEqual(x['potato']['c'][1], 4)
        self.assertEqual(x['potato']['c'][2], 5)
        self.assertEqual(x['potato'].d[0].a, 1)
        self.assertEqual(x['potato'].d[1].b, 2)
        self.assertEqual(x['potato'].d[0]['a'], 1)
        self.assertEqual(x['potato'].d[1]['b'], 2)
        self.assertEqual(x['potato']['d'][0].a, 1)
        self.assertEqual(x['potato']['d'][1].b, 2)
        self.assertEqual(x['potato']['d'][0]['a'], 1)
        self.assertEqual(x['potato']['d'][1]['b'], 2)

    def test_args_and_kwargs(self):
        """Test using args and kwargs to create"""

        x = PropertyDict(self.dict_b,
                         self.dict_a,
                         peter={'d': 20},
                         pan=[40, 41, 42])

        self.assertEqual(x.z.a, 7)
        self.assertEqual(x.zz.b, 8)
        self.assertEqual(x.z['a'], 7)
        self.assertEqual(x.zz['b'], 8)
        self.assertEqual(x['z'].a, 7)
        self.assertEqual(x['zz'].b, 8)
        self.assertEqual(x['z']['a'], 7)
        self.assertEqual(x['zz']['b'], 8)
        self.assertEqual(x.a, 1)
        self.assertEqual(x['a'], 1)
        self.assertEqual(x.b, 2)
        self.assertEqual(x['b'], 2)
        self.assertEqual(x.c[0], 3)
        self.assertEqual(x.c[1], 4)
        self.assertEqual(x.c[2], 5)
        self.assertEqual(x['c'][0], 3)
        self.assertEqual(x['c'][1], 4)
        self.assertEqual(x['c'][2], 5)
        self.assertEqual(x.d[0].a, 1)
        self.assertEqual(x.d[1].b, 2)
        self.assertEqual(x.d[0]['a'], 1)
        self.assertEqual(x.d[1]['b'], 2)
        self.assertEqual(x['d'][0].a, 1)
        self.assertEqual(x['d'][1].b, 2)
        self.assertEqual(x['d'][0]['a'], 1)
        self.assertEqual(x['d'][1]['b'], 2)
        self.assertEqual(x.peter.d, 20)
        self.assertEqual(x.peter['d'], 20)
        self.assertEqual(x['peter'].d, 20)
        self.assertEqual(x['peter']['d'], 20)
        self.assertEqual(x.pan[0], 40)
        self.assertEqual(x.pan[1], 41)
        self.assertEqual(x.pan[2], 42)
        self.assertEqual(x['pan'][0], 40)
        self.assertEqual(x['pan'][1], 41)
        self.assertEqual(x['pan'][2], 42)


if __name__ == '__main__':
    unittest.main(verbosity=2)
