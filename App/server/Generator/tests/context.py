"""Handles the imports for tests."""

import os
import sys
sys.path.insert(0, os.path.abspath('../ebook_annotations'))
sys.path.insert(0, os.path.abspath('../'))

from Book import *
from Parser import *
from Analyser import *
from BookSearcher import *
from Generator import *
from Utils import *
