import yaml
class nhentai_obj(object):
    def __init__(self):
        with open("config.yml","r") as stream:
            self.config=yaml.load(stream)
        self.container=[]
    def __iter__(self):
        self.counter=0
        return self
    def __next__(self):
        if self.counter==len(self.container):
            raise StopIteration
        else:
            self.counter+=1
            return self.container[self.counter-1]


class nhentai_error(BaseException):
    pass