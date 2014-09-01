music_download
==============

Allows you to download mp3's conveniently by just typing in a song name on terminal.

Requirements
==============
You will need a Youtube Developer's API Key. To get started, check out:
[Youtube Data API V3](https://developers.google.com/youtube/v3/getting-started). 
When your application is registered make sure you include "Youtube Data API v3" in your APIs & auth.

Additionally, [Selenium](http://selenium-python.readthedocs.org/) is required.
You can download it using 
```
pip install selenium
```
_Note_: If you get a "permission denied" error use sudo. 

Lastly, [Chromepicker](http://chromedriver.storage.googleapis.com/index.html) is needed (download via the link).

 
Instructions
==============
Replace necessary fields: the Developer API Key, your downloads folder and desired destination folder paths, and chromedriver download location.
To execute the script, run
```
python download.py --q "search_term"
```
Replace the search_term with a song name - note it must be in enclosed in quotes.
A temporary chrome window should be opened, then closed when the download completes. If the browser does not close, an error has happened. Some print statements have been left within the script to denote possible errors, and comments have been included to explain parts of the script. 
