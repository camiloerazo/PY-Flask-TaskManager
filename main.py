from User import User
from App import App
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from functions import getId, createTask, transformDate, send_email, is_tomorrow

app = Flask(__name__)
app.secret_key = "supersecretkey"
taskApp = App()

@app.route("/", methods=["POST", "GET"])
def home():
    taskApp.updateData()
    session.clear()
    username = request.form.get('username')
    password = request.form.get('password')
    rusername = request.form.get('rusername')
    rpassword = request.form.get('rpassword')
    email = request.form.get('email')
    userList = taskApp.users["users"]
    if username and password:
        for dataset in userList:
            if dataset["username"] == username and dataset["password"] == password:
                print(f"User {username} logged in an sending data")
                print(dataset["tasks"])
                session["userData"] = dataset
                return redirect("/manager")
    elif rusername and rpassword:
        taskApp.addUser(rusername, rpassword, email)
    return render_template("index.html")

@app.route("/manager", methods=["GET", "POST"])
def manager():
    if "userData" not in session:
        return redirect(url_for("home"))
    # User data
    taskApp.updateData()
    dataset = session["userData"]
    print("dataset ----------------")
    print(dataset)
    usrname = dataset["username"]
    userTasks = dataset["tasks"]
    for data in taskApp.users["users"]:
        if data["username"] == usrname:
            userTasks = data["tasks"]
    cstatus = request.form.get("change_status")
    description = request.form.get("description")
    expDate = transformDate(request.form.get("date"))
    taskId = request.form.get("taskId")
    taskDesc = request.form.get("taskdesc")
    edit_task_date = request.form.get("edate")
    print("edit_task_date = ", edit_task_date)
    date = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    print("dateeeeeeeeee = ", date )
    tid = getId(userTasks)
    print("userTasks = ", userTasks)
    print("tdi = ", tid)
    ctbutton = request.form.get("createTaskButton")
    editbutton = request.form.get("editTask")
    deleteButton = request.form.get("delete")
    task_id_delete = request.form.get("task_id_delete")
    print("delte button is = ", task_id_delete)

    #send emails
    for userData in taskApp.users["users"]:
        for task in userData["tasks"]:
            expires = task["expires"]
            day, month, year = map(int, expires.split('-'))
            if is_tomorrow(day, month, year):
                print("SENDING MAAAAAAAAAAIL")
                print(dataset["email"])
                send_email("Task Reminder", f"Tu tarea '{task['description']}' se vence mañana",dataset["email"] , "juancamiloerazo82@gmail.com", "vgim yvwx gvyx ntia", "smtp.gmail.com", 587)
                

    # Change status
    if request.method == "POST" and request.form.get("change_status") != None:
        print("button was pressed and usrname = ", usrname)
        for data in taskApp.users["users"]:
            if data["username"] == usrname:
                print("found user")
                for task in data["tasks"]:
                    if task["id"] == int(cstatus):
                        print("found task")
                        if task["status"] == "pending":
                            task["status"] = "done"
                        else:
                            task["status"] = "pending"
                        userTasks = data["tasks"]
        taskApp.dumpData()
        return render_template("tasks.html", tasks=userTasks)

    # Create task
    if request.method == "POST" and ctbutton == "createTaskPressed":
        dataset["tasks"] = createTask(dataset["username"], taskApp, tid, description, date, expDate)
        session["userData"] = dataset  # Update session data
        # print(dataset["tasks"])
        return render_template("tasks.html", tasks=dataset["tasks"])

    # Edit task
    if request.method == "POST" and editbutton == "editTaskPressed":
        print("edit button pressed")
        for data in taskApp.users["users"]:
            if data["username"] == usrname:
                for task in data["tasks"]:
                    if task["id"] == int(taskId):
                        # check if none
                        if taskDesc:
                            task["description"] = taskDesc
                        elif edit_task_date:
                            task["expires"] = transformDate(edit_task_date)
                        taskApp.dumpData()
                        return render_template("tasks.html", tasks=data["tasks"])

    # Delete task
    if request.method == "POST" and task_id_delete:
        idd = int(task_id_delete)
        for i in range(0, len(taskApp.users["users"])):
            if taskApp.users["users"][i]["username"] == usrname:
                tasks = taskApp.users["users"][i]["tasks"]
                l = len(tasks)
                x = idd
                print("pre pop")
                for task in tasks:
                    print(task)
                tasks.pop(idd - 1)
                print("after pop")
                for task in tasks:
                    print(task)
                for j in range(idd - 1, l - 1):
                    # [1,2,3,4,5,6,7]
                    print(j)
                    tasks[j]["id"] = x
                    x += 1
                taskApp.users["users"][i]["tasks"] = tasks
                taskApp.dumpData()
                userTasks = taskApp.users["users"][i]["tasks"]
                session["userData"]["tasks"] = taskApp.users["users"][i]["tasks"]
                print("final")
                # for task in session["userData"]["tasks"]:
                #   print(task)
                return render_template("tasks.html", tasks=taskApp.users["users"][i]["tasks"])
    return render_template("tasks.html", tasks=dataset["tasks"])

app.run(debug=True)