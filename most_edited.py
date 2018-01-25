# Author: Sourabh Shetty
# Email:  sour@vt.edu
#         sourabhshetty@gmail.com

import xml.etree.ElementTree as ET
from datetime import datetime
import sys
import codecs

DEFAULT_XML = 'elwiki-20170601-pages-meta-history.xml'
DEFAULT_NAMESPACE = '{http://www.mediawiki.org/xml/export-0.10/}'
DEFAULT_MONTH = 4
DEFAULT_YEAR = 2017

def strip_namespace(tag):
  return tag.replace(DEFAULT_NAMESPACE, '')


def parse_xml(file_name):
  debug_counter = 0
  total_pages = 0
  page_id_needed = False

  current_page_id = ""
  current_page_title = ""
  current_page_revisions = 0

  final_id = 0
  final_title = ""
  final_revisions = 0

  context = ET.iterparse(file_name, events=('start', 'end'))
  context = iter(context)
  event, root = next(context)

  for event, elem in context:
    tag = strip_namespace(elem.tag)

    if event == "start":

      if tag == 'page':
        total_pages += 1
        current_page_revisions = 0
        page_id_needed = True

      elif tag == 'title':
        current_page_title = elem.text

      elif tag == 'id':

        if (page_id_needed):
          page_id_needed = False
          current_page_id = elem.text

    elif event == "end":

      if tag == 'page':
        if (current_page_revisions > final_revisions):
          final_revisions = current_page_revisions
          final_id = current_page_id
          final_title = current_page_title

        #if (total_pages % 4000 == 0):
          #print(total_pages)

      elif tag == 'timestamp':
        time = datetime.strptime(elem.text, "%Y-%m-%dT%H:%M:%SZ")

        if time.year == DEFAULT_YEAR and time.month == DEFAULT_MONTH:
          current_page_revisions += 1

      elem.clear()

    debug_counter += 1

    #if (c > 200):
      #break
  print("Total Pages:", total_pages)
  print("\nMost edited page in the month of", DEFAULT_MONTH, DEFAULT_YEAR, ":\n")
  print("ID:", final_id)
  print("Title:", final_title)
  print("Revisions:", final_revisions)


if __name__ == "__main__":

  # Done to avoid decoding error while printing unicode characters
  if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

  file_name = DEFAULT_XML

  if len(sys.argv) > 1:
    file_name = sys.argv[1] # Set the file name from the command line argument

  parse_xml(file_name)
