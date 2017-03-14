# -*- coding: utf-8 -*-
"""Misc useful functions."""
import requests
import os
import rdflib
import sqlite3
import zipfile
import tarfile
import argparse
from argparse import RawTextHelpFormatter
from limigrations import limigrations
from tqdm import tqdm

__all__ = ['URLS', 'DB_FILE_NAME', 'DB_MIGRATIONS_FOLDER', 'connect_database',
           'enclose_in_html_tag', 'COMMON_WORDS_FILE_NAME',
           'HTML_BOOKS_FOLDER', 'BookNotFoundException',
           'migrate_up', 'migrate_rollback', 'CachingType']

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
DB_FILE_NAME = os.path.join(os.path.dirname(__file__),
                            './database/database.db')
DB_MIGRATIONS_FOLDER = os.path.join(os.path.dirname(__file__),
                                    './database/migrations')
HTML_BOOKS_FOLDER = os.path.join(os.path.dirname(__file__),
                                 '../html-books')


def represents_int(s):
    """Check whether a given string represents an int."""
    try:
        int(s)
        return True
    except ValueError:
        return False


def connect_database():
    """Connect to the local database, returning the connection and a cursor."""
    conn = sqlite3.connect(DB_FILE_NAME)
    c = conn.cursor()
    return (conn, c)


def reset_migrations():
    """Drop the migrations table."""
    conn, c = connect_database()
    c.execute('''DROP TABLE IF EXISTS migrations''')
    conn.commit()


def reset_annotations():
    """Truncate the annotations table."""
    conn, c = connect_database()
    c.execute('''DELETE FROM annotations''')
    c.execute('''DELETE FROM SQLITE_SEQUENCE WHERE name='annotations' ''')
    conn.commit()


def reset_database():
    """Reset the database, creating the books table."""
    # Delete the file if it exists
    if os.path.isfile(DB_FILE_NAME):
        os.unlink(DB_FILE_NAME)
    # Create and connect to db
    conn, c = connect_database()
    c.execute('''CREATE TABLE books
                            (id text, title text UNIQUE, html_file_name text,
                             pdf_file_name, url text)''')
    conn.commit()
    c.execute('''ADD INDEX books_index (title)''')
    conn.execute()
    conn.close()
    migrate_up()


def migrate_up():
    """Run all the migrations."""
    limigrations.migrate(DB_FILE_NAME, DB_MIGRATIONS_FOLDER)


def migrate_rollback():
    """Roll back the last migration."""
    limigrations.rollback(DB_FILE_NAME, DB_MIGRATIONS_FOLDER)


def download_index_file():
    """Download the RDF files.

    Connects to a gutenberg mirror and downloads the RDF catalog that contains
    indices for all the books.
    """
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


def reset_refresh():
    """Reset the database, and reseed it.

    Resets the database, re-inserting the book entries parsed from the
    downloaded RDF files. If the RDF files are not found try to download them.
    """
    dcterms = rdflib.Namespace('http://purl.org/dc/terms/')
    # Reset the db
    reset_database()
    # Get db connection and cursor
    conn, c = connect_database()
    # Check we have rdf, else download
    if not os.isdir(RDF_CATALOG_PATH):
        download_index_file()
    # Go through all rdf files
    print("Parsing RDF files. If this process is stopped, the progress is" +
          " lost.")
    for index, directory in \
            tqdm(list(enumerate(os.listdir(RDF_CATALOG_PATH)))):
        rdf_file_name = RDF_CATALOG_PATH + '/' + directory + '/pg' +\
            directory + '.rdf'
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
        c.execute('''INSERT ON CONFLICT IGNORE
                     INTO books (id, title, html_file_name, pdf_file_name, url)
                     VALUES (?, ?, ?, ?, ?)''',
                  (the_id, title.lower(), '', '', ''))
        if index > 5000 and index % 5000 == 0:
            c.commit()
            print("Processed " + index)
    # Commit the query
    conn.commit()


def enclose_in_html_tag(tag, data, attributes=None):
    """Enclose the data in a HTML tag with attributes."""
    if attributes is None:
        attributes = {}
    text = '<' + str(tag) + ' ' + \
           ' '.join(key + '="' + value + '"'
                    for key, value in attributes.iteritems()) + '>'
    text += data
    text += '</' + tag + '>'
    return text


class BookNotFoundException(Exception):
    """Thrown if a book was not found."""

    pass


class CachingType(object):
    """Type of caching used."""

    NONE = 0
    HTML = 1
    ANNOTATIONS = 2
    HTML_ANNOTATIONS = 3


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="python Utils.py",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("action", help="The action to be taken.\n" +
                        "     m_up = Migrate the database\n" +
                        "     m_down = Roll back the last\n" +
                        "                            migration\n" +
                        "     r_db = Reset the database,\n" +
                        "                            truncating all tables\n" +
                        "     rdf = Download the RDF files\n" +
                        "     r_mig = Delete migrations\n" +
                        "     r_ann = Delete annotations",
                        choices=['m_up', 'm_down', 'r_db',
                                 'rdf', 'r_mig',
                                 'r_ann'])
    args = parser.parse_args()
    if args.action == 'm_up':
        migrate_up()
    elif args.action == 'm_down':
        migrate_rollback()
    elif args.action == 'r_db':
        reset_refresh()
    elif args.action == 'rdf':
        download_index_file()
    elif args.action == 'r_mig':
        reset_migrations()
    elif args.action == 'r_ann':
        reset_annotations()
    else:
        print("Invalid action.")
        parser.print_help()
