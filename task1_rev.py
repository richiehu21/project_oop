from datetime import datetime

class Identitas:
    def __init__(self, id, name):
        self._id = id
        self._name = name
                
    def cetakIdentitas(self):
        return f"{self._id} - {self._name}"

class User(Identitas):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name)
        self.__email = email

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, new_email):
        if "@" not in new_email:
            print("Email tidak valid. Harus mengandung '@'")
        else:
            self.__email = new_email

    def cetakIdentitas(self):
        return f"{self.id} - {self.name} - {self.__email}"


class Project:
    def __init__(self, project_id, name, description):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.tasks = []
        self.teams = []
    
    def append_team(self, team):
        self.teams.append(team)

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

    def update_status(self, status):
        self.status = status

class Team:
    def __init__(self, team_id, name):
        self.team_id = team_id
        self.name = name
        self.members = []

    def add_member(self, user):
        self.members.append(user)

    def get_members(self):
        return self.members 

class TaskReminder:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, task, remind_time):
        self.reminders.append({"task": task, "remind_time": remind_time})

    def check_due_reminders(self):
        current_time = datetime.now()
        due = []
        for r in self.reminders:
            if current_time >= r["remind_time"] and r["task"].status != "Siap":
                due.append(r["task"])
        return due

projects = []
users = []
teams = []
task_reminder = TaskReminder()

while True:
    print(
"""\n--- Menu Utama ---
1. Buat Project Baru
2. Manage Task dalam Project
3. Buat User Baru
4. Tampilkan Semua Project dan Progress
5. Tampilkan Semua User
6. Tampilkan Semua Project
7. Management Tim
8. Reminder Task
0. Keluar""")

    pilihan = input("Pilih menu: ")
    print()

    if pilihan == "0":
        print()
        break

    else:
        if pilihan == "1":
            print("\n--- Buat Project Baru ---")
            pid = int(input("ID Project: "))
            name = input("Nama Project: ")
            desc = input("Deskripsi: ")
            project = Project(pid, name, desc)
            projects.append(project)
            print("Project berhasil dibuat.")
            print()

        elif pilihan == "2":
            print("\n--- Manage Task ---")
            pid = int(input("ID Project: "))
            project = next((p for p in projects if p.project_id == pid), None)
            if not project:
                print("Project tidak ditemukan.")
                continue
            while True:
                print(f"\n--- Manage Task untuk Project '{project.name}' ---")
                print("1. Tambah Task")
                print("2. Hapus Task")
                print("3. Tampilkan Task")
                print("4. Tandai Task Selesai")
                print("0. Kembali")
                task_menu = input("Pilih menu task: ")
                if task_menu == "0":
                    break

                elif task_menu == "1":
                    print("\n--- Tambah Task ---")
                    tid = int(input("ID Task: "))
                    title = input("Judul Task: ")
                    deadline = input("Deadline (YYYY-MM-DD): ")
                    task = Task(tid, title, deadline)
                    project.add_task(task)
                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                    remind_time = deadline_date.replace(hour=9, minute=0, second=0)
                    task_reminder.add_reminder(task, remind_time)
                    print("Task berhasil ditambahkan.") 

                elif task_menu == "2":
                    print("\n--- Hapus Task ---")
                    tid = int(input("ID Task yang akan dihapus: "))
                    before = len(project.tasks)
                    print("Task berhasil dihapus.")
                elif task_menu == "3":
                    if not project.tasks:
                        print("Belum ada task.")
                    else:
                        print(f"\n--- Daftar Task untuk Project '{project.name}' ---")
                        for t in project.tasks:
                            print(f"{t.task_id} - {t.title} | Status: {t.status} | Deadline: {t.deadline}")

                elif task_menu == "4":
                    print("\n--- Tandai Task Selesai ---")
                    tid = int(input("ID Task yang selesai: "))
                    task = next((t for t in project.tasks if t.task_id == tid), None)
                    if task:
                        task.update_status("Siap")
                        print("Task ditandai selesai.")
                        progress = project.calculate_progress(project.get_tasks())
                        print(f"Progress Project '{project.name}': {progress:.2f}%")
                    else:
                        print("Task tidak ditemukan.")
                else:
                    print("Pilihan tidak valid.")

        elif pilihan == "3":
            print("\n--- Buat User Baru ---")
            uid = int(input("ID User: "))
            name = input("Nama User: ")
            email = input("Email: ")
            user = User(uid, name, email)
            users.append(user)
            print("User berhasil dibuat.")
            print()     
               
        elif pilihan == "4":
            if not projects:
                print("Belum ada project.")
            else:
                print("\n--- Semua Project dan Progress ---")
                for project in projects:
                    max_length = len(f"{project.project_id} - {project.name}: {project.description}")
                    print("-" * (max_length + 1))
                    print(f"{project.project_id} - {project.name}: {project.description}")
                    print("-" * (max_length + 1))
                    progress = project.calculate_progress(project.get_tasks())
                    print(f"Progress Project '{project.name}': {progress:.2f}%")
                    if project.teams:
                        print("Tim yang menangani project:")
                        for team in project.teams:
                            print(f"  Tim {team.team_id} - {team.name}")
                            print("    Anggota:")
                            if team.members:
                                for member in team.get_members():
                                    print(f"{member.cetakIdentitas()}")
                            else:
                                print("      (Belum ada anggota)")
                    else:
                        print("Belum ada tim yang menangani project ini.")
                    print()             

        elif pilihan == "5":
            if not users:
                print("Belum ada user.")
            else:
                print("\n--- Semua User ---")
            for u in users:
                print(u.cetakIdentitas())


        elif pilihan == "6":
            if not projects:
                print("Belum ada project.")
                continue
            print("\n--- Semua Project ---")
            max_length = 0
            for p in projects:
                string = f"{p.project_id} - {p.name}: {p.description}"
                if len(string) > max_length:
                    max_length = len(string)
            for p in projects:
                string = f"{p.project_id} - {p.name}: {p.description}"
                print("-" * (max_length + 1))
                print(string)
                print("-" * (max_length + 1))


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
                    print("\n--- Buat Tim Baru ---")
                    tid = int(input("ID Tim: "))
                    name = input("Nama Tim: ")
                    pid = int(input("ID Project: "))
                    team = Team(tid, name)
                    project = next((p for p in projects if p.project_id == pid), None)
                    if not project:
                        print("Project tidak ditemukan.")
                        continue
                    project.append_team(team)
                    teams.append(team)
                    print("Tim berhasil dibuat dan di-assign ke project.")

                elif sub_pilihan == "2":
                    print("\n--- Tambah Anggota ke Tim ---")
                    if not teams:
                        print("Belum ada tim. Buat tim terlebih dahulu.")
                        continue
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
                    print("\n--- Tampilkan Tim ---")
                    if not teams:
                        print("Belum ada tim.")
                        continue
                    for t in teams:
                        print(f"Tim {t.team_id} - {t.name}")
                        print("Anggota:")
                        if t.get_members():
                                for t in t.get_members():
                                    print(f"  {t.cetakIdentitas()}")
                        else:
                            print("  (Belum ada anggota)")
                else:
        
                    print("Pilihan tidak valid.")

        elif pilihan == "8":
            print("\n--- Reminder Task ---")
            if not projects:
                print("Belum ada project.")
            else:
                due_tasks = task_reminder.check_due_reminders()
                if not due_tasks:
                    print("Tidak ada task yang perlu diingatkan.")
                else:
                    print("Task yang perlu diingatkan:")
                    for task in due_tasks:
                        print(f"{task.task_id} - {task.title} | Status: {task.status} | Deadline: {task.deadline}")