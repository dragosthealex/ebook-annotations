# -*- coding: utf-8 -*-
"""This module contains the Generator class.

Used to generate the HTML file from a given ID / query.
"""
import codecs
import argparse
from argparse import RawTextHelpFormatter
import book as bk
import book_searcher as b_searcher
from utils import *

__all__ = ['Generator']


class Generator(object):
    """The main class for of the module.

    Implements the pipeline, providing a method for generating
    a html file for a given ID and returning the results.

    Attributes:
        book (:obj:`Book`): An instance of the book that is currently
        generated.
        html_file_name (str): The name of the generated HTML file.
        searcher (:obj:`BookSearcher`): An instance of the searcher used
                                        to get books.
    """

    @property
    def book(self):  # pragma: no-cover
        """Get the book."""
        if self._book is None:
            raise AttributeError("Attribute book was not set.")
        return self._book

    @book.setter
    def book(self, value):  # pragma: no-cover
        """Set the book."""
        self._book = value

    @property
    def html_file_name(self):  # pragma: no-cover
        """Get the html book file name."""
        if self._html_file_name is None:
            raise AttributeError("Attribute html_file_name was not set.")
        return self._html_file_name

    @html_file_name.setter
    def html_file_name(self, value):  # pragma: no-cover
        """Set the html book file name."""
        self._html_file_name = value

    @property
    def searcher(self):  # pragma: no-cover
        """Get the resulted url."""
        if self._searcher is None:
            raise AttributeError("Attribute searcher was not set.")
        return self._searcher

    @searcher.setter
    def searcher(self, value):  # pragma: no-cover
        """Set the resulted url."""
        self._searcher = value

    def __init__(self):
        """Initialise the Generator."""
        self._book = None
        self._html_file_name = None
        self._searcher = b_searcher.BookSearcher()

    def search_for_query(self, query):
        """Search for a query and returns the possible matches.

        Params:
            query (str): The query to search for.

        Returns:
            A list of dicts containing the book id and title of all the
            resulted books.
        """
        self.searcher.search_query = query
        results = self.searcher.search_for_query()
        return results

    def generate_html_book(self, the_id, caching=CachingType.NONE,
                           max_chapters=0):
        """Generate the html book given a title.

        Args:
            query (str): The query to search for. If set, it returns the first
            caching (:obj:`CachingType`, optional, default=0): What caching
                                        type to use. Can be CachingType.NONE,
                                        CachingType.ANNOTATIONS,
                                        CachingType.HTML,
                                        CachingType.HTML_ANNOTATIONS
            max_chapters (int, default=0): The maximum numbers of chapters to
                                        analyse
                                        and annotate. 0 means analyse all.

        Returns:
            The absolute path to the generated file.
        """
        # Get the url and the source from the query
        self.searcher.book_id = the_id
        # Create the book from url and source
        the_url, the_id, src = self.searcher.get_book_info()
        book = bk.Book(the_url, the_id, src)

        # Check html caching
        if caching in [CachingType.HTML, CachingType.HTML_ANNOTATIONS] and\
                book.is_cached_html():
            return book.get_html_file_name()
        # Else, parse the book into the object
        book.populate_content()
        self.book = book

        # Put title in tags
        title = enclose_in_html_tag('h1', book.title, {'class': 'title'})
        # Put author in tags
        author = enclose_in_html_tag('h2', book.author, {'class': 'author'})
        # Put the table of contents in tags
        table_of_contents = ''
        for index, chapter in enumerate(book.chapter_titles):
            chapter_tag = enclose_in_html_tag('a', chapter,
                                              {'href': '#ch-' + str(index)})
            table_of_contents += enclose_in_html_tag('li', chapter_tag)
        table_of_contents = enclose_in_html_tag('ul', table_of_contents,
                                                {'class': 'chapter_title'})

        # Annotate the text (in chapters)
        book.create_annotations(max_chapters, caching)
        book.annotate(max_chapters)

        # Put the chapters in tags
        chapters = ''
        for index, chapter in enumerate(book.chapters):
            ch_title = ""
            if len(book.chapter_titles) > 0:
                ch_title = enclose_in_html_tag('a', book.chapter_titles[index],
                                               {'name': 'ch-' + str(index)})
            ch_title = enclose_in_html_tag('h3', ch_title,
                                           {'class': 'chapter-title'})
            # chapter = re.sub(r'(([^\n]*\n[^\n]*)\n)', r'\1<br>', chapter)
            chapter = enclose_in_html_tag('p', chapter,
                                          {'class': 'chapter-body'})
            chapters += enclose_in_html_tag('div', ch_title + chapter,
                                            {'class': 'chapter'})
        # Enclose everything in a div tag with class book
        file_name = HTML_BOOKS_FOLDER + '/' + str(the_id) + '.html'
        # Create the html file
        with codecs.open(file_name, 'w', encoding="utf-8") as f:
            f.write(enclose_in_html_tag('div', title + author +
                                        table_of_contents +
                                        chapters, {'class': 'book'}))
        # Return its name
        return file_name


def main():
    """Run this module as stand-alone."""
    parser = argparse.ArgumentParser(prog="python Generator.py",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("action", help="Action to take.\n" +
                        "search = look for the book by title, returning \n" +
                        "           the ids of matching books. Query \n" +
                        "           should be the title.\n" +
                        "get = generates the html of the book by ID, query\n" +
                        "           should be the ID",
                        choices=['search', 'get'])
    parser.add_argument("query", help="The query to use when searching.")
    parser.add_argument("-c", "--caching", help="The caching level.\n" +
                        "0 = No caching\n" +
                        "1 = Just HTML\n" +
                        "2 = Just annotations\n" +
                        "3 = Both HTML and annotations", choices=[0, 1, 2, 3],
                        default=0, type=int)
    parser.add_argument("-m", "--max-chapters", help="The maximum amount of " +
                        "chapters to annotate. 0 means all", default=2,
                        type=int)
    args = parser.parse_args()
    g = Generator()
    if args.action == 'search':
        result = g.search_for_query(args.query)
        if len(result) == 0:
            result = 'No results.'
        else:
            result = '\n'.join([str(r) for r in result])
    elif args.action == 'get':
        result = g.generate_html_book(args.query, args.caching,
                                      args.max_chapters)
        g.book.print_text('result.txt')
        print('Book contents were printed in result.txt')
    else:
        print("Invalid action.")
        parser.print_help()
    print(result)

if __name__ == '__main__':
    main()
