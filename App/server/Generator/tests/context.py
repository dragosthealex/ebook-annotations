import os
import sys
sys.path.insert(0, os.path.abspath('../smart_ebook_generator'))
sys.path.insert(0, os.path.abspath('../'))

from Book import Book
from Parser import Parser
from Analyser import Analyser
from UrlSearcher import UrlSearcher2
from utils import *