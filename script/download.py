from threading import Thread
from script.base import *

class download_manager(nhentai_obj):
    def __init__(self,code):
        super(download_manager,self).__init__()
        