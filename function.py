import sqlite3
import os
import datetime

db = 'TODO'+'.db'
con = sqlite3.connect(db)
cur = con.cursor()
statusList = ['ToDo', 'Inprogress', 'Done']

def create_table():
    initComand = """
                BEGIN;

                PRAGMA foreign_keys = ON;

                CREATE TABLE IF NOT EXISTS status (
                    id                     INTEGER      PRIMARY KEY,
                    status              TEXT
                    );

                CREATE TABLE IF NOT EXISTS tasks (
                    id                     INTEGER     PRIMARY KEY,
                    task_name       TEXT,
                    create_date     TEXT,
                    deadline          TEXT,
                    task_status_id   INTEGER    NOT NULL,
                    FOREIGN KEY (task_status_id)
                    REFERENCES status (id)
                    );

                COMMIT;
                """

    showAllStatusComand = """SELECT * FROM status"""

    cur.executescript(initComand)

    res = cur.execute(showAllStatusComand)
    if len(res.fetchall()) == 0:
        cur.executemany("""INSERT INTO status VALUES(?,?)""", enumerate(statusList, start=1))
        con.commit()


def add_task():
    # ENETR TASK NAME
    print('Enter task name: ')
    taskName = input(">>> ")

    # ENTER DEADLINE
    while True:
        print('Enter task deadline (YYYY-MM-DD): ')
        taskDeadLine = datetime.date.fromisoformat(input(">>> "))
        if datetime.date.today() <= taskDeadLine:
            break
        else:
            print('Enter correct date !')

    # ENTER TASK STATUS
    while True:
        print('Chose task status: ')
        nStatus = 0
        for id, status in cur.execute("""SELECT * FROM status"""):
            print(f'{id} - {status}')
            nStatus = id

        taskState = int(input(">>> "))
        if taskState in range(1,nStatus +1):
            break
        else:
            print("Chose correct task status !")

    # INSERT TASK TO DATABASE
    cur.execute("INSERT INTO tasks (task_name, create_date, deadline, task_status_id) VALUES (?,?,?,?)",
                (taskName, datetime.date.today(), taskDeadLine, taskState))
    con.commit()


def show_all_task():
    showAllTaskComand = """
    SELECT
            t1.id,
            t1.task_name,
            t1.create_date,
            t1.deadline,
            t2.status
    FROM tasks AS t1
    LEFT JOIN status AS t2 ON t1.task_status_id = t2.id

    """

    print("Tasks")
    print('{:^4} | {:^50} | {:^12} | {:^12} | {:^12}'.format('ID', 'Task name', 'Create date', 'Deadline', 'Status'))
    print('-'*5,'+','-'*52,'+','-'*14,'+','-'*14,'+','-'*14, sep='')

    for id, taskName, createDate, deadline, status in cur.execute(showAllTaskComand):
        print(f'{id:^4} | {taskName:<50} | {createDate:^12} | {deadline:^12} | {status:<12}')
    print('\n')



def update_task():
    #TODO:
    print('Task ID for update:')
    taskIdForUpdate = int(input('>>> '))

    print('New value:')
    newValue = int(input('>>> '))

    columnToUpdate = 'task_status_id'

    updateComand = f'''UPDATE tasks SET {columnToUpdate} = {newValue} WHERE id == {taskIdForUpdate}'''

    cur.execute(updateComand)
    con.commit()

    print("UPDATED")


def delete_task():
    #TODO:
    print('Enter task ID to delete: ')
    taskIdToDelete = int(input(">>> "))
    cur.execute("DELETE FROM tasks WHERE id == ?", (taskIdToDelete,))
    con.commit()
    print('DELETED')


def delete_database():
    con.close()
    if os.path.exists(db):
        os.remove(db)
