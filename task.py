class Task:
    def __init__(self, task_id, title, deadline):
        self.task_id = task_id
        self.title = title
        self.status = "To Do"
        self.deadline = deadline
        self.assignees = []   # daftar User yang ditugaskan

    def assign_user(self, user):
        self.assignees.append(user)

    def update_status(self, new_status):
        self.status = new_status

    def get_info(self):
        assigned = ", ".join([u.name for u in self.assignees]) or "Belum ada"
        return f"[{self.status}] {self.title} (Deadline: {self.deadline}) | Assigned: {assigned}"


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


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"{self.name} <{self.email}>"


class ProgressTracker:
    def calculate_progress(self, tasks):
        if not tasks:
            return 0
        done = sum(1 for t in tasks if t.status == "Done")
        return (done / len(tasks)) * 100


class ReportGenerator:
    def generate_report(self, project):
        print(f"\n--- Project Report: {project.name} ---")
        for task in project.get_tasks():
            print(task.get_info())
        tracker = ProgressTracker()
        progress = tracker.calculate_progress(project.get_tasks())
        print(f"Progress: {progress:.2f}%\n")


# --- MENU INTERAKTIF ---
def main():
    users = []
    projects = []
    report_gen = ReportGenerator()

    while True:
        print("\n=== MENU ===")
        print("1. Tambah User")
        print("2. Tambah Project")
        print("3. Tambah Task ke Project")
        print("4. Assign User ke Task")
        print("5. Update Status Task")
        print("6. Lihat Progress Project")
        print("7. Cetak Laporan Project")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            uid = len(users) + 1
            name = input("Nama User: ")
            email = input("Email User: ")
            users.append(User(uid, name, email))
            print("User berhasil ditambahkan!")

        elif pilihan == "2":
            pid = len(projects) + 1
            name = input("Nama Project: ")
            desc = input("Deskripsi Project: ")
            projects.append(Project(pid, name, desc))
            print("Project berhasil ditambahkan!")

        elif pilihan == "3":
            if not projects:
                print("Belum ada project!")
                continue
            pid = int(input("ID Project: "))
            project = next((p for p in projects if p.project_id == pid), None)
            if project:
                tid = len(project.tasks) + 1
                title = input("Judul Task: ")
                deadline = input("Deadline Task: ")
                task = Task(tid, title, deadline)
                project.add_task(task)
                print("Task berhasil ditambahkan!")
            else:
                print("Project tidak ditemukan!")

        elif pilihan == "4":
            if not users:
                print("Belum ada user!")
                continue
            if not projects:
                print("Belum ada project!")
                continue
            pid = int(input("ID Project: "))
            project = next((p for p in projects if p.project_id == pid), None)
            if project:
                tid = int(input("ID Task: "))
                task = next((t for t in project.tasks if t.task_id == tid), None)
                if task:
                    print("Daftar User:")
                    for u in users:
                        print(f"{u.user_id}. {u.name}")
                    uid = int(input("Pilih ID User: "))
                    user = next((u for u in users if u.user_id == uid), None)
                    if user:
                        task.assign_user(user)
                        print("User berhasil di-assign!")
                    else:
                        print("User tidak ditemukan!")
                else:
                    print("Task tidak ditemukan!")
            else:
                print("Project tidak ditemukan!")

        elif pilihan == "5":
            pid = int(input("ID Project: "))
            project = next((p for p in projects if p.project_id == pid), None)
            if project:
                tid = int(input("ID Task: "))
                task = next((t for t in project.tasks if t.task_id == tid), None)
                if task:
                    status = input("Masukkan status baru (To Do / In Progress / Done): ")
                    task.update_status(status)
                    print("Status berhasil diupdate!")
                else:
                    print("Task tidak ditemukan!")
            else:
                print("Project tidak ditemukan!")

        elif pilihan == "6":
            pid = int(input("ID Project: "))
            print(p.name for p in projects)
            project = next((p for p in projects if p.project_id == pid), None)
            if project:
                tracker = ProgressTracker()
                progress = tracker.calculate_progress(project.get_tasks())
                print(f"Progress Project '{project.name}': {progress:.2f}%")
            else:
                print("Project tidak ditemukan!")

        elif pilihan == "7":
            pid = int(input("ID Project: "))
            project = next((p for p in projects if p.project_id == pid), None)
            if project:
                report_gen.generate_report(project)
            else:
                print("Project tidak ditemukan!")

        elif pilihan == "0":
            print("Keluar...")
            break

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()