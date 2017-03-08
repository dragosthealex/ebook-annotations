# ebook-annotations

## Description
A generator for annotated ebooks, which uses the freely available [gutenberg project](https://www.gutenberg.org) sources.
Consists of a php-based web front-end which connects to the python-based generator.

### Requirements
Generator requires **Python 2.7** (all other dependencies are installed when the setup is run).
Front-end requires any PHP server (tested with Apache).

Tested on Windows 10 and Kali Linux (debian-based). Should work without problems on other UNIX distros.

### Installation
Run App/setup.sh (or App\setup.bat) and behold.
```bash
git clone git@github.com:dragosthealex/ebook-annotations
cd ebook-annotations
./App/setup.sh
```
```bash
git clone git@github.com:dragosthealex/ebook-annotations
cd ebook-annotations
App\setup.bat
```

A one-time only step is the indexing of the available books, which is done *(automatically, by the setup script)* by downloading the project gutenberg RDF files and parsing them into a local db. This step will take some time
The RDF files archive is pretty big (~50MB) so the download time will depend on your connection speed. Then it needs to be extracted, and it will take some more time.
And the slow part is parsing all the RDF files into the db. This takes really long (~2h min on Windows 6th gen Core i7).
You can take a walk, grab a coffe, ~~watch some p\*rn~~ or anything you might like.

Also, it is recommended to **prevent the computer from turning off or otherwise interrupt the process**. Every 5000 files the connection commits the inserts, so the max number of files not inserted will be 5000. But if you interrupt the process and start again, for every insert a check will have to be made, which takes extra time, making the total duration a little bit longer.

After enabling the PHP server, make a symlink from your server root (htdocs in Apache) to point to App/front_end/www
You can name this how you want. (e.g. `ln -s ~/ebook-annotations/App/front_end/www /var/www/html/ebook-annotations`)
Then, make another symlink from the endpoint to point to App/server/www
You can also name this how you want. (e.g. `ln -s ~/ebook-annotations/App/server/www /var/www/html/ebook-annotations-api`)
Then, open the file App/front_end/.env.example and edit the value of API_ROOT to point to the second symlink (e.g. `API_ROOT="localhost/ebook-annotations-api"`)


### How to use

1. Start the PHP server, and navigate to the front-end url
2. Search for a book by name (maybe even by author in the future) and should get a list of results
3. Click any of those to generate the html book
4. ???
5. ~~Profit~~


### Coming features

- caching
- print-friendly footer annotations
- images for personalities / geo places
- **proper support for multiple books**
- optimisations?
- user voting for annotations
