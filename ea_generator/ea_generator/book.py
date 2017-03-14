# -*- coding: utf-8 -*-
"""This module contains Book and BookSource classes.

Book represents a parsed book.
BookSource is an enum that provides maintainability
if more sources (except Gutenberg) will be added.
"""
import re
import codecs
import parser
import analyser
from utils import *

__all__ = ['Book', 'BookSource']


class BookSource(object):
    """Contains the possible sources for the original books."""

    GUTENBERG = 1


class Book(object):
    """Represents the parsed book.

    Attributes:
        the_id (str): The id of this book.
        parser (:obj:`Parser`): An instance of the parser used to parse
                                this book.
        title (str): The title of the book.
        author (str): The author of the book.
        chapter_titles (:list:str): A list containing the parsed chapter
                                    titles.
        chapters (:list:str): A list containing the parsed chapters.
        annotations (:list:obj:`Annotation`): A list containing all the
                                              annotations of this book.
        html_file_name (str): The name of the HTML file for this book.
    """

    @property
    def parser(self):
        """Get the parser."""
        return self._parser

    @parser.setter
    def parser(self, value):
        """Set the parser."""
        self._parser = value

    def __init__(self, url, the_id, source=BookSource.GUTENBERG):
        """Initialise the book."""
        self._parser = parser.GutenbergParser(url)
        self.the_id = the_id
        self.title = None
        self.author = None
        self.chapter_titles = []
        self.chapters = []
        self.annotations = []

    def is_cached_html(self):
        """Check if we already have the html version of this book.

        Returns:
        """
        conn, c = connect_database()
        c.execute('''SELECT html_file_name FROM books WHERE id = ?''',
                  (self.the_id,))
        html_file_name = c.fetchone()[0]
        conn.close()
        if html_file_name is None or html_file_name == '':
            return False
        self.html_file_name = html_file_name
        return True

    def cache_to_db(self, file_name=None):
        """Cache this book to db.

        Args:
            file_name (str): The filename of this html.
                             If let empty, will remove cache.
        """
        if file_name is None:
            file_name = ''
        conn, c = connect_database()
        c.execute('''UPDATE books
                     SET html_file_name = ?
                     WHERE id = ?''', (file_name, self.the_id))
        conn.commit()
        conn.close()

    def get_html_from_db(self):
        """Return the filename of this book form DB.

        Returns:
            The filename of this html book.
        """
        conn, c = connect_database()
        c.execute('''SELECT html_file_name FROM books WHERE id = ?''',
                  (self.the_id,))
        html_file_name = c.fetchone()[0]
        conn.close()
        return html_file_name

    def populate_content(self):
        """Use the parser to parse everything and get the content."""
        self.title = self.parser.get_title()
        self.author = self.parser.get_author()
        self.chapter_titles = self.parser.get_chapter_titles()
        self.chapters = self.parser.get_chapters()
        if self.title is None or self.author is None or \
                len(self.chapter_titles) == 0 or len(self.chapters) == 0:
            raise BookNotFoundException('Book was not found.')

    def create_annotations(self, chapters=0, caching=CachingType.NONE):
        """Analyse the text and create the annotations.

        Using the analyser, generate the annotations for all the chapters.

        Args:
            chapters (int, optional, default=0): How many chapters to analyse.
                                                0 means analyse all.
            caching (:obj:`CachingType, optional, default=0): What caching to
                                                use. Can be CachingType.NONE,
                                                CachingType.ANNOTATIONS,
                                                CachingType.HTML,
                                                CachingType.HTML_ANNOTATIONS
        """
        if chapters == 0:
            text = ' '.join(self.chapters)
        else:
            text = ' '.join(self.chapters[:chapters])
        ana = analyser.Analyser(text)
        self.annotations = ana.generate_annotations(caching)

    def annotate(self, chapters=0):
        """Apply the annotations for all the chapters.

        Args:
            chapters (int, optional, default=0): How many chapters to annotate.
                                                 0 means analyse all.
        """
        if chapters == 0:
            for index, chapter in enumerate(self.chapters):
                self.chapters[index] = self.apply_annotations(chapter)
        else:
            for index, chapter in enumerate(self.chapters[:chapters]):
                self.chapters[index] = self.apply_annotations(chapter)

    def apply_annotations(self, text):
        """Apply the annotations on the words.

        Args:
            text (str): The text to annotate.

        Returns:
            The annotated text.
        """
        # split text into individual words
        words = text.split(' ')
        # Get just the annotation words
        words_to_annotate = [ann.word for ann in self.annotations]
        ana = analyser.Analyser(None)
        # Deal with multiple words proper nouns
        proposed_ann_word = words[0]
        in_word = False
        number_of_words = 1
        for index, current_word in enumerate(words):
            # We need to remove extra stuff, like when looked for annotations
            current_word = ana.preprocess_input(current_word)
            # Test next word
            next_word = "~!~"
            if index + 1 < len(words):
                next_word = ana.preprocess_input(words[index + 1])

            if not in_word:
                if (current_word + " " + next_word) in words_to_annotate:
                    proposed_ann_word = current_word + " " + next_word
                    number_of_words = 2
                    in_word = True
                    continue
                else:
                    proposed_ann_word = current_word
                    number_of_words = 1
            else:
                if (proposed_ann_word + " " + next_word) in words_to_annotate:
                    proposed_ann_word += " " + next_word
                    number_of_words += 1
                    continue
                else:
                    in_word = False

            # Check if the word or its lower case version is to be annotated
            if proposed_ann_word in words_to_annotate:
                # Get the annotation tag
                ann = self.annotations[words_to_annotate
                                       .index(proposed_ann_word)]
                # We didn't find the meaning
                if ann.data is None:
                    continue
                tag = enclose_in_html_tag('a', str(proposed_ann_word),
                                          {'class': 'annotation',
                                           'data-content': '' + ann.data,
                                           'title': "<a target='_blank' " +
                                           "href='" + ann.url +
                                           "'>More</a>"})
                # Replace the processed word found with a tag with the
                # annotation
                if number_of_words == 1:
                    words[index] = re.sub(proposed_ann_word, tag, current_word)
                else:
                    # Delete words
                    words[index - number_of_words + 1:index + 1] = []
                    # Replace with tag
                    words.insert(index - number_of_words + 1, tag)
                # Remove annotation from list
                if ann in self.annotations:
                    self.annotations.remove(ann)
                    words_to_annotate.remove(proposed_ann_word)
        # Rebuild the original text
        text = ' '.join(words)
        return text

    def print_text(self, file_name='book.txt'):
        """Print the book contents into a text file.

        Args:
            file_name (str): The file name where to print the text.
        """
        with codecs.open(file_name, 'w', encoding="utf-8") as f:
            f.write(self.title)
            f.write('\n')
            f.write(self.author)
            f.write('\n')
            f.write(' '.join(self.chapter_titles))
            f.write('\n')
            f.write('\n'.join(self.chapters))
