where pip2 >nul 2>nul
if %errorlevel%==1 (
    @echo pip2 not found, trying pip. Make sure you have python2.7 installed.
    pip install -r requirements.txt
) else (
  pip2 install -r requirements.txt
)
py -2 ea_generator\setup.py
if not exist "ea_generator\html_books\" (
  @echo creating generated books dir
  mkdir "ea_generator\html_books"
}
