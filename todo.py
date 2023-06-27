from colorama import Fore, Back, Style
from tabulate import tabulate
import csv
import os


class Task:
    def __init__(self, body="", priority="normal", status="incomplete"):
        """
        Creates a new object from the class Task

        :param body: A string containing the body of the task
        :type file_name: str
        :param priority: A string containing the priority of the task
        :type file_name: str
        :param status: A string containing the status of the task
        :type file_name: str
        :return: An object of class Task
        :r type: class Task
        """
        self.body = body
        self.priority = priority
        self.status = status

    def __str__(self):
        headers = ["Task", "Priority", "Status"]
        # return f"{self.body}\t{self.priority}\t{self.status}"
        return tabulate(
            [[self.body, self.priority, self.status]],
            headers,
            tablefmt="mixed_grid",
            colalign=("left", "center", "center"),
            maxcolwidths=[120, 8, 10],
        )

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        if priority.lower().strip() in ["low", "normal", "high"]:
            self._priority = priority.lower().strip()
        else:
            raise ValueError("Invalid Priority. Priority can be low, normal or high")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status.lower().strip() in ["complete", "incomplete"]:
            self._status = status.lower().strip()
        else:
            raise ValueError("Invalid Status. Status can be complete or incomplete")


class Note:
    def __init__(self, title=""):
        """
        Creates a new object from the class Note

        :param title: A string containing the title of the note
        :type file_name: str
        :return: An object of class note
        :r type: class Note
        """
        self.num_of_tasks = 0
        self.tasks = []
        self.title = title


    def __str__(self):
        """
        Returns a string ready for use in print function.

        :return: Returns a string in the table format from all the tasks inside the Note.
        :rtype: str
        """
        headers = [
            Fore.CYAN + "No" + Style.RESET_ALL,
            Fore.CYAN + "Task" + Style.RESET_ALL,
            Fore.CYAN + "Priority" + Style.RESET_ALL,
            Fore.CYAN + "Status" + Style.RESET_ALL,
        ]
        status_format = {
            "complete": "🗹",
            "incomplete": "☐",
        }
        priority_format = {
            "low": Fore.GREEN + "low" + Style.RESET_ALL,
            "normal": Fore.YELLOW + "normal" + Style.RESET_ALL,
            "high": Fore.RED + "high" + Style.RESET_ALL,
        }
        # print(f"{self.title}")
        if self.num_of_tasks:
            return tabulate(
                [
                    [i, task.body, priority_format[task.priority], status_format[task.status]]
                    for i, task in enumerate(self.tasks, start=1)
                ],
                headers,
                tablefmt="mixed_grid",
                colalign=("left", "left", "center", "center"),
                maxcolwidths=[5, 120, 8, 10],
            )
        else:
            return tabulate(
                [headers],
                tablefmt="mixed_grid",
                colalign=("left", "left", "center", "center"),
                maxcolwidths=[5, 120, 8, 10],
            )

    def new_task(self, task):
        """
        Creates a new task inside the the current instance of the Note.
        Increases the self.num_of_notes by 1

        :param task: An object of the class Task
        :type task: Class Task
        """
        self.tasks.append(task)
        self.num_of_tasks = len(self.tasks)

class ToDo:
    def __init__(self, file_name):
        """
        Creates a new file or read the existing file (file_name) and initiate the engine for use of the ToDo class
        The object created loads all the notes and tasks from the file_name (or return an empty object is file_name do not exists)

        :param file_name: a string contain the file name to load or create a new file if does file_name does not exists
        :type file_name: str
        :raise ValueError: If the existing file_name does not follows the required csv format for this applications
        :return: An object of class ToDo. It contains all the notes an tasks that are saved in the file file_name
        :r type: class ToDo
        """
        self.file_name = file_name
        self.notes = {}
        if os.path.isfile(file_name):
            with open(file_name) as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 4:
                        raise ValueError(f"{file_name} curropted.")
                    else:
                        if row[0] in self.notes:
                            # check if a note with title in row[0] already exists in self.notes, if so add the current task in the row to it.
                            self.notes[row[0]].new_task(Task(row[1], row[2], row[3]))
                        else:
                            # note with title in row[0] does not exists in self.notes . We create a new Note with title row[0] and then add the current task to it.
                            self.notes[row[0]] = Note(row[0])
                            self.notes[row[0]].new_task(Task(row[1], row[2], row[3]))

        else:
            file = open(file_name, "a")
            file.close()

        self.num_of_notes = len(self.notes)
        self.current_note = list(self.notes.keys())[0] if self.num_of_notes else None
        self.is_saved = True

    def __str__(self):
        """
        Returns a string ready for use in print function.

        :return: Returns a string in the table format from all note title inside the ToDo object and all the the tasks inside the self.current_note
        :rtype: str
        """
        if self.num_of_notes:
            # tabulate note titles and distinguish current Note with color MAGENTA
            tabs = [
                Fore.MAGENTA + Style.BRIGHT + title + Style.RESET_ALL if self.current_note == title else title
                for title in self.notes.keys()
            ]

            return tabulate([tabs], tablefmt="simple_grid") + "\n" + str(self.notes[self.current_note])

        else:
            # There are no notes in the ToDo engine.
            return "There are no Notes. To create a new Note, use: note [note_title]"

    def new_note(self, title=""):
        '''
        If there is a note in self.notes with same title, switches the self.current_note to it,
        Othersie, creates a new note in the engine and change the self.current_note to it
        If title is not passed or title is empty string, generates an authomatic name for the title of the new note.

        :param title: A string containing the title of the new note
        :type title: str
        '''
        if title in self.notes.keys():
            self.current_note = title
        else:
            if not title:
                # if title is empty, creates a generic name for it
                i = 1
                while True:
                    if f"new_note_{i}" in self.notes.keys():
                        i += 1
                    else:
                        title = f"new_note_{i}"
                        break

            self.notes[title] = Note(title)
            self.num_of_notes = len(self.notes)
            self.current_note = title

    def new_task(self, **kwargs):
        '''
        Creates a new task for the self.notes[self.current_note]

        :param **kwargs: Named parametes with names body, priority and status
        :type **kwargs: str
        '''
        self.notes[self.current_note].new_task(Task(**kwargs))


    def save(self):
        '''
        Saves all the tasks of all the notes in self.notes inside the file self.file_name with csv format.

        '''
        with open(self.file_name, "w", newline="") as file:
            writer = csv.writer(file)
            for note in self.notes.values():
                for task in note.tasks:
                    writer.writerow([note.title, task.body, task.priority, task.status])
