
"""
License:
    NASA Open Source Agreement 1.3
"""

import os
import sys
import logging
import urllib2


from lxml import objectify as objectify


from espa import XMLError, XMLInterface


class MetadataError(Exception):
    """Error Exception for Metadata"""
    pass


class Metadata(XMLInterface):
    """Enhances the XMLInterface specifically for an ESPA Metadata XML

    Determines the best source for the schema to use for validation of the
    specified ESPA Metadata XML.  First the ESPA_SCHEMA environment variable
    is searched for and used if present.  Second the installation directory
    where the schema should exist if installed on the local system.  And third
    the URI where the schema should reside on the internet.
    """

    def __init__(self, xml_filename=None):
        """Object initialization and parsing of the XML document

        Performes determination for the source of the ESPA Metadata XML schema
        an utilizes that source during initialization of the parent class.

        Args:
            xml_filename (str): The name of the file to parse.
        """

        # Get the logger to use
        logger = logging.getLogger('espa.processing')
        # Just in-case one was not defined
        logger.addHandler(logging.NullHandler())

        xsd_version = '1_3'
        xsd_filename = 'espa_internal_metadata_v{0}.xsd'.format(xsd_version)
        xsd_uri = ('http://espa.cr.usgs.gov/schema/{0}'.format(xsd_filename))

        # Create a schema object from the metadata xsd source
        xml_xsd = None
        # Search for the environment variable and use that if valid (first)
        if 'ESPA_SCHEMA' in os.environ:
            xsd_path = os.getenv('ESPA_SCHEMA')

            if os.path.isfile(xsd_path):
                with open(xsd_path, 'r') as xsd_fd:
                    xml_xsd = xsd_fd.read()
                logger.info('Using XSD source {0} for validation'
                            .format(xsd_path))
            else:
                logger.info('Defaulting to espa-product-formatter'
                            ' installation directory')
                xml_xsd = None
        else:
            logger.warning('Missing environment variable ESPA_SCHEMA'
                           ' defaulting to espa-product-formatter'
                           ' installation directory')
            xml_xsd = None

        # Use the espa-product-formatter installation directory (second)
        if xml_xsd is None:
            xsd_path = ('/usr/local/espa-product-formatter/schema/{0}'
                        .format(xsd_filename))
            if os.path.isfile(xsd_path):
                with open(xsd_path, 'r') as xsd_fd:
                    xml_xsd = xsd_fd.read()
                logger.info('Using XSD source {0} for validation'
                            .format(xsd_path))
            else:
                logger.info('Defaulting to {0}'.format(xsd_uri))
                xml_xsd = None

        # Use the schema_uri (third)
        if xml_xsd is None:
            with urllib2.urlopen(xsd_uri) as xsd_fd:
                xml_xsd = xsd_fd.read()
            logger.info('Using schema source {0} for validation'
                        .format(xsd_uri))

        # (fail)
        if xml_xsd is None:
            raise MetadataError('Failed to find ESPA XML schema for'
                                ' validation')

        super(Metadata, self).__init__(xml_xsd=xml_xsd,
                                       xml_filename=xml_filename)
