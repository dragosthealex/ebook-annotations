# -*- coding: utf-8 -*-

import requests
import re
import os
import sys
import rdflib
import sqlite3
from tqdm import tqdm

__all__ = ['URLS', 'DB_FILE_NAME', 'connect_database']

URLS = {
  'GUTENBERG_SEARCH' : 'http://www.gutenberg.org/ebooks/search/?query=',
  'EREMITA_MIRROR' : 'http://eremita.di.uminho.pt/gutenberg/',
  'BOOK_INDEX' : 'http://eremita.di.uminho.pt/gutenberg/GUTINDEX.ALL',
  'GUTENBERG_RDF_CATALOG': 'https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.zip'
}

RDF_CATALOG_PATH = os.path.join(os.path.dirname(__file__), './rdf-files/cache/epub')
DB_FILE_NAME = os.path.join(os.path.dirname(__file__), './database.db')
# Check if string s represents an int
def represents_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False
# Connect to the database, returning the connection and a cursor
def connect_database():
  conn = sqlite3.connect(DB_FILE_NAME)
  c = conn.cursor()
  return (conn, c)

# Create the sqlite database
def reset_database():
  # Delete the file if it exists
  if os.path.isfile(DB_FILE_NAME):
    os.unlink(DB_FILE_NAME)
  # Create and connect to db
  conn, c = connect_database()
  # Create the books table
  c.execute('''CREATE TABLE books
              (title text, id text)''')
  conn.commit()
  conn.close()
# Update the book index file
def update_index_file(url = None):
  dcterms = rdflib.Namespace('http://purl.org/dc/terms/')
  # Reset the db
  reset_database()
  # Get db connection and cursor
  conn, c = connect_database()
  # Number of files to go through
  no_files = len(os.listdir(RDF_CATALOG_PATH))
  f = open('tmp.txt', 'w')
  # Go through all rdf files
  for index, directory in tqdm(list(enumerate(os.listdir(RDF_CATALOG_PATH)))[:100]):
    rdf_file_name = RDF_CATALOG_PATH + directory + '/pg' + directory + \
                    '.rdf'
    g = rdflib.Graph()
    g.load(rdf_file_name)
    # Get the title from rdf file
    if (None, dcterms.title, None) not in g:
      continue
    title = g.objects(None, dcterms.title).next()
    the_id = directory
    f.write(title.encode('utf-8') + '\n')
    # Put title and id in db
    c.execute('''INSERT INTO books (title, id)
                 VALUES (?, ?)''', (title.lower(), the_id))
  # Commit the query
  conn.commit()
  f.close()

if __name__ == '__main__':
  print "shit"
  update_index_file()
