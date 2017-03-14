# -*- coding: utf-8 -*-
"""The middleware between front-end and generator."""
import sys
import os
sys.path.insert(0, os.path.abspath('../'))
import json
import argparse
from argparse import RawTextHelpFormatter
from ea_generator.generator import Generator
from ea_generator.utils import BookNotFoundException
from ea_generator.utils import CachingType


def main():
    """The main method."""
    parser = argparse.ArgumentParser(prog="python search.py",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("action", help="The action to be taken.\n" +
                        "all = Search for the query, getting the \n" +
                        "      results as JSON\n" +
                        "single = Get a book by ID.",
                        choices=['all', 'single'])
    parser.add_argument("query", help="The query to search for.")
    parser.add_argument("-c", "--caching", help="The caching level.\n" +
                        "0 = No caching\n" +
                        "1 = Just HTML\n" +
                        "2 = Just annotations\n" +
                        "3 = Both HTML and annotations", choices=[0, 1, 2, 3],
                        default=0, type=int)
    args = parser.parse_args()
    generator = Generator()
    if args.action == 'all':
        results = generator.search_for_query(args.query)
        print(json.dumps(results))
        sys.exit()
    elif args.action == 'single':
        try:
            # The arg query will be an ID
            file_name = generator.generate_html_book(args.query,
                                                     args.caching, 2)
            with open(file_name, 'r') as f:
                print(f.read())
        except BookNotFoundException:
            print("<div class='alert alert-danger'><p>Book not found.</p>" +
                  "</div>")
    else:
        print("Invalid action.")
        parser.print_help()

if __name__ == '__main__':
    main()
