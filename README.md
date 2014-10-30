## DESCRIPTION ##
easytrans is a small program to translate the selected text on Russian lang. Written by python with tkinter. Use a google and yandex api for translation.

## Dependencies ##

`tk` `getopt` `re` `requests` `xsel` `python-requests` `python-urllib` `python-gobject`

## Use ##

```
make dir easytrans
$ mkdir /path/easytrans
$ cd /path/easytrans

clone easytrans
$ git clone https://bitbucket.org:remasik/easytrans.git

rights
# chmod +x easytrans.py
$ ./easytrans.py
```
> You can assign a hotkey for start an tkmenu
```
For change settings and applications you must edit easytrans.conf, which is located in programm folder

[appearance]
panelbgcolor=#e4e4e4
panelfgcolor=#343434
bgcolor=#232323
fgcolor=#e4e4e4
textfont=Terminus
textsize=8
```
![No image](https://bytebucket.org/remasik/easytrans/raw/05edb1958f763d40d82a93d448df9e6c86075bf5/screen/screen.png)

>  font and size may differ from that in the screenshot