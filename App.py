import json

class App:
    def __init__(self):
        with open("data.json",'r') as f:
            self.users = json.load(f)
    def updateData(self):
        with open("data.json",'r') as f:
            self.users = json.load(f)
    def dumpData(self):
        with open("data.json",'w') as f:
            json.dump(self.users, f, indent=4)
    def addUser(self, user, password, email):
        self.users["users"].append({"username":user, "password":password, "email":email,"tasks":[]})
        with open("data.json",'w') as f:
            json.dump(self.users, f, indent=4)
    def removeUser(self, user):
        for u in self.users["users"]:
            if u["username"] == user:
                self.users["users"].remove(u)
                with open("data.json",'w') as f:
                    json.dump(self.users, f, indent=4)