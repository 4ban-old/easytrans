#!/bin/env python
from tkinter import *
import os
import sys
import getopt
import re
#import requests
tk = Tk()
tk.title("pytrans")
tk.overrideredirect(True)
tk.tkraise()
tk.grab_set
tk.minsize(500,500)
tk.geometry('+500+200')
#functions
def __init__():
	comm = ""
	print (comm)
def close():
	tk.quit()
	os._exit(0)
def help():
	print("""Usage:
	pytrans [-h, -a]\n
	-a\tSettings.
	-h\tPrint help.""")
	close()
def translate():
	transtext = os.popen("xsel -o | sed 's/\"[<>]//g; s/\\./,/g'").read()
	Label(tk, text=transtext, bg="#000000",fg="#e5e5e5", font=("Terminus", 8)).place(x=0, y=15)
	#enc = re.search('[йцукенгшщзхъфывапролджэячсмитьбюё]',transtext) and 'en' or 'ru' 
	#os.system("notify-send 'google''"+requests.request("GET", "http://translate.google.com/translate_a/t?client=t&text="+transtext+"&sl=auto&tl="+enc, headers={'User-Agent': 'Mozilla/5.0'}).transtext.split("\"")[1]+ "")
	#close()
def main(argv):
	try:
		options, args = getopt.getopt(argv, "a:h:t")
	except getopt.GetoptError:
		help()
	for option, arg in options:
		if option in "-h":
			help()
		elif option in "-a":
			comm = arg
		elif option in "-t":
			translate()
#code
main(sys.argv[1:])
Label(tk, text="pytrans v.1.0", bg="#0088cc", fg="#e5e5e5", font=("Terminus", 8)).place(x=0, y=0, width=450) 
Button(tk, text="close",    command=close, bg="#ff0000", fg="#e5e5e5", font=("Terminus", 8)).place(x = 450, y = 0, height = 14)
#end
tk.mainloop()

#xsel -o wget -U "Mozilla/5.0" -qO - "http://translate.google.com/translate_a/t?client=t&text=$(xsel -o | sed "s/[\"'<>]//g")&sl=auto&tl=ru" | sed 's/\[\[\[\"//' | cut -d \" -f 1
