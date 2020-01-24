
"""
License:
    NASA Open Source Agreement 1.3
"""

import os
import sys
import logging
from io import StringIO


class ENVIHeader(object):
    """Manipulates ENVI header files

    Allows for updating ENVI header files.
    """

    def __init__(self, envi_header_filename):
        """Object initialization

        Args:
            envi_header_filename (str): The name of the header file.
        """

        super(ENVIHeader, self).__init__()

        self.envi_header = envi_header_filename

    def update_envi_header(self,
                           description='USGS-EROS-ESPA generated',
                           band_names='band 1',
                           data_type=None,
                           no_data_value=None):
        """Updates the ENVI header

        Args:
            description (str): A description for the data.
            band_names (str): The band names in the file as a comma separated
                              list of names.
            data_type (int): Specify the type of the data.
                             1 = 8-bit unsigned integer
                             2 = 16-bit signed integer
                             3 = 32-bit signed integer
                             4 = 32-bit single-precision floating-point
                             5 = 64-bit double-precision floating-point
                             6 = Real-imaginary pair of single-precision
                                 floating-point
                             9 = Real-imaginary pair of double precision
                                 floating-point
                             12 = 16-bit unsigned integer
                             13 = 32-bit unsigned integer
                             14 = 64-bit signed integer
                             15 = 64-bit unsigned integer
            no_data_value (float): Specify a no datra value to apply.
        """

        def find_ending_bracket(fd):
            """Method to find the ending bracket for an ENVI element"""
            while True:
                next_line = fd.readline()
                if not next_line or next_line.strip().endswith('}'):
                    break

        hdr_text = StringIO()
        with open(self.envi_header, 'r') as tmp_fd:
            while True:
                line = tmp_fd.readline()

                if not line:
                    break

                if line.startswith('description'):
                    # This may be on multiple lines so read lines until
                    # we find the closing brace
                    if not line.strip().endswith('}'):
                        find_ending_bracket(tmp_fd)
                    hdr_text.write('description = {{{0}}}\n'
                                   .format(description))

                elif line.startswith('band names'):
                    # This may be on multiple lines so read lines until
                    # we find the closing brace
                    if not line.strip().endswith('}'):
                        find_ending_bracket(tmp_fd)
                    hdr_text.write('band names = {{{0}}}\n'
                                   .format(band_names))

                elif line.startswith('data type'):
                    if data_type is not None:
                        hdr_text.write('data type = {0}\n'
                                       .format(data_type))
                    else:
                        hdr_text.write(line)

                    # If we specified one, this is where to place it
                    if no_data_value is not None:
                        hdr_text.write('data ignore value ='
                                       ' {0}\n'.format(no_data_value))

                elif (line.startswith('data ignore value') and
                      no_data_value is None):
                    # If present in the file, this allows removal of it
                    pass
                else:
                    # Not something we track care about replacing, so keep it
                    hdr_text.write(line)

        # Do the actual replacement of the file
        with open(self.envi_header, 'w') as tmp_fd:
            tmp_fd.write(hdr_text.getvalue())
