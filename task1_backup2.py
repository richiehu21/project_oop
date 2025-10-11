from datetime import datetime

class Identitas:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        def tambah_anggota_ke_tim(self, users):
            for user in users:
                self.add_member(user)
    def cetakIdentitas(self):
        return f"{self.id} - {self.name}"

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
teams = []

while True:
    print("1. Tambah Project")
    print("2. Tambah Task")
    print("3. Tambah User")
    print("4. Tampilkan Project")
    print("5. Tampilkan User")
    print("6. Tampilkan Progress Project")
    print("7. Management Tim")
    print("0. Keluar")

    pilihan = input("Pilih menu: ")

    if pilihan == "0":
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
            while True:
                print("\n--- Management Tim ---")
                print("1. Buat Tim Baru")
                print("2. Tambah Anggota ke Tim")
                print("3. Tampilkan Tim")
                print("0. Kembali")
                sub_pilihan = input("Pilih menu tim: ")

                if sub_pilihan == "0":
                    break

                elif sub_pilihan == "1":
                    tid = int(input("ID Tim: "))
                    name = input("Nama Tim: ")
                    team = Team(tid, name)
                    teams.append(team)
                    print("Tim berhasil dibuat.")

                elif sub_pilihan == "2":
                    tid = int(input("ID Tim: "))
                    team = next((t for t in teams if t.team_id == tid), None)
                    if not team:
                        print("Tim tidak ditemukan.")
                        continue
                    x = int(input("Jumlah anggota yang akan ditambahkan: "))
                    for i in range(x):
                        uid = int(input(f"ID User ke-{i+1} yang akan ditambahkan: "))
                        user = next((u for u in users if u.id == uid), None)
                        if user:
                            team.add_member(user)
                            print(f"User {user.name} berhasil ditambahkan ke Tim {team.name}.")
                        else:
                            print("User tidak ditemukan.")

                elif sub_pilihan == "3":
                    for t in teams:
                        print(f"Tim {t.team_id} - {t.name}")
                        print("Anggota:")
                        for m in t.get_members():
                            print(f"  {m.cetakIdentitas()}")

                else:
                    print("Pilihan tidak valid.")

        else:
            print("Pilihan tidak valid.")