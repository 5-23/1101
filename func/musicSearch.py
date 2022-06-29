from nextcord import Member
import json

class musicSearch():
    def __init__(self , text : str = None , user : Member = None):
        self.text = text
        self.user = user
        self.Json = []

    def read(self):
        with open("json/musicSearch.json" , "r" , encoding = "UTF-8") as f:
            try:self.Json : list = json.load(f)
            except:self.Json : list = []
        try:
            self.Json[str(self.user.id)]
        except:
            self.Json[str(self.user.id)] = [self.text]
            self.save()
        
        if self.text in self.Json[str(self.user.id)]:
            del self.Json[str(self.user.id)][self.Json[str(self.user.id)].index(self.text)]
            try:del self.Json[20][self.Json[str(self.user.id)].index(self.text)]
            except:pass

            self.Json[str(self.user.id)].insert(0 , self.text)

            self.save()
        else:
            try:del self.Json[str(self.user.id)][20]
            except:pass
            self.Json[str(self.user.id)].insert(0 , self.text)
            self.save()
        return self.Json
    
    def load(self):
        with open("json/musicSearch.json" , "r" , encoding = "UTF-8") as f:
            try:self.Json : list = json.load(f)
            except:self.Json : list = []
        try:return self.Json[str(self.user.id)]
        except:return []

    def save(self):
        with open("json/musicSearch.json" , "w" , encoding = "UTF-8") as f: json.dump(self.Json , f , indent = 4 , ensure_ascii = False)
        