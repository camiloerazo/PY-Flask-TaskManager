class User:
    def __init__(self, name, password, mail):
        self.name = name
        self.password = password
        self.mail = mail
    def addTask(self, task):
        self.tasks.append(task)
    def completeTask(self, task):
        for t in self.tasks:
            print(t.description)
        #Missing code
    def editTask(self, task, newTask):
        pass
        #Missing code
    def removeTask(self, task):
        self.tasks.remove(task)
