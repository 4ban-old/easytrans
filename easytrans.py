#!/bin/env python
from tkinter import *
import os
import sys
import getopt
import re
import requests
tk = Tk()
tk.title("easytrans")
tk.overrideredirect(True)
tk.tkraise()
tk.grab_set
tk.minsize(500,500)
tk.geometry('+500+200')
##############
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
	enc = re.search('[йцукенгшщзхъфывапролджэячсмитьбюё]',transtext) and 'en' or 'ru' 
	translation = requests.request("GET", "http://translate.google.com/translate_a/t?client=t&text="+transtext+"&sl=auto&tl="+enc, headers={'User-Agent': 'Mozilla/5.0'}).text.split("\"")[1]
	Message(tk, text=transtext+"\n ---------------------------------------------------------------------------------\n"+translation, justify="left", width="497" ,fg="#e5e5e5", font=("Terminus", 8)).place(x=0, y=15)
	#close()
def main(argv):
	try:
		options, args = getopt.getopt(argv, "h")
	except getopt.GetoptError:
		help()
	for option, arg in options:
		if option in "-h":
			help()
#############
main(sys.argv[1:])
translate()
Label(tk, text="easytrans v.1.0", bg="#0088cc", fg="#e5e5e5", font=("Terminus", 8)).place(x=0, y=0, width=450) 
Button(tk, text="close", command=close, bg="#ff0000", fg="#e5e5e5", font=("Terminus", 8)).place(x = 450, y = 0, height = 14)

tk.mainloop()