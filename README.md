# Simple Todo Application
#### Video Demo: [CS50’s Introduction to Programming with Python - Final Project](https://youtu.be/Ixq3d5N1Rew)
#### Description:
This is a simple todo application which runs inside the terminal.
The application can save the todo in a csv file.
The file can be loaded for later uses.

To start of the program, simply type `python project.py` in the terminal. The program will start and asks the user if he/she wants to create an new empty workspace or wants to load an existing workspace from a _.csv_ file.

Then, the program will show the existing notes and highlights the active note with magenta color and shows all the tasks within active note.

Then the programs shows `>>` and waits for the user commands.


## classes
The classess are defined in the _todo.py_ file.
## 1. calss Task:
This class creates an object that mimics a specific task
### attributes:
1. **body**: _str_\
Contains the body of the task
2. **priority**: _str_\
Can be low, normal or high \
3. **status**: _str_\
Can be complete or incomplete

### methods:
1. \__init__ 
2. \__str__

## 2. class Note
This class creates an object that can containes tasks.\
This object is created to give us the ability to create different categories of tasks.

### attributes:
1. **num_of_tasks**: _int_
2. **tasks**: _list_
3. **title**: _str_

### methods:
1. __init__
2. __str__
3. **newtask**:\
creates a new task inside the note

## 3. class ToDo
This class is the heart of the program. It creates a engine that contains all the information inside your todo workspace including all the notes and the tasks of each note.
### attributes:
1. **file_name**: _str_
2. **notes**: _dictionary_\
{note_title : Note}
3. **num_of_notes**: _int_
4. **current_note**: _str_
5. **is_saved**: _bool_\
Is _Ture_ if all changes are saved in the file **file_name**, otherewise _False_
### methods:
1. **init**
2. **str**
3. **new_note**\
Creates a new note in the workspace
4. **new_task**\
Creates a new task within the note with the title of **current_note**
5. **save**\
Saves all the notes and tasks inside the file **file_name**


# main code
the _project.py_ file contains the main code that runs the program with the help of classess defined.
after running the program, it prompt the user for the data file and then waits for the use commands.

## Availabale commands
1. help
2. note
3. newtask
4. task
5. delete
6. save
7. exit

### 1. help
To access help of any command, simply type `help [command]` and hit enter.
If a commad is used with wrong syntax, it will shows the help of that command.
If `help` is used with no argument or is used with a wrong command, it will show the help for all the available commands.

### 2. note
`note` is used to create a new note or switch the active note.\
Syntaxt: `note note_title`\
If used with no argument, it creates a new note with an authomatic generated title.\
If used with an argument, the argument is title of the note.\
If the title already exits, it switched the active note, otherwise it creates a new note with that title.

### 3. newtask
Syntax: `newtask body`\
Creates a task within active note.

### 4. task
This command is used to edit the body, priority and the status of a task.\
Syntaxt: `task n property value`\
`n` is the task number.\
`property` must be one of the following: `status`, ``priority`` or ``edit``\
``status``: if you want to change the status of the task\
``priority``: if you want to change the priority of the task\
``edit``: if you want to edit the body of the task\
``value``: In case of status, it must be ``complete``|``incomplete``. In case of priority, it can be ``low``|``normal``|``high``


### 5. delete
It can be used to delete a task or a note.\
Syntax: `delete object arg`\
`object` can be either `note` or `task`.\
If you want to delete a task ``arg`` should be the task number.\
If you want to delete a note, ``arg`` should be note title.

### 6. save
Syntax: ``save``\
Use with no argument to saves the changes on the file.


### 7. exit
Syntax: ``exit``\
Use with no argument to exit from the program