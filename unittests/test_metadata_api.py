#!/usr/bin/env python


import os
import unittest
from cStringIO import StringIO
from lxml import objectify as objectify


from espa import XMLError, XMLInterface
from espa import MetadataError, Metadata


class TestMetadata(unittest.TestCase):
    """Test a few things, and expand on it someday"""

    def setUp(self):

        xml_filename = 'unittests/test.xml'
        self.mm = Metadata(xml_filename=xml_filename)
        self.mm.parse()

    def tearDown(self):
        pass

    def test_find_version(self):
        self.assertEqual(self.mm.xml_object.get('version'), '2.0')

    def test_find_corners(self):
        self.assertEqual(self.mm.xml_object.global_metadata.corner[0]
                         .attrib['location'], 'UL')
        self.assertEqual(self.mm.xml_object.global_metadata.corner[1]
                         .attrib['location'], 'LR')

    def test_find_band_names(self):
        self.assertEqual(self.mm.xml_object.bands.band[0].get('name'),
                         'band1')
        self.assertEqual(self.mm.xml_object.bands.band[1].get('name'),
                         'band2')
        self.assertEqual(self.mm.xml_object.bands.band[2].get('name'),
                         'band3')
        self.assertEqual(self.mm.xml_object.bands.band[3].get('name'),
                         'band4')
        self.assertEqual(self.mm.xml_object.bands.band[4].get('name'),
                         'band5')
        self.assertEqual(self.mm.xml_object.bands.band[5].get('name'),
                         'band6')

    def test_write_success(self):
        # Also tests for successful validation
        self.mm.write(xml_filename='walnuts_pass.xml')
        self.assertTrue(os.path.exists('walnuts_pass.xml') == 1)
        os.unlink('walnuts_pass.xml')

    def test_validation_fail(self):
        myE = objectify.ElementMaker(annotate=False, namespace=None,
                                     nsmap=None)
        self.mm.xml_object.animals = myE.root()
        self.mm.xml_object.animals.tiger = myE.frog('white')
        self.mm.xml_object.animals.frog = myE.frog('green')

        with self.assertRaises(XMLError):
            self.mm.validate()


if __name__ == '__main__':
    unittest.main(verbosity=2)
