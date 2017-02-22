# -*- coding: utf-8 -*-

import requests
import json
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from Utils import *

__all__ = ['TextAnnotation', 'AnnotationType']


class AnnotationType:
  UNCOMMON_WORD = 0
  EXTRA = 1


class TextAnnotation:

  the_type = None
  word = None
  data = None
  url = None

  def __init__(self, word, the_type):
    self.the_type = the_type
    self.word = word

    if the_type == AnnotationType.UNCOMMON_WORD:
      self.get_meaning()
    elif the_type == AnnotationType.EXTRA:
      self.get_info()

  # Gets the meaning of the set word
  # TODO: implement caching of meaning
  def get_meaning(self):
    dict_url = URLS["DICTIONARY_URL"]
    dict_api_url = URLS["DICTIONARY_API_URL"]
    # When searching use lower case version
    result = json.loads(requests.get(dict_api_url + self.word.lower()).content)

    try:
      if result['status'] == 200 and result['total'] > 0:
        self.data = (((result['results'])[0]['senses'])[0]['definition'])[0]
      else:
        self.data = None
    except Exception:
      self.data = None

    self.url = dict_url + self.word

  # Gets the info about the set word (valid for extras)
  # TODO: Implement code to get the info
  def get_info(self):
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
    self.data = r
    self.url = "http://wikipedia.org/wiki/" + self.word
