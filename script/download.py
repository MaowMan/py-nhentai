from threading import Thread
from script.base import *
import requests
from bs4 import BeautifulSoup
import os
from time import time

class download_manager(nhentai_obj):
    def __init__(self,code):
        super(download_manager,self).__init__()
        self.html=requests.get("{}{}".format(self.config["base-url"],code),headers=self.config["headers"]).text
        self.code=code
        self.bsobj=BeautifulSoup(self.html,"lxml")
        self.tags=self.bsobj.find("section",{"id":"tags"}).find_all("div")
        self.page=int(self.tags[-1].find_next("div").get_text().split(" ")[0])
        self.gallerycode=self.bsobj.find("div",{"id":"cover"}).find("img").get("data-src").split("/")[4]
        if self.create_folder() == False:
            return None
        self.start()
    def create_folder(self):
        if os.path.exists("{}/{}".format(self.config["content-folder"],self.code)):
            if not self.config["overwrite"]:
                return False
        else:
            os.makedirs("{}/{}".format(self.config["content-folder"],self.code))
        if self.config["keep-info"]:
            info={}
            info["code"]=self.code
            info["title"]=self.bsobj.find("h1").get_text()
            info["upload-time"]=self.bsobj.find("time").get("datetime")
            info["tags"]={}
            for tag in self.tags:
                #字串處理義大利麵code
                data=tag.text.replace("\n","").replace(":","").replace(",","").split("\t")
                result=[]
                for element in data:
                    if len(element)>2:
                        result.extend(map(lambda x: "end" if len(x)==0 else x+")",element.split(")")))
                info["tags"][result[0].replace("'","").replace(")","")]=result[1:-1]
            with open("{}/{}/info.yml".format(self.config["content-folder"],self.code),"w") as writer:
                yaml.dump(info,writer)
        return True
    def start(self):
        queue=list(map(lambda x:str(x),list(range(1,self.page+1))))
        start=time()
        threads=[]
        while queue!=[]:
            try:
                threads.append(download_thread(self.code,self.gallerycode,queue[0]))
                threads[-1].start()
                del queue[0]
            except(Exception):
                pass
        for thread in threads:
            thread.join()
        end=time()
        print(end-start)
    

class download_thread(nhentai_obj,Thread):
    def __init__(self,code,gallerycode,page):
        self.code=code
        self.gallerycode=gallerycode
        self.page=page
        super().__init__()
        super(nhentai_obj,self).__init__()
        Thread.__init__(self)
    def run(self):
        #print("running")
        for filetype in self.config["file-types"]:
            html=requests.get("{}{}/{}.{}".format(self.config["gallery-url"],self.gallerycode,self.page,filetype))
            if html.status_code==requests.codes.ok:
                break
        if filetype=="null":
            return None
        with open("{}/{}/{}-{}.{}".format(self.config["content-folder"],self.code,self.code,self.page,filetype),"wb") as writer:
            writer.write(html.content)
        

