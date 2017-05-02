
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
    """Enhances the XMLInterface specifically for an XSD Schema defined XMLs

    Determines the best source for the schema to use for validation of the
    specified Metadata XML.
    First: Environment variables are always used if present, but not all are
           tried.
           They are searched for in this order:
               (XML_SCHEMA, ESPA_SCHEMA, ARD_SCHEMA)
    Second: The URI where the schema should reside on the internet as defined
            by the input XML.
    """

    def __init__(self, xml_filename=None):
        """Object initialization and parsing of the XML document

        Performs determination for the source of the Metadata XML schema
        an utilizes that source during initialization of the parent class.

        Args:
            xml_filename (str): The name of the file to parse.
        """

        # Get the logger to use
        logger = logging.getLogger('espa.processing')
        # Just in-case one was not defined
        logger.addHandler(logging.NullHandler())

        # Create a schema object from the metadata xsd source
        xml_xsd = None
        xsd_path = None
        # Search for an environment variable and use that if valid (first)
        if 'XML_SCHEMA' in os.environ:
            xsd_path = os.getenv('XML_SCHEMA')
        elif 'ESPA_SCHEMA' in os.environ:
            xsd_path = os.getenv('ESPA_SCHEMA')
        elif 'ARD_SCHEMA' in os.environ:
            xsd_path = os.getenv('ARD_SCHEMA')
        elif xml_filename is None:
            raise MetadataError('Must provide an xml_filename if no environment'
                                ' variables are defined (XML_SCHEMA,'
                                ' ESPA_SCHEMA, ARD_SCHEMA) so that an XSD'
                                ' Schema can be loaded')

        if xsd_path is not None:
            # An environment variable from above was specified, so use it
            # to retrieve the schema

            if os.path.isfile(xsd_path):
                with open(xsd_path, 'r') as xsd_fd:
                    xml_xsd = xsd_fd.read()
                logger.info('Using XSD source {0} for validation'
                            .format(xsd_path))

        elif xml_filename is not None:
            # An input file was specified instead of one of the environment
            # variables so use the schemaLocation defined in the file if
            # provided

            # Read the file into a string to be used for parsing
            with open(xml_filename, 'r') as xml_fd:
                xml_text = xml_fd.read()

            # Load the file into an objectify object
            xml_object = objectify.fromstring(xml_text)
            xsd_uri = None

            # Retrieve xsi:schemaLocation from the XML file
            for attribute in xml_object.attrib:
                if attribute.endswith('schemaLocation'):
                    xsd_uri = xml_object.attrib[attribute].split()[1]

            # If not present then fail
            if not xsd_uri:
                raise MetadataError('No schemaLocation defined in provided'
                                    ' XML data')

            # Read the schema
            xsd_fd = urllib2.urlopen(xsd_uri)
            xml_xsd = xsd_fd.read()
            xsd_fd.close()
            logger.info('Using XSD source {0} for validation'.format(xsd_uri))

        # (fail)
        if xml_xsd is None:
            raise MetadataError('Failed to find XML schema for validation')

        super(Metadata, self).__init__(xml_xsd=xml_xsd,
                                       xml_filename=xml_filename)

        if xml_filename is not None:
            super(Metadata, self).parse(xml_filename=xml_filename)
