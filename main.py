import function

function.create_table()

print('\nThis is test message')
while True:

    print('\n0 - END\n1 - Add task\n2 - Show all tasks\n3 - Update task\n4 - Delete task')
    choice = int(input('\n-> '))

    if choice == 0:
        function.con.close()
        break

    if choice == 1:
        function.add_task()

    if choice == 2:
        function.show_all_task()

    if choice == 3:
        function.update_task()

    if choice == 4:
        function.delete_task()

    if choice == 919:
        function.delete_database()
        break