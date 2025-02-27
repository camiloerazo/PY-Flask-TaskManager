from enum import Enum
from datetime import datetime, date, timedelta

class TaskStatus(Enum):
    PENDING = 0
    COMPLETED = 1

class Task:
    def __init__(self, description, begin = datetime.now(), expires = None):
        self.description = description
        self.state = TaskStatus.PENDING
        self.begin = begin
        self.expires = expires
    def complete(self):
        self.state = TaskStatus.COMPLETED
    def uncomplete(self):
        self.state = TaskStatus.PENDING
    def edit(self, newDescription = None, newBegin = None, newExpires = None):
        if newDescription:
            self.description = newDescription
        elif newBegin:
            self.begin = newBegin
        else:
            self.expires = newExpires
    def toDict(self):
        return {"description":self.description, "state":self.state, "begin":self.begin, "expires":self.expires}