# -*- coding: utf-8 -*-
"""Contains the Annotation classes."""
import requests
import hashlib
import json
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from Utils import *

__all__ = ['TextAnnotation', 'AnnotationType']


class AnnotationType:
  """Enum for Annotation types."""

  UNCOMMON_WORD = 0
  EXTRA = 1


class TextAnnotation:
  """Annotation that contains some text.

  TODO: Make proper docstrings.
  """

  the_type = None
  word = None
  data = None
  url = None
  votes = None

  def __init__(self, word, the_type, caching=CachingType.NONE):
    """Initialise the Annotation.

    Args:
      word (str): The word this annotation is for.
      the_type (:obj:AnnotationType): The type of the annotation. Can be
                                      AnnotationType.UNCOMMON_WORD or
                                      AnnotationType.EXTRA
      caching (:obj:CachingType, optional, default=0): What caching type to
                                      use. Can be CachingType.NONE,
                                      CachingType.ANNOTATIONS,
                                      CachingType.HTML,
                                      CachingType.HTML_ANNOTATIONS
    """
    self.the_type = the_type
    self.word = word
    self.votes = 0
    self.caching = caching

    if the_type == AnnotationType.UNCOMMON_WORD:
      self.get_meaning()
    elif the_type == AnnotationType.EXTRA:
      self.get_info()

  def get_meaning(self):
    """Get the meaning of the set word."""
    # Try from db first
    if self.caching in \
       [CachingType.ANNOTATIONS, CachingType.HTML_ANNOTATIONS] and\
       self.get_from_db():
      return
    dict_url = URLS["DICTIONARY_URL"]
    dict_api_url = URLS["DICTIONARY_API_URL"]
    # When searching use lower case version
    result = json.loads(requests.get(dict_api_url + self.word.lower()).content)

    try:
      if result['status'] == 200 and result['total'] > 0:
        self.data = 'Def (from Pearson Dictionary):&nbsp;' +\
            (((result['results'])[0]['senses'])[0]['definition'])[0]
      else:
        self.data = None
    except Exception:
      self.data = None
    self.url = dict_url + self.word

  def get_info(self):
    """Get the info about the set word (valid for extras)."""
    # Try from db first
    if self.caching in \
       [CachingType.ANNOTATIONS, CachingType.HTML_ANNOTATIONS] and\
       self.get_from_db(case_sensitive=True):
      return
    w = re.sub(r"[ \"\']", '_', self.word)
    # Do sparql stuff
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbpprop: <http://dbpedia.org/property/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX yago:<http://dbpedia.org/class/yago/>
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
        PREFIX category: <http://dbpedia.org/resource/Category:>
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        PREFIX dbpedia:<http://dbpedia.org/resource/>

        SELECT ?abstract ?thumbnail
        WHERE
        {
          dbpedia:%s dbpedia-owl:abstract ?abstract ;
                                   dbpedia-owl:thumbnail ?thumbnail .
          filter(langMatches(lang(?abstract),"en"))
        }
    """ % (w))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    r = results["results"]["bindings"]
    # No result
    if(len(r) == 0):
      self.data = None
      self.url = None
      return
    # Assign the value
    r = r[0]["abstract"]["value"]
    self.url = "http://wikipedia.org/wiki/" + self.word
    # Make sure no more than 300 chars
    if len(r) > 500:
      r = r[:500] + "..."
    self.data = 'About (from Wikipedia):&nbsp;' + r

  def get_from_db(self, case_sensitive=False):
    """Get the info from the database.

    Returns:
      True if the annotation was populated from db, otherwise False.
    """
    m = hashlib.sha256()
    if case_sensitive:
      m.update(self.word)
    else:
      m.update(self.word.lower())
    conn, c = connect_database()
    c.execute('''SELECT * FROM annotations
                 WHERE hash=?
                 LIMIT 1''', (m.hexdigest(),))
    result = c.fetchone()
    if result is None:
      return False
    self.data = result[3]
    self.url = result[4]
    self.votes = result[5]
    return True

  def save_to_db(self, case_sensitive=False):
    """Save the info to the database.

    Returns:
      True if the annotation was populated from db, otherwise False.
    """
    m = hashlib.sha256()
    if case_sensitive:
      m.update(self.word)
    else:
      m.update(self.word.lower())
    conn, c = connect_database()
    c.execute('''SELECT * FROM annotations
                 WHERE hash=?
                 LIMIT 1''', (m.hexdigest(),))
    result = c.fetchone()
    if result is not None:
      # Already in, so don't save
      return False
    c.execute('''INSERT INTO annotations
                 (hash, word, data, url, votes)
                 VALUES (?, ?, ?, ?, ?)''',
              (m.hexdigest(), self.word, self.data, self.url, self.votes))
    conn.commit()
    return True
