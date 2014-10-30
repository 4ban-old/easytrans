#!/bin/env python
from tkinter import *
import requests,os,re,sys,configparser
from urllib.parse import quote
from multiprocessing import Process, Queue
tk = Tk()
tk.title("easytrans")
tk.overrideredirect(True)
tk.tkraise()
tk.grab_set
tk.minsize(500,500)
tk.geometry('+500+200')
config=configparser.ConfigParser()
config.read('/home/rem/dev/python/easytrans/easytrans.conf')
panelbackgroundcolor=config['appearance']['panelbgcolor']
panelforegroundcolor=config['appearance']['panelfgcolor']
backgroundcolor=config['appearance']['bgcolor']
foregroundcolor=config['appearance']['fgcolor']
textfont=config['appearance']['textfont']
textsize=config['appearance']['textsize']
#yandex translate api key
YandexApiKey="trnsl.1.1.20141003T022807Z.4bec480b9480a548.3654b59140bca4ecd7f4d452734d93d8cd526cc3"

def close():
	tk.quit()
	os._exit(0)
def help():
	print("""Usage:
	easytrans [-h, -a]\n
	-a\tSettings.
	-h\tPrint help.""")
	close()
#simple russian language detect
def detect_lang(text):
    return re.search('[а-я]', text) and 'en' or 'ru'
def get_clip():
    with os.popen("xsel -o") as clip:
        return clip.read()
#translate with google translate API
def goo_translate(q, text, enc):
    try:
        resp = requests.request("GET",
        "http://translate.google.com/translate_a/t?client=x&text=" + quote(text)
        + "&sl=auto&tl=" + enc, headers={'User-Agent': 'Mozilla/5.0'})
    except requests.exceptions.ConnectionError:
        q.put("connection problems")

    if resp.ok:
        ret = ''
        for i in resp.json()['sentences']:
            ret += i['trans']
        resp.close()
        print("goo первый!")
        q.put(ret)
    else:
        q.put("connection problems")

#translate with yandex translate API, for working need API key
def ya_translate(q, text, enc):
    try:
        resp = requests.request("GET",
        "https://translate.yandex.net/api/v1.5/tr.json/translate?key=" + YandexApiKey
        + "&text=" + quote(text) + "&lang=" + enc + "&options=1")
    except requests.exceptions.ConnectionError:
        q.put("connection problems")

    if resp.ok:
        resp.close()
        print("ya закончил!")
        q.put(resp.json()['text'][0])
    else:
        q.put("yandex "+ resp.json()['message'])

if __name__ == "__main__":
	que=Queue()
	clip=get_clip()
	enc=detect_lang(clip)
	if len(clip) < 1: sys.exit(0)
	if YandexApiKey != '': ya = Process(target=ya_translate, args=(que, clip, enc,))
	goo = Process(target=goo_translate, args=(que, clip, enc,))
	if YandexApiKey != '': ya.start()
	goo.start()
	#get return
	trans = que.get()
	if YandexApiKey != '': ya.terminate()
	goo.terminate()
	Label(tk, text="easytrans", font=("textfont", textsize), bg=panelbackgroundcolor, fg=panelforegroundcolor).pack(fill='both')
	Button(tk, text="[x]", command=close, font=("textfont", textsize), bg=panelbackgroundcolor, fg=panelforegroundcolor).place(height = 14, width = 25, x=478)
	translate=Message(tk, text=trans,anchor="nw",padx=10, width="490", font=("textfont", textsize), bg=backgroundcolor, fg=foregroundcolor).pack(side=LEFT, fill=BOTH)
	Scrollbar(translate).pack(side=RIGHT, fill=Y)
	tk.mainloop()
