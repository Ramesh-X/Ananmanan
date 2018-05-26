# Ananmanan
Song downloader for http://www.ananmanan.lk/free-sinhala-mp3

Need `python3` with `bs4`, 'urllib' and 'shutil' to work. Works in any OS with python3 support. Still writing the code. But you can download songs with url.

Goto [Anammanan](http://www.ananmanan.lk/free-sinhala-mp3) song page and copy the url to the page with list of songs.
> Eg: http://www.ananmanan.lk/free-sinhala-mp3/artist/52/sunil-edirisinghe-sinhala-mp3-songs.html

This is the song list page of the artist Sunil Edirisinghe.

Then follow the steps:
* Run the program by typing `python main.py`
* Press 3 and enter key to goto custom search mode
* Type `url` and enter key to goto url download mode
* Then enter the copied url with the minimum count as follows
> http://www.ananmanan.lk/free-sinhala-mp3/artist/52/sunil-edirisinghe-sinhala-mp3-songs.html d10000

* This will download all the songs above 10000 download count.
* Then the songs will be downloaded to the `downloads` folder.

Feel free to report any issue. It is really helpul in developing..
Thank You, Enjoy!!
