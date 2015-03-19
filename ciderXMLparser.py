#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 2.7
#
# Script parses CIDER XML export and extracts data from desired 
# elements into a newly created CSV file.
#
# Run script from folder containing XML file you wish to parse.
# Script prompts user for names of XML and (new) CSV file.
# 
# In order to change extracted attributes and elements, change the values
# in the tuples xml_attributes and xml_elements, starting on rows 40 and 44. 
# The first string in each value pair is a name that will be printed to 
# the CSV file's header row. The second string in each value pair is that 
# element or attribute's XPath.  
#
# Tim Walsh, March 2015

import collections
import csv
import xml.etree.ElementTree as ET

# prompt user for names of files
in_file = raw_input('XML input file: ')
out_file = raw_input('Output file: ')

output_file = open(out_file, 'wb')
writer = csv.writer(output_file, quoting=csv.QUOTE_NONNUMERIC)

with open(in_file, 'rt') as f:
    tree = ET.parse(f)

root = tree.getroot()

print 'Reading XML...'

# store names and XPaths of desired elements and attributes in tuples
# and then convert to ordered dictionaries
xml_attributes = (('item_number', 'number'), 
                  ('parent', 'parent'))
xml_attributes = collections.OrderedDict(xml_attributes)
				  
xml_elements = (('title', './title'), 
				('restrictions', './restrictions'), 
				('dc_type', './dcType'), 
				('location', './classes/digitalObject/location'), 
				('pid', './classes/digitalObject/pid'), 
				('notes', './classes/digitalObject/notes'), 
				('original_filename', './classes/digitalObject/originalFilename'))
xml_elements = collections.OrderedDict(xml_elements)

# write csv header row
header_list = []
for key in xml_attributes.iterkeys():
    header_list.append(key)
for key in xml_elements.iterkeys():
    header_list.append(key)

writer.writerow(header_list)

# write data rows
for item in root.iter('item'):
	
	# create new dictionary for this item's info
	row_data = {}
	
	# iterate over attributes and write data to row_data
	for key, value in xml_attributes.iteritems():
		try:
		    row_data['%s' % key] = str(item.get(value).encode('utf8'))
		except AttributeError:
		    row_data['%s' % key] = ''
	
	# iterate over elements and write data to row_data
    for key, value in xml_elements.iteritems():
        try:
		    row_data['%s' % key] = str(item.find(value).text.encode('utf8'))
        except AttributeError:
		    row_data['%s' % key] = ''

	# print row to CSV
	row_values = []
    for key in xml_attributes.iterkeys():
	    row_values.append(row_data[key])
	for key in xml_elements.iterkeys():
	    row_values.append(row_data[key])
	writer.writerow(row_values)

output_file.close()

print 'Process complete. %s created.' % out_file
