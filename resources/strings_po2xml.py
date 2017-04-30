'''
Filename : strings_po2xml.py
Purpose  : Convert strings.po to strings.xml (XBMC4Xbox)
Author   : Dan Dar3 <dan.dar33@gmail.com>
Date     : 20 Jan 2014
'''

# Imports
import sys, os, re
from xml.sax.saxutils import escape
import codecs

#
# Convert...
#
def convert(path):
    # Check input file exists...
    if os.path.isfile(path):
        strings_po = path
        path       = os.path.dirname(path)
    else :
        strings_po = os.path.join(path, 'strings.po')
    if not os.path.exists(strings_po):
        print 'File not found "%s"' % strings_po
        return False

    # Read input (strings.po)...
    f = codecs.open(strings_po, mode='r', encoding='UTF-8')
    contents = f.read()
    f.close()

    # Write output (strings.xml)
    strings_xml = os.path.join(path, 'strings.xml')
    f = codecs.open(strings_xml, mode='w+', encoding='UTF-8')

    # Message...
    print 'Converting "%s" to "%s"...' % (strings_po, strings_xml)

    # Header...
    f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
    f.write('<!--$Revision$-->\n')
    f.write('<strings>\n')

    # Entries...
    pattern = re.compile('msgctxt "#(\d+)"\s+msgid "(.*)?"\s+msgstr "(.*)?"')
    for match in pattern.finditer(contents) :
        msgctxt =        match.group(1)
        msgid   = escape(match.group(2))
        msgstr  = escape(match.group(3))

        if (msgstr) :
            f.write('  <string id="%s">%s</string>\n' % ( msgctxt, msgstr ))
        else :
            f.write('  <string id="%s">%s</string>\n' % ( msgctxt, msgid ))

    # Footer...
    f.write('</strings>')
    f.close()

    # Return...
    return True

#
# Main
#
if len(sys.argv) == 1 :
    success = convert(os.getcwd())
    if not success :
        print ''
        print 'Convert strings.po to strings.xml (XBMC4Xbox)\n'
        print 'Syntax:'
        print '   python %s [path_to_strings.po]' % ( os.path.basename(sys.argv[0]) )
else:
    for argv in sys.argv[1:] :
        convert(argv)
