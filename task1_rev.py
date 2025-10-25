from datetime import datetime

class iterator:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self._collection):
            result = self._collection[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

class Identitas:
    def __init__(self, id, name):
        self._id = id
        self._name = name
                
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

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
        completed = list(map(lambda t: 1 if t.status == "Siap" else 0, tasks))
        return (sum(completed) / len(tasks)) * 100

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
        for r in list(self.reminders):
            try:
                if current_time >= r["remind_time"] and r["task"].status != "Siap":
                    due.append(r["task"])
            except Exception:
                continue
        return due

projects = []
users = []
teams = []
task_reminder = TaskReminder()

try:
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

        pilihan = input("Pilih menu: ").strip()
        print()

        if pilihan == "0":
            print()
            break

        else:
            if pilihan == "1":
                try:
                    print("\n--- Buat Project Baru ---")
                    pid = int(input("ID Project: ").strip())
                    name = input("Nama Project: ").strip()
                    desc = input("Deskripsi: ").strip()
                    exists = False
                    itp = iter(projects)
                    while True:
                        try:
                            p = next(itp)
                            if p.project_id == pid:
                                exists = True
                                break
                        except StopIteration:
                            break
                    if exists:
                        print("ID Project sudah ada.")
                        continue
                    project = Project(pid, name, desc)
                    projects.append(project)
                    print("Project berhasil dibuat.")
                    print()
                except ValueError:
                    print("ID Project harus berupa angka.")
                except Exception as e:
                    print("Terjadi kesalahan saat membuat project:", e)

            elif pilihan == "2":
                try:
                    print("\n--- Manage Task ---")
                    pid = int(input("ID Project: ").strip())
                    project = None
                    itp = iter(projects)
                    while True:
                        try:
                            p = next(itp)
                            if p.project_id == pid:
                                project = p
                                break
                        except StopIteration:
                            break
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
                        task_menu = input("Pilih menu task: ").strip()
                        if task_menu == "0":
                            break

                        elif task_menu == "1":
                            try:
                                print("\n--- Tambah Task ---")
                                tid = int(input("ID Task: ").strip())
                                it = iter(project.tasks)

                                result = False
                                while True:
                                    try:
                                        t = next(it)              
                                        if t.task_id == tid:   
                                            result = True
                                            break
                                    except StopIteration:
                                        break

                                if result:
                                    print("ID Task sudah ada di project ini.")
                                    continue


                                title = input("Judul Task: ").strip()
                                deadline = input("Deadline (YYYY-MM-DD): ").strip()
                                try:
                                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                                except ValueError:
                                    print("Format deadline salah. Gunakan YYYY-MM-DD.")
                                    continue
                                task = Task(tid, title, deadline)
                                project.add_task(task)
                                remind_time = deadline_date.replace(hour=9, minute=0, second=0)
                                task_reminder.add_reminder(task, remind_time)
                                print("Task berhasil ditambahkan.")
                            except ValueError:
                                print("ID Task harus berupa angka.")
                            except Exception as e:
                                print("Terjadi kesalahan saat menambah task:", e)

                        elif task_menu == "2":
                            try:
                                print("\n--- Hapus Task ---")
                                tid = int(input("ID Task yang akan dihapus: ").strip())
                                task = None
                                itt = iter(project.tasks)
                                while True:
                                    try:
                                        t = next(itt)
                                        if t.task_id == tid:
                                            task = t
                                            break
                                    except StopIteration:
                                        break

                                if task:
                                    project.tasks.remove(task)
                                    task_reminder.reminders = [r for r in task_reminder.reminders if r.get("task") != task]
                                    print("Task berhasil dihapus.")
                                else:
                                    print("Task tidak ditemukan.")
                            except ValueError:
                                print("ID Task harus berupa angka.")
                            except Exception as e:
                                print("Terjadi kesalahan saat menghapus task:", e)

                        elif task_menu == "3":
                            if not project.tasks:
                                print("Belum ada task.")
                            else:
                                print(f"\n--- Daftar Task untuk Project '{project.name}' ---")
                                itt = iter(project.tasks)
                                while True:
                                    try:
                                        t = next(itt)
                                        print(f"{t.task_id} - {t.title} | Status: {t.status} | Deadline: {t.deadline}")
                                    except StopIteration:
                                        break

                        elif task_menu == "4":
                            try:
                                print("\n--- Tandai Task Selesai ---")
                                tid = int(input("ID Task yang selesai: ").strip())
                                task = None
                                itt = iter(project.tasks)
                                while True:
                                    try:
                                        t = next(itt)
                                        if t.task_id == tid:
                                            task = t
                                            break
                                    except StopIteration:
                                        break

                                if task:
                                    task.update_status("Siap")
                                    print("Task ditandai selesai.")
                                    progress = project.calculate_progress(project.get_tasks())
                                    print(f"Progress Project '{project.name}': {progress:.2f}%")
                                else:
                                    print("Task tidak ditemukan.")
                            except ValueError:
                                print("ID Task harus berupa angka.")
                            except Exception as e:
                                print("Terjadi kesalahan saat mengupdate status task:", e)
                        else:
                            print("Pilihan tidak valid.")
                except ValueError:
                    print("ID Project harus berupa angka.")
                except Exception as e:
                    print("Terjadi kesalahan:", e)

            elif pilihan == "3":
                try:
                    print("\n--- Buat User Baru ---")
                    uid = int(input("ID User: ").strip())
                    name = input("Nama User: ").strip()
                    email = input("Email: ").strip()
                    exists = False
                    itu = iter(users)
                    while True:
                        try:
                            u = next(itu)
                            if u.id == uid:
                                exists = True
                                break
                        except StopIteration:
                            break
                    if exists:
                        print("ID User sudah ada.")
                        continue
                    user = User(uid, name, email)
                    users.append(user)
                    print("User berhasil dibuat.")
                    print()
                except ValueError:
                    print("ID User harus berupa angka.")
                except Exception as e:
                    print("Terjadi kesalahan saat membuat user:", e)
                   
            elif pilihan == "4":
                if not projects:
                    print("Belum ada project.")
                else:
                    print("\n--- Semua Project dan Progress ---")
                    itp = iter(projects)
                    while True:
                        try:
                            project = next(itp)
                            max_length = len(f"{project.project_id} - {project.name}: {project.description}")
                            print("-" * (max_length + 1))
                            print(f"{project.project_id} - {project.name}: {project.description}")
                            print("-" * (max_length + 1))
                            progress = project.calculate_progress(project.get_tasks())
                            print(f"Progress Project '{project.name}': {progress:.2f}%")
                            if project.teams:
                                print("Tim yang menangani project:")
                                itt = iter(project.teams)
                                while True:
                                    try:
                                        team = next(itt)
                                        print(f"  Tim {team.team_id} - {team.name}")
                                        print("    Anggota:")
                                        members_it = iter(team.get_members())
                                        has_member = False
                                        while True:
                                            try:
                                                member = next(members_it)
                                                has_member = True
                                                print(f"      {member.cetakIdentitas()}")
                                            except StopIteration:
                                                break
                                        if not has_member:
                                            print("      (Belum ada anggota)")
                                    except StopIteration:
                                        break
                            else:
                                print("Belum ada tim yang menangani project ini.")
                            print()
                        except StopIteration:
                            break             

            elif pilihan == "5":
                if not users:
                    print("Belum ada user.")
                else:
                    print("\n--- Semua User ---")
                    itu = iterator(users)
                    while True:
                        try:
                            u = next(itu)
                            print(u.cetakIdentitas())
                        except StopIteration:
                            break


            elif pilihan == "6":
                if not projects:
                    print("Belum ada project.")
                    continue
                print("\n--- Semua Project ---")
                max_length = 0
                itp = iter(projects)
                while True:
                    try:
                        p = next(itp)
                        string = f"{p.project_id} - {p.name}: {p.description}"
                        if len(string) > max_length:
                            max_length = len(string)
                    except StopIteration:
                        break
                itp = iter(projects)
                while True:
                    try:
                        p = next(itp)
                        string = f"{p.project_id} - {p.name}: {p.description}"
                        print("-" * (max_length + 1))
                        print(string)
                        print("-" * (max_length + 1))
                    except StopIteration:
                        break


            elif pilihan == "7":
                while True:
                    print("\n--- Management Tim ---")
                    print("1. Buat Tim Baru")
                    print("2. Tambah Anggota ke Tim")
                    print("3. Tampilkan Tim")
                    print("0. Kembali")
                    sub_pilihan = input("Pilih menu tim: ").strip()

                    if sub_pilihan == "0":
                        break

                    elif sub_pilihan == "1":
                        try:
                            print("\n--- Buat Tim Baru ---")
                            tid = int(input("ID Tim: ").strip())
                            name = input("Nama Tim: ").strip()
                            pid = int(input("ID Project: ").strip())
                            exists = False
                            itt = iter(teams)
                            while True:
                                try:
                                    tt = next(itt)
                                    if tt.team_id == tid:
                                        exists = True
                                        break
                                except StopIteration:
                                    break
                            if exists:
                                print("ID Tim sudah ada.")
                                continue
                            team = Team(tid, name)
                            project = None
                            itp = iter(projects)
                            while True:
                                try:
                                    p = next(itp)
                                    if p.project_id == pid:
                                        project = p
                                        break
                                except StopIteration:
                                    break
                            if not project:
                                print("Project tidak ditemukan.")
                                continue
                            project.append_team(team)
                            teams.append(team)
                            print("Tim berhasil dibuat dan di-assign ke project.")
                        except ValueError:
                            print("ID harus berupa angka.")
                        except Exception as e:
                            print("Terjadi kesalahan saat membuat tim:", e)

                    elif sub_pilihan == "2":
                        try:
                            print("\n--- Tambah Anggota ke Tim ---")
                            if not teams:
                                print("Belum ada tim. Buat tim terlebih dahulu.")
                                continue
                            tid = int(input("ID Tim: ").strip())
                            team = None
                            itt = iter(teams)
                            while True:
                                try:
                                    tt = next(itt)
                                    if tt.team_id == tid:
                                        team = tt
                                        break
                                except StopIteration:
                                    break
                            if not team:
                                print("Tim tidak ditemukan.")
                                continue
                            x = int(input("Jumlah anggota yang akan ditambahkan: ").strip())
                            for i in range(x):
                                try:
                                    uid = int(input(f"ID User ke-{i+1} yang akan ditambahkan: ").strip())
                                    user = None
                                    itu = iter(users)
                                    while True:
                                        try:
                                            uu = next(itu)
                                            if uu.id == uid:
                                                user = uu
                                                break
                                        except StopIteration:
                                            break
                                    if user:
                                        team.add_member(user)
                                        print(f"User {user.name} berhasil ditambahkan ke Tim {team.name}.")
                                    else:
                                        print("User tidak ditemukan.")
                                except ValueError:
                                    print("ID User harus berupa angka.")
                        except ValueError:
                            print("ID Tim atau jumlah anggota harus berupa angka.")
                        except Exception as e:
                            print("Terjadi kesalahan saat menambah anggota ke tim:", e)


                    elif sub_pilihan == "3":
                        print("\n--- Tampilkan Tim ---")
                        if not teams:
                            print("Belum ada tim.")
                            continue
                        itt = iter(teams)
                        while True:
                            try:
                                tm = next(itt)
                                print(f"Tim {tm.team_id} - {tm.name}")
                                print("Anggota:")
                                members_it = iter(tm.get_members())
                                has_member = False
                                while True:
                                    try:
                                        member = next(members_it)
                                        has_member = True
                                        print(f"  {member.cetakIdentitas()}")
                                    except StopIteration:
                                        break
                                if not has_member:
                                    print("  (Belum ada anggota)")
                            except StopIteration:
                                break
                    else:
                        print("Pilihan tidak valid.")

            elif pilihan == "8":
                print("\n--- Reminder Task ---")
                if not projects:
                    print("Belum ada project.")
                else:
                    try:
                        due_tasks = task_reminder.check_due_reminders()
                        if not due_tasks:
                            print("Tidak ada task yang perlu diingatkan.")
                        else:
                            print("Task yang perlu diingatkan:")
                            itt = iter(due_tasks)
                            while True:
                                try:
                                    task = next(itt)
                                    print(f"{task.task_id} - {task.title} | Status: {task.status} | Deadline: {task.deadline}")
                                except StopIteration:
                                    break
                    except Exception as e:
                        print("Terjadi kesalahan saat memeriksa reminder:", e)
            else:
                print("Pilihan menu tidak valid. Silakan coba lagi.")

except (KeyboardInterrupt, EOFError):
    print("\nProgram dihentikan.")
except Exception as e:
    print("Terjadi kesalahan tidak terduga:", e)