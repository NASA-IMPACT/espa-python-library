
"""
License:
    NASA Open Source Agreement 1.3
"""

import os
import logging
from cStringIO import StringIO


from lxml import etree as etree
from lxml import objectify as objectify


class XMLError(Exception):
    """Error Exception for XMLInterface"""
    pass


class XMLInterface(object):
    """Wraps parsing, writing, and validation around lxml functionality.

    Implements a class to wrap lxml functionality to provide validation of the
    XML document, as well as provide access to an lxml.objectify object for
    manipulation of the XML document.  Parsing and writing mechanisms are also
    provided.

    Attributes:
        xml_schema (lxml.schema): The schema derived from XSD input, and used
            to create the parser.
        xml_parser (lxml.parser): The parser created from the schema and used
            to parse the XML document, as well as validation.
        xml_object (lxml.objectify): The XML document in lxml.objectify form
            to allow for manipulation.
    """

    def __init__(self, xml_xsd, xml_filename=None):
        """Object initialization and parsing of the XML document

        Creates an lxml schema from the specified XSD and creates a lxml
        parser from the schema to be used during parsing and validation.

        Args:
            xml_xsd (str): The XSD to use for validation.
            xml_filename (str): The name of the file to parse.

        Raises:
            XMLError: An error occurred using the lxml module.
        """

        super(XMLInterface, self).__init__()

        # Get the logger to use
        self.logger = logging.getLogger('espa.processing')
        # Just in-case one was not defined
        self.logger.addHandler(logging.NullHandler())

        # Assign to local variables
        self.xml_filename = xml_filename

        # Initilize the object
        self.xml_object = None

        # Create a schema from the XSD
        try:
            self.xml_schema = etree.XMLSchema(file=StringIO(xml_xsd))
        except etree.LxmlError:
            self.logger.exception('LXML Error')
            raise XMLError('Schema Creation Error - See LXML Error')

        # Create a parser from the schema
        try:
            self.xml_parser = objectify.makeparser(schema=self.xml_schema)
        except etree.LxmlError:
            self.logger.exception('LXML Error')
            raise XMLError('Parser Creation Error - See LXML Error')

    def parse(self, xml_filename=None):
        """Parses the specified file into an lxml objectify object

        Reads the file into memory and uses lxml to parse the file into an
        lxml objectify object.

        Args:
            xml_filename (str): The name of the file to parse.

        Raises:
            XMLError: An error occurred using the lxml module.
        """

        # Figure out the filename to use
        name = self.xml_filename
        if xml_filename is not None:
            name = xml_filename

        # Read the file into a string to be used for parsing
        with open(name, 'r') as xml_fd:
            xml_text = xml_fd.read()

        try:
            # Parse the document, also performs validation
            self.xml_object = objectify.fromstring(xml_text, self.xml_parser)
        except etree.LxmlError:
            self.logger.exception('LXML Error')
            raise XMLError('Parsing Error - See LXML Error')

    def validate(self):
        """Validates the lxml objectify object against the schema

        Performs validation by converting the lxml.objectify object back into
        a string and then parsing it again.

        Raises:
            XMLError: An error occurred using the lxml module.
        """

        try:
            temp_text = etree.tostring(self.xml_object, encoding='utf-8')

            # Simply validate by using the parser initially created
            objectify.fromstring(temp_text, self.xml_parser)
        except etree.LxmlError:
            self.logger.exception('LXML Error')
            raise XMLError('Validation Error - See LXML Error')

    def debug(self):
        """Prints the XML to stdout for debugging purposes
        """

        print(etree.tostring(self.xml_object,
                             encoding='utf-8',
                             pretty_print=True))

    def write(self, xml_filename=None):
        """Writes the XML to a file

        The XML is validated before being written to the file.  A temp file is
        utilized so that the original XML document is not lost should any
        errors occur.

        Args:
            xml_filename: The name of the file to create.  If not provided,
                the original source filename is used.

        Raises:
            XMLError: An error occurred using the lxml module.
        """

        # First validate the lxml objectify object
        self.validate()

        # Figure out the filename to use
        name = self.xml_filename
        if xml_filename is not None:
            name = xml_filename

        try:
            # Create and populate a temporary file
            temp_name = 'temp_ESPA_XML_{0}'.format(name)
            with open(temp_name, 'w') as xml_fd:
                xml_fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
                xml_fd.write(etree.tostring(self.xml_object, encoding='utf-8',
                                            pretty_print=True))

            # Rename/Overwrite the output XML file with the temporary one
            os.rename(temp_name, name)

        except etree.LxmlError:
            self.logger.exception('LXML Error')
            raise XMLError('Write Error - See LXML Error')
