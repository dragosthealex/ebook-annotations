import os
import sys
sys.path.insert(0, os.path.abspath('../smart_ebook_generator'))
sys.path.insert(0, os.path.abspath('../'))

from Book import *
from Parser import Parser
from Analyser import Analyser
from BookSearcher import BookSearcher
from Generator import Generator
from Utils import *
