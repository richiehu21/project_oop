from datetime import datetime

class Identitas:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def cetakIdentitas(self):
        return f"{self.id} - {self.name}"

class TeamCollection:
    def __init__(self):
        self.teams = []

    def add_team(self, team):
        self.teams.append(team)

    def get_teams(self):
        return self.teams

    def find_team(self, team_id):
        return next((t for t in self.teams if t.team_id == team_id), None)

class Project:
    def __init__(self, project_id, name, description):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks
    
    def calculate_progress(self, tasks):
        if not tasks:
            return 0
        done = sum(1 for t in tasks if t.status == "Siap")
        return (done / len(tasks)) * 100
    
class Task:
    def __init__(self,task_id, title, deadline):
        self.task_id = task_id
        self.title = title
        self.status = "To Do"
        self.deadline = deadline
        self.assigned_user = None

    def assign_user(self, user):
        self.assigned_user = user

    def update_status(self, status):
        self.status = status

    
class User(Identitas):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name)
        self.__email = email

    def cetakIdentitas(self):
        return f"{self.id} - {self.name} {self.__email}"


class Team:
    def __init__(self, team_id, name):
        self.team_id = team_id
        self.name = name
        self.members = []

    def add_member(self, user):
        self.members.append(user)

    def get_members(self):
        return self.members 
    
class Reminder:
    def __init__(self, task, remind_time):
        self.task = task
        self.remind_time = remind_time

    def check_reminder(self):
        if datetime.now() >= self.remind_time:
            print(f"Reminder: Task '{self.task.title}' is due on {self.task.deadline}")
            return True
        return False
    
projects = []
users = []

while True:
    print("1. Tambah Project")
    print("2. Tambah Task")
    print("3. Tambah User")
    print("4. Tampilkan Project")
    print("5. Tampilkan User")
    print("6. Tampilkan Progress Project")
    print("7. Keluar")

    pilihan = input("Pilih menu: ")

    if pilihan == "7":
        break

    else:
        if pilihan == "1":
            pid = int(input("ID Project: "))
            name = input("Nama Project: ")
            desc = input("Deskripsi: ")
            project = Project(pid, name, desc)
            projects.append(project)

        elif pilihan == "2":
            tid = int(input("ID Task: "))
            title = input("Judul Task: ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            task = Task(tid, title, deadline)
            pid = int(input("ID Project untuk menambahkan Task: "))
            project = next((p for p in projects if p.project_id == pid), None)
            if project:
                project.add_task(task)
            else:
                print("Project tidak ditemukan.")

        elif pilihan == "3":
            uid = int(input("ID User: "))
            name = input("Nama User: ")
            email = input("Email: ")
            user = User(uid, name, email)
            users.append(user)

        elif pilihan == "4":
            for p in projects:
                print(f"{p.project_id} - {p.name}: {p.description}")

        elif pilihan == "5":
            for u in users:
                print(u.cetakIdentitas())

        elif pilihan == "6":
            pid = input("ID Project untuk melihat progress: ")
            project = next((p for p in projects if str(p.project_id) == pid), None)
            if project:
                progress = project.calculate_progress(project.get_tasks())
                print(f"Progress Project '{project.name}': {progress:.2f}%")
            else:
                print("Project tidak ditemukan.")

        elif pilihan == "7":
            break
        
        else:
            print("Pilihan tidak valid.")