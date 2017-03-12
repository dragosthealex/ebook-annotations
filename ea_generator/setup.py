#!/usr/bin/python
import nltk
from ebook_annotations import Utils as u

nltk.download('tagsets')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')

# Download raw RDF files
u.download_index_file()
# Create local DB and populate it with the indices
u.update_index_file()
