# -*- coding: utf-8 -*-

import requests
import re
import os
import sys
import rdflib
import sqlite3
import zipfile
import tarfile
from tqdm import tqdm

__all__ = ['URLS', 'DB_FILE_NAME', 'connect_database', 'enclose_in_html_tag',
           'COMMON_WORDS_FILE_NAME', 'HTML_BOOKS_FOLDER',
           'BookNotFoundException']

URLS = {
    'GUTENBERG_SEARCH': 'http://www.gutenberg.org/ebooks/search/?query=',
    'EREMITA_MIRROR': 'http://eremita.di.uminho.pt/gutenberg/',
    'MIRRORSERVICE': 'http://www.mirrorservice.org/sites/gutenberg.org/',
    'BOOK_INDEX': 'http://eremita.di.uminho.pt/gutenberg/GUTINDEX.ALL',
    'GUTENBERG_RDF_CATALOG':
    'https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.zip',
    'DICTIONARY_URL': 'http://www.ldoceonline.com/dictionary/',
    'DICTIONARY_API_URL':
    'http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword='
}

COMMON_WORDS_FILE_NAME = os.path.join(os.path.dirname(__file__),
                                      './common_words')
RDF_CATALOG_PATH = os.path.join(os.path.dirname(__file__),
                                './rdf-files/cache/epub')
DB_FILE_NAME = os.path.join(os.path.dirname(__file__), './database.db')
HTML_BOOKS_FOLDER = os.path.join(os.path.dirname(__file__), '../../html_books')


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
              (id text, title text, html_file_name text, pdf_file_name,
              url text)''')
  conn.commit()
  conn.close()


# Download the book index RDF files
def download_index_file():
  path = os.path.dirname(__file__)
  url = URLS['GUTENBERG_RDF_CATALOG']
  response = requests.get(url, stream=True)
  # Save the file, showing progress bar while streaming
  if not os.path.isfile(path + '/rdf-files.tar.zip'):
    print("Downloading book index file...\n")
    with open(path + '/rdf-files.tar.zip', 'wb') as f:
      for data in response.iter_content(chunk_size=1024):
        if data:
          f.write(data)
      print("Download complete. Unzipping...\n")
  if not os.path.isfile(path + '/rdf-files.tar'):
    with zipfile.ZipFile(path + '/rdf-files.tar.zip', 'r') as f:
      print("Extracting zip...")
      f.extractall(path)
  if not os.path.isdir(path + '/rdf-files'):
    with tarfile.open(path + '/rdf-files.tar', 'r:') as f:
      print("Extracting tar...")
      f.extractall(path + '/rdf-files')
  print("Done.")


# Update the book index file
def update_index_file(url=None):
  dcterms = rdflib.Namespace('http://purl.org/dc/terms/')
  # Reset the db
  reset_database()
  # Get db connection and cursor
  conn, c = connect_database()
  # Go through all rdf files
  print("Parsing RDF files. If this process is stopped, the progress is lost.")
  for index, directory in tqdm(list(enumerate(os.listdir(RDF_CATALOG_PATH)))):
    rdf_file_name = RDF_CATALOG_PATH + '/' + directory + '/pg' + directory + \
        '.rdf'
    g = rdflib.Graph()
    try:
      g.load(rdf_file_name)
    except Exception:
      continue

    # Get the title from rdf file
    if (None, dcterms.title, None) not in g:
      continue
    title = g.objects(None, dcterms.title).next()
    the_id = directory
    # Put title and id in db
    c.execute('''INSERT INTO books (id, title, html_file_name, pdf_file_name, url)
                 VALUES (?, ?, ?, ?, ?)''',
              (the_id, title.lower(), '', '', ''))
  # Commit the query
  conn.commit()


# Enclose some data in a given tag
def enclose_in_html_tag(tag, data, attributes={}):
  text = '<' + str(tag) + ' ' + \
         ' '.join(str(key) + '="' + str(value) + '"'
                  for key, value in attributes.iteritems()) + '>'
  text += data
  text += '</' + tag + '>'
  return text


# Exceptions
class BookNotFoundException(Exception):
  pass


if __name__ == '__main__':
  # update_index_file()
  pass
