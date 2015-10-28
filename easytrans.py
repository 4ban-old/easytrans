# coding: utf-8
from tkinter import *
import requests
import os
import re
import sys
import configparser
from urllib.parse import quote
from multiprocessing import Process, Queue

class Easytrans:
    def __init__(self):
        self.root = Tk()
        self.root.title("easytrans v.1.0")
        self.config = self.read_config()
        if self.config['overridedirect']:
            self.root.overrideredirect(True)
        self.root.tkraise()
        self.root.grab_set
        # notification mode: True-windows, False - notify daemon
        mode = True
        if not self.config['win_mode']:
            mode = self.config['win_mode']

        #x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        #y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        #root.wm_geometry("+%d+%d" % (x, y))
        #root.minsize(500,500)
        #root.geometry('+500+200')
        que = Queue()
        clip = self.get_clip()
        enc = self.detect_lang(clip)
        if len(clip) < 1: self._exit()
        if self.config['yandexapikey'] != '':
            ya = Process(target=self.yandex_translate, args=(que, clip, enc,))
            ya.start()
        goo = Process(target=self.google_translate, args=(que, clip, enc,))
        goo.start()

        trans = que.get()
        if self.config['yandexapikey'] != '':
            ya.terminate()
        goo.terminate()

        Label(self.root,
              text="easytrans",
              font=(self.config['textfont'], self.config['textsize']),
              bg=self.config['panelbackgroundcolor'],
              fg=self.config['panelforegroundcolor']).pack(fill='both')
        Button(self.root,
               text="[x]",
               command=self._exit,
               font=(self.config['textfont'], self.config['textsize']),
               bg=self.config['panelbackgroundcolor'],
               fg=self.config['panelforegroundcolor']).place(height = 14, width = 25, x=478)

        translate=Message(self.root,
                          text=trans,
                          anchor="nw",
                          padx=10,
                          width="490",
                          font=(self.config['textfont'], self.config['textsize']),
                          bg=self.config['panelbackgroundcolor'],
                          fg=self.config['panelforegroundcolor']).pack(side=LEFT, fill=BOTH)
        Scrollbar(translate).pack(side=RIGHT, fill=Y)
        self.root.mainloop()

    def _exit(self):
        self.root.destroy()
        sys.exit()
        self.root.quit()
        os._exit(0)

    def _help(self):
        """
            Print help into terminal.
        """
        print """Usage:
        easytrans [-h, -a]\n
        -a\tSettings.
        -h\tHelp."""

    def read_config(self):
        """
            Reading config file.
        :param config: configparser
        :return: dictionary with results.
        """
        res_config = dict()
        config=configparser.ConfigParser()
        home = os.path.expanduser("~")
        config.read(home+'.dop/easytrans/easytrans.conf')
        res_config['panelbackgroundcolor']=config['appearance']['panelbgcolor']
        res_config['panelforegroundcolor']=config['appearance']['panelfgcolor']
        res_config['backgroundcolor']=config['appearance']['bgcolor']
        res_config['foregroundcolor']=config['appearance']['fgcolor']
        res_config['textfont']=config['appearance']['textfont']
        res_config['textsize']=config['appearance']['textsize']
        res_config['overridedirect']=config['settings']['overridedirect']
        res_config['win_mode']=config['settings']['win_mode']
        res_config['yandexapikey']=config['yandexapi']['yandexapikey']
        return res_config

    def detect_lang(self, text):
        return re.search('[а-я]', text) and 'en' or 'ru'

    def get_clip(self):
        with os.popen("xsel -o") as clip:
            return clip.read()

    def google_translate(self, q, text, enc):
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
    def yandex_translate(self, q, text, enc):
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
    Easytrans()
