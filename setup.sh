#!/bin/sh
if ! type "pip2" > /dev/null; then
  echo "pip2 not found, trying pip. Make sure you have python2.7 installed."
  pip install -r requirements.txt
  python ea_generator/setup.py
else
  pip2 install -r requirements.txt
  python2 ea_generator/setup.py
fi
if[ ! -d "ea_generator/html_books" ]; then
  mkdir "ea_generator/html_books"
fi
