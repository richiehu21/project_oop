from datetime import datetime
from abc import ABC, abstractmethod 

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

class Identitas(ABC):
    def __init__(self, id, name):
        self._id = id      
        self._name = name  
                
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @abstractmethod  
    def cetakIdentitas(self):
        pass

class User(Identitas):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name)
        self.__email = None 
        self.email = email  

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, new_email):
        if new_email and "@" in new_email:
            self.__email = new_email
        elif new_email is None:
            self.__email = None
        else:
            print(f"Email '{new_email}' tidak valid. Harus mengandung '@'. Email tidak diubah.")

    def cetakIdentitas(self):
        return f"{self.id} - {self.name} - {self.__email}"


class Project(Identitas):
    def __init__(self, project_id, nama_project, description):
        super().__init__(project_id, nama_project)
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
        completed_tasks = (1 for task in tasks if task.status == "Siap")
        return (sum(completed_tasks) / len(tasks)) * 100

    def cetakIdentitas(self):
        return f"{self.id} - {self.name}: {self.description}"


def get_task_titles(project):
    for task in project.tasks:
        yield task.name


def task_status_monitor():
    while True:
        task = yield
        if task.status == "Siap":
            print(f"Task '{task.name}' telah selesai!")
        elif task.status == "To Do":
            print(f"Task '{task.name}' masih dalam pengerjaan")

class Task(Identitas):
    def __init__(self,task_id, title, deadline):
        super().__init__(task_id, title)
        self.status = "To Do"
        self.deadline = deadline

    def update_status(self, status):
        self.status = status
    
    def cetakIdentitas(self):
        return f"{self.id} - {self.name} | Status: {self.status} | Deadline: {self.deadline}"

class Team(Identitas):
    def __init__(self, team_id, name):
        super().__init__(team_id, name)
        self.members = []

    
    
    def add_member(self, *users):
        for user in users:
            if isinstance(user, User):
                self.members.append(user)
                print(f"User {user.name} berhasil ditambahkan ke Tim {self.name}.")
            else:
                print(f"Item {user} bukan User object yang valid.")

    def get_members(self):
        return self.members 
    
    def cetakIdentitas(self):
        return f"Tim {self.id} - {self.name}"
        
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






#=================DUMMY===================


user1 = User(101, "Budi Santoso", "budi@example.com")
user2 = User(102, "Citra Lestari", "citra@example.com")

user3 = User(103, "Doni Firmansyah", "doni.invalid") 

users = [user1, user2, user3]


project1 = Project(1, "Sistem E-commerce", "Pengembangan platform e-commerce baru")
project2 = Project(2, "Aplikasi Mobile Banking", "Pembuatan aplikasi mobile untuk nasabah")

projects = [project1, project2] 


task1 = Task(1001, "Desain Halaman Utama", datetime(2025, 11, 10))
task2 = Task(1002, "Implementasi Keranjang Belanja", datetime(2025, 11, 15))
task3 = Task(2001, "Setup Database API", datetime(2025, 11, 12))


team1 = Team(50, "Tim Frontend")
team2 = Team(51, "Tim Backend")

teams = [team1, team2]


project1.add_task(task1)
project1.add_task(task2)
project2.add_task(task3)


project1.append_team(team1)
project2.append_team(team2)


team1.add_member(user1, user2) 
team2.add_member(user3)        


task_reminder = TaskReminder()

task_reminder.add_reminder(task1, task1.deadline.replace(hour=9, minute=0))
task_reminder.add_reminder(task2, task2.deadline.replace(hour=9, minute=0))
task_reminder.add_reminder(task3, task3.deadline.replace(hour=9, minute=0))

#=================DUMMY END===================



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
                            if p.id == pid:
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
                            if p.id == pid:
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
                                        if t.id == tid:   
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
                                task = Task(tid, title, deadline_date)
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
                                        if t.id == tid:
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
                                        print(t.cetakIdentitas())
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
                                        if t.id == tid:
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
                    
                    if user.email is None:
                        print(f"Peringatan: Email '{email}' tidak valid dan tidak disimpan.")
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
                            max_length = len(project.cetakIdentitas())
                            print("-" * (max_length + 1))
                            print(project.cetakIdentitas())
                            print("-" * (max_length + 1))
                            
                            print("Daftar Task:")
                            
                            for title in get_task_titles(project):
                                print(f"- {title}")
                            
                            
                            print("\nStatus Tasks:")
                            
                            monitor = task_status_monitor()
                            next(monitor) 
                            for task in project.tasks:
                                monitor.send(task) 
                            monitor.close()
                
                            progress = project.calculate_progress(project.get_tasks())
                            print(f"Progress Project '{project.name}': {progress:.2f}%")
                            if project.teams:
                                print("Tim yang menangani project:")
                                itt = iter(project.teams)
                                while True:
                                    try:
                                        team = next(itt)
                                        print(team.cetakIdentitas())
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
                    identitas_iterator = map(lambda user: user.cetakIdentitas(), users)
                    for identitas_str in identitas_iterator:
                        print(identitas_str)


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
                        string = p.cetakIdentitas()
                        if len(string) > max_length:
                            max_length = len(string)
                    except StopIteration:
                        break

                itp = iter(projects)
                finished = False
                while not finished:
                    try:
                        p = next(itp)
                        string = p.cetakIdentitas()
                        print("-" * (max_length + 1))
                        print(string)
                        print("-" * (max_length + 1))
                    except StopIteration:
                        finished = True
                    finally:
                        if finished:
                            print("Semua project sudah ditampilkan.")
                

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
                                    if tt.id== tid:
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
                                    if p.id == pid:
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
                                    if tt.id == tid:
                                        team = tt
                                        break
                                except StopIteration:
                                    break
                            if not team:
                                print("Tim tidak ditemukan.")
                                continue
                            
                            uids_str = input("Masukkan ID User yang akan ditambahkan (pisahkan dengan koma, cth: 1, 2, 3): ").strip()
                            if not uids_str:
                                print("Tidak ada ID User yang dimasukkan.")
                                continue
                            
                            user_map = {user.id: user for user in users}
                            
                            target_id_strs = [s.strip() for s in uids_str.split(',') if s.strip()]
                            target_ids = set()
                            invalid_inputs = []

                            for s in target_id_strs:
                                try:
                                    target_ids.add(int(s))
                                except ValueError:
                                    invalid_inputs.append(s)

                            users_to_add = [user_map[uid] for uid in target_ids if uid in user_map]
                            
                            found_ids = {user.id for user in users_to_add}
                            
                            not_found_ids = target_ids - found_ids 
                            
                            if invalid_inputs:
                                print(f"Input berikut bukan ID angka yang valid: {', '.join(invalid_inputs)}")
                            if not_found_ids:
                                print(f"User dengan ID berikut tidak ditemukan: {', '.join(map(str, not_found_ids))}")
                            
                            if users_to_add:
                                team.add_member(*users_to_add) 
                            else:
                                print("Tidak ada user valid yang ditambahkan.")
                            
                                
                        except ValueError:
                            print("ID Tim harus berupa angka.")
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
                                print(tm.cetakIdentitas()) 
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
                                    print(task.cetakIdentitas())
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