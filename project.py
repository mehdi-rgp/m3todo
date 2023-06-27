from tabulate import tabulate
from pyfiglet import Figlet
import re
import sys
import os

# import todo Library
from todo import Task, Note, ToDo


def clear_screen():
    """
    Clears the screen
    """
    # for windows
    if os.name == "nt":
        _ = os.system("cls")
    # for mac and linux
    else:
        _ = os.system("clear")


def initiate():
    """
    This function prinits the welcome message and get the file_name from user

    :return: A string of the file name
    :rtype: str
    """
    figlet = Figlet()
    figlet.setFont(font="doom")
    print(figlet.renderText("M3 ToDo"))
    print("Created by Mehdi Rezagholipour")
    print("mehdi.rezagholipour@gmail.com\n\n")

    return get_file_name("Please insert your todo: ")


def get_file_name(s):
    """
    get input from user with message s.
    Extract file name from user input
    The file should be a valid csv file, but the use can pass the file name without .csv,
    i.e. use can input both file_name and file_name.csv and the function will extract file_name and return it.

    :param s: is the message that we want to be printed when prompting for user input
    :type s: str
    :return: a string contains file_name with .csv extension
    :rtype: str
    """
    while True:
        load_file = get_yes_no("Do you want to load an existing todo?")
        n = input(s)
        matches = re.search(r"^(.+?)(?:\.csv)?$", n, re.IGNORECASE)
        file_name = matches.group(1)

        if load_file:
            # when user wants to load a file
            if os.path.isfile(file_name + ".csv"):
                return f"{file_name}.csv"
            else:
                make_new_file = get_yes_no(
                    f"{file_name}.csv does not exists, do you want to create new file?"
                )
                if make_new_file:
                    return f"{file_name}.csv"

        else:
            # when user wants to create a new file
            if os.path.isfile(file_name + ".csv"):
                # check if the file_name.csv exists.
                # if exists, ask if user wants to load it
                load = get_yes_no(f"{file_name}.csv exists, do you want to load it?")
                if load:
                    return f"{file_name}.csv"
                else:
                    continue
            else:
                # this is if the file_name.csv do not exists.
                # check if the file_name is a valid system file name
                try:
                    # Here we check the file_name is a valid system file name, by trying to creating a new file
                    # If we get a system error, that means it is not a valid system file name.
                    # If file creation was susccessfull, we delete the file and return file_name.csv
                    file = open(f"{file_name}.csv", "w")
                    file.close()
                    os.remove(f"{file_name}.csv")
                    return f"{file_name}.csv"
                except OSError as e:
                    print(f"{file_name}.csv is not a valid file name. {e}")


def get_yes_no(yes_no_question):
    """
    Ask user a question and wait for a yes/no answer case insensitively
    If answer is not yes/no or y/n, repeats the qestion until answer is valid
    Returns True if the answr is yes or y
    Returns False if the answer is no or n

    :param yes_no_question: is the message tha will be printed when prompting for user input
    :type yes_no_question: str
    :return: A boolean, True for yes/y, False for No/n
    :rtype: bool
    """
    while True:
        answer = input(yes_no_question + " (yes/no or y/n) ").lower().strip()
        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False


def show(engine):
    """
    clears the screen and prints the engine

    :param engine: An object from the class ToDo
    :type engine: ToDo
    """
    clear_screen()
    print(engine)
    print("\n\n")


def get_command():
    """
    Get the input from user and checks if the first part of the input matches any of the predefined commands.
    Predefined commands are newtask, delete, task, note, save, exit and help

    :return: A tupple containing (command, args) command is the first of the user input. args is anything after that. args is None if there is nothing after first part.
    :rtype: tuple
    """
    while True:
        user_input = input(">> ").strip()
        if matches := re.search(
            r"^(newtask|delete|task|note|save|exit|help)( .+)?$", user_input
        ):
            command, args = matches.groups()
            return command, args

        else:
            print("Invalid command")


def newtask(engine, args):
    """
    get an object of class ToDo and creates a newtask under the current note with body in args

    :param engine: An object from the class ToDo
    :type engine: ToDo
    :param args: A string containing the body of the new task
    :type args: str
    :return: True if newtask was successful, False otherwise
    :rtype: bool
    """
    if args is None:
        return False
    else:
        print(args)
        print(len(args))
        engine.new_task(body=args.strip())
        return True


def delete(engine, args):
    """
    Deletes a note or a task based on what is in args
    If args is in the format of "note note_title": Deletes the note with title note_title
    If args is in the format of "task task_number": Deletes task number task_number


    :param engine: An object from the class ToDo
    :type engine: ToDo
    :param args: A string, which will be analysed if is in correct format.
    :type args: str
    :return: True if delete was successful, False otherwise
    :rtype: bool
    """
    if args is None:
        return False
    else:
        matches = re.search(r"^(task|note) (.+)", args.strip())
        if matches is None:
            return False
        arg1, arg2 = matches.groups()
        if arg2 is None:
            return False
        else:
            if arg1 == "task":
                try:
                    task_number = int(arg2.strip())
                except:
                    return False
                try:
                    del engine.notes[engine.current_note].tasks[task_number - 1]
                    return True
                except IndexError:
                    return False
            elif arg1 == "note":
                if arg2.strip() in engine.notes.keys():
                    del engine.notes[arg2.strip()]
                    # decreasing the number of notes by 1
                    engine.num_of_notes -= 1

                    if engine.num_of_notes:
                        # check if there is any notes left in the engine
                        if engine.current_note == arg2.strip():
                            # if we are deleteing the current_note, then the current_note should be changed, we set it to the first note
                            engine.current_note = list(engine.notes.keys())[0]
                    else:
                        engine.current_note = None
                    return True
                else:
                    return False


def task(engine, args):
    """
    This is for modifying a task's status, priority or body
    args should be in the format of :
        # priority [low|normal|high]
        # satus [complete|incomplete]
        # edit body
    where # should be the task_number

    :param engine: An object from the class ToDo
    :type engine: ToDo
    :param args: A string or None, which will be analysed if is in correct format.
    :type args: str
    :return: True if task operation was successful, False otherwise
    :rtype: bool
    """

    if args is None:
        return False
    if matches := re.search(r"^(\d+) (priority|status|edit) (.+)", args.strip()):
        task_number = int(matches.group(1).strip())
        stat = matches.group(3)
        if engine.notes[engine.current_note].num_of_tasks < task_number:
            return False
        if matches.group(2) == "status":
            try:
                engine.notes[engine.current_note].tasks[task_number - 1].status = stat
                return True
            except ValueError:
                return False
        elif matches.group(2) == "priority":
            try:
                engine.notes[engine.current_note].tasks[task_number - 1].priority = stat
                return True
            except ValueError:
                return False
        elif matches.group(2) == "edit":
            try:
                engine.notes[engine.current_note].tasks[task_number - 1].body = stat
                return True
            except ValueError:
                return False
    else:
        return False


def note(engine, args):
    """
    This is for creating a new note or switching the active note
    If args is None, creates a new note and generates an authomatic name
    If args is a string and there is no note with title=args, creates a new note with title=args
    If args is a string and there is a note with title=args, switches the active note to it.

    :param engine: An object from the class ToDo
    :type engine: ToDo
    :param args: A string or None, which will be analysed if is in correct format.
    :type args: str or None
    :return: True if note operation was successful, False otherwise
    :rtype: bool
    """
    if args is None:
        engine.new_note("")
    else:
        engine.new_note(args.strip())
    return True


def save(engine, args):
    """
    If used with no args, i.e. when args is None, saves the changes to te file

    :param engine: An object from the class ToDo
    :type engine: ToDo
    :param args: A string or None, which will be analysed if is in correct format.
    :type args: str or None
    :return: True if save operation was successful, False otherwise
    :rtype: bool
    """
    if args is None:
        try:
            engine.save()
            print("Saved successfull.")
            return True
        except:
            print("Save Error")
    return False


def exit(engine, args):
    """
    If used with no args, i.e. when args is None, exits the program.
    If there are any unsavesd changes in the object engine, prompt the user and asks if he/she wants to save first.

    :param engine: An object from the class ToDo
    :type engine: ToDo
    :param args: A string or None, which will be analysed if is in correct format.
    :type args: str or None
    :return: returns False if exit was unsuccessful
    :rtype: bool
    """
    if args is None:
        # check if the command exit is used with no arg
        if not engine.is_saved:
            # There are unsaved changes, ask the user if he/she wants to save before exit
            ifsave = get_yes_no("Do you want to save before exit?")
            if ifsave:
                save(engine, args)
        bye()
    else:
        # exit command is used with an argument. Invalid use, return false
        return False


def help(engine, args):
    """
    command: help [command]
    if a [command] is passed, shows help for that command.
    if the passed [command] does not exists or no [command] is passed, shows help for all functions

    :param engine: An object from the class ToDo. This is not used in this function, it is there for unification with other commands
    :type engine: ToDo
    :param args: A string or None, which will be analysed if is in correct format.
    :type args: str or None
    :return: Always returns True
    :rtype: bool
    """
    newtask_help = (
        "Command: newtask body:\n" "\tThis will add a new task under active note."
    )
    note_help = (
        "Command: note [note_title]:\n"
        "\tIf argument [note_title] is not passed creates a new note with an authomatic generated title.\n"
        "\tIf a note with title [note_title] already exists, changes the active note to the [note_title]. \n"
        "\tOtherwise creates a new note with title [note_title]"
    )
    task_help = (
        "Command: task n property value:\n"
        "\tn is the task number\n"
        "\tproperty must be one of the following: status, priority or edit\n"
        "\t\tstatus: if you want to change the status of the task\n"
        "\t\tpriority: if you want to change the priority of the task\n"
        "\t\tedit: if you want to edit the body of the task\n"
        "\tvalue: In case of status, it must be complete|incomplete. In case of priority, it can be low|normal|high"
    )
    delete_help = (
        "Command: delete object arg:\n"
        "\tIt can be used to delete a task or a note depending on the argument object, which can be task or note\n"
        "\tIf you want to delete a task arg should be the task number\n"
        "\tIf you want to delete a note, arg should be note title"
    )
    save_help = (
        "Command: save:\n" "\tUse with no argument to saves the changes on the file"
    )
    exit_help = "Command: exit:\n" "\tUse with no argument to exit from the program"

    function_help = {
        "newtask": newtask_help,
        "note": note_help,
        "task": task_help,
        "delete": delete_help,
        "save": save_help,
        "exit": exit_help,
    }
    # is args is None, change it to empty str
    args = args if args else ""
    if args.strip() not in function_help:
        for _ in function_help:
            print(function_help[_])
            print()
    else:
        print(function_help[args.strip()])
    return True


def bye():
    """
    Print goodbye message and exit the program
    """
    figlet = Figlet()
    figlet.setFont(font="doom")
    print(figlet.renderText("Stay organized, stay ahead!"))
    sys.exit()


def process(engine, command, args):
    """
    Runs the approperiate function based on the value in command

    :param engine: An object from the class ToDo
    :type engine: ToDo
    :param command: A string conaining one of the predefined functions
    :type command: str
    :param args: A string or None, which will be passed to approperiate function for further analysis
    :type args: str or None
    :return: returns True if function command was successful, False otherwise
    :rtype: bool
    """

    functions = {
        "newtask": newtask,
        "delete": delete,
        "task": task,
        "note": note,
        "save": save,
        "exit": exit,
        "help": help,
    }
    command_function = functions.get(command)
    return command_function(engine, args)


def run(engine):
    """
    This function continously gets input from user and run the approperiate command based on the user input.

    :param engine: An object from the class ToDo
    :type engine: ToDo
    """

    show(engine)
    while True:
        command, args = get_command()
        if process(engine, command, args):
            # process returns True if it was exceuted correctly
            if command not in ["help", "save", "exit"]:
                show(engine)

            if command == "save":
                # If the command was save, set engine.is_saved to True
                engine.is_saved = True
            elif command == "help":
                # If command was help, do not change the engine.is_saved
                pass
            else:
                # Change the engine.is_saved to False otherwise
                engine.is_saved = False
        else:
            # if process returns False, this means theres was something wrong with command, prints help for the command
            print("\nInvalid Command\n")
            help(engine, command)


def main():
    """
    It initiates the program,
    creates the engine, which is an object of class ToDo
    and then starts the run function
    """
    file_name = initiate()
    engine = ToDo(file_name)
    run(engine)


if __name__ == "__main__":
    main()
