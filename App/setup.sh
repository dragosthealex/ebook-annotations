#!/bin/sh
if ! type "pip2" > /dev/null; then
  echo "pip2 not found, trying pip. Make sure you have python2.7 installed."
  pip install -r requirements.txt
  python server/Generator/setup.py
else
  pip2 install -r requirements.txt
  python2 server/Generator/setup.py
fi
if[ ! -d "server/html_books" ]; then
  mkdir "server/html_books"
fi
