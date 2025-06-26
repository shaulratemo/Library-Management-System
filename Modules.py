import mysql.connector
import random
import datetime


def generate_ticket_number():
    ticket_no = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    return ticket_no


class LibraryManager:
    """
    A class for managing users in the library database.
    """
    def __init__(self, host, user, password, database):
        """
        Initializes the connection to the library database.
        """
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def add_record(self, table_name):
        if table_name == 'members':
            mem_loop = 1
            while mem_loop == 1:
                full_name = input("Enter your name: ")
                user_name = input("Enter your username: ")
                m_query = "SELECT * FROM members WHERE username = %s"
                self.cursor.execute(m_query, (user_name,))
                m_result = self.cursor.fetchone()
                if m_result:
                    print(f"There already exists a member with username {user_name}. Please try again.")
                else:
                    e_mail = input("Enter your email: ")
                    password = input("Enter your password: ")
                    occupation = ''
                    my_loop = 1
                    while my_loop == 1:
                        print("Below are occupations.")
                        print("#1 Student")
                        print("#2 Lecturer")
                        choice_1 = int(input("Please select your occupation(Enter either 1 or 2): "))
                        if choice_1 == 1:
                            occupation = 'student'
                            my_loop = 0
                        elif choice_1 == 2:
                            occupation = 'lecturer'
                            my_loop = 0
                        else:
                            print("Invalid choice. Please try again!")
                    sql = "INSERT INTO members(full_name, username, email, member_password, member_type) " \
                          "VALUES(%s, %s, %s, %s, %s)"
                    self.cursor.execute(sql, (full_name, user_name, e_mail, password, occupation))
                    self.connection.commit()
                    print(f"User {user_name} was added successfully!")
                    mem_loop = 0
        elif table_name == 'books':
            """
            Adds a new book to the book table.
            """
            bk_loop = 1
            while bk_loop == 1:
                print("#*Please fill out the following fields*#")
                title = input("Book title: ")
                author = input("Author: ")
                isbn = input("ISBN number: ")
                bk_query = "SELECT * FROM books WHERE ISBN = %s"
                self.cursor.execute(bk_query, (isbn,))
                bk_result = self.cursor.fetchone()
                if bk_result:
                    print(f"There already exists a book with ISBN no. '{isbn}'. Please try again.")
                else:
                    category = input("Book category: ")
                    description = input("Book description: ")
                    copies = 0
                    loop_0 = 1
                    while loop_0 == 1:
                        copies = int(input("Number of available copies(Number should be greater than 0): "))
                        if copies < 1:
                            print("Invalid entry. Please try again!")
                        else:
                            loop_0 = 0
                    sql = "INSERT INTO books (book_title, author, ISBN, category, book_description, available_copies)" \
                          " VALUES (%s, %s, %s, %s, %s, %s)"
                    self.cursor.execute(sql, (title, author, isbn, category, description, copies))
                    self.connection.commit()
                    print(f"'{title}' book was added successfully!")
                    bk_loop = 0
        elif table_name == 'issues':
            loop_1 = 1
            while loop_1 == 1:
                name = input("Enter the name of the book you wish to borrow: ")
                query = "SELECT * FROM books WHERE book_title LIKE %s"
                self.cursor.execute(query, ("%" + name + "%",))
                # Fetch all the rows returned by the query
                books = self.cursor.fetchall()
                # Display the results
                if books:
                    loop_2 = 1
                    while loop_2 == 1:
                        print("Books containing '{}' in the title:".format(name))
                        print("{:<10} {:<40} {:<15} {:<20} {:<20} {:<35} {:<10}".format("ID", "Title", "Author", "ISBN",
                                                                                        "Category", "Description",
                                                                                        "Copies"))
                        print("-" * len(books) * 40)
                        for book in books:
                            print("{:<10} {:<40} {:<15} {:<20} {:<20} {:<35} {:<10}".format(book[0], book[1], book[2],
                                                                                            book[3], book[4], book[5],
                                                                                            book[6]))

                        bk_id = int(input("Enter the ID of the book you wish to borrow: "))
                        query_2 = "SELECT available_copies FROM books WHERE book_id = %s"
                        self.cursor.execute(query_2, (bk_id,))
                        id_result = self.cursor.fetchone()
                        if not id_result:
                            print(f"No books with ID '{bk_id}' found in the database. Please try again!")
                        elif id_result[0] > 0:
                            loop_2 = 0
                            loop_a = 1
                            while loop_a == 1:
                                name = input("Enter your username: ")
                                query_3 = "SELECT member_id FROM members WHERE username = %s"
                                self.cursor.execute(query_3, (name,))
                                nm_result = self.cursor.fetchone()
                                if nm_result:
                                    query_7 = "SELECT * FROM issues WHERE member_id = %s AND book_id = %s" \
                                              " ORDER BY due_date DESC LIMIT 1"
                                    self.cursor.execute(query_7, (nm_result[0], bk_id,))
                                    result_1 = self.cursor.fetchone()
                                    if not result_1:
                                        query_9 = "SELECT member_type FROM members WHERE member_id = %s"
                                        self.cursor.execute(query_9, (nm_result[0],))
                                        result_3 = self.cursor.fetchone()
                                        ticket_number = generate_ticket_number()
                                        from datetime import datetime, timedelta
                                        issue_date = datetime.now().date()
                                        due_date = issue_date + timedelta(days=10)
                                        if result_3[0] == 'lecturer':
                                            num = int(input("Please enter the number of copies you wish to borrow: "))
                                        else:
                                            num = 1
                                        query_4 = "SELECT available_copies FROM books WHERE book_id = %s"
                                        self.cursor.execute(query_4, (bk_id,))
                                        cp_result = self.cursor.fetchone()
                                        rem_copies = cp_result[0] - num
                                        query_5 = "UPDATE books SET available_copies = %s WHERE book_id = %s"
                                        self.cursor.execute(query_5, (rem_copies, bk_id,))
                                        self.connection.commit()
                                        query_6 = "INSERT INTO issues(issue_id, book_id, member_id, copies," \
                                                  " issue_date, due_date) VALUES(%s, %s, %s, %s, %s, %s)"
                                        self.cursor.execute(query_6, (ticket_number, bk_id, nm_result[0], num,
                                                                      issue_date, due_date))
                                        self.connection.commit()
                                        print(f"Book Issuance process was completed successfully. Your ticket number is"
                                              f" '{ticket_number}'")
                                        print(
                                            f"Your deadline for returning the book is '{due_date}'.\nPlease ensure you "
                                            f"return on or before the deadline.")
                                        print("Thank you for your time. Have a wonderful day!")
                                        loop_1 = 0
                                        loop_a = 0
                                    else:
                                        query_8 = "SELECT issue_id FROM issues WHERE member_id = %s AND book_id = %s" \
                                                  " AND return_date = NULL ORDER BY due_date DESC LIMIT 1"
                                        self.cursor.execute(query_8, (nm_result[0], bk_id,))
                                        result_2 = self.cursor.fetchone()
                                        if not result_2:
                                            print("There is a similar book that you have not returned yet.")
                                            print(
                                                "Please check back with us when you return the book to borrow"
                                                " it again.")
                                            print("Thank you for your time. Have a blessed day :)")
                                            loop_a = 0
                                            loop_1 = 0
                                        else:
                                            ticket_number = generate_ticket_number()
                                            from datetime import datetime, timedelta
                                            issue_date = datetime.now().date()
                                            due_date = issue_date + timedelta(days=10)
                                            query_4 = "SELECT available_copies FROM books WHERE book_id = %s"
                                            self.cursor.execute(query_4, (bk_id,))
                                            cp_result = self.cursor.fetchone()
                                            rem_copies = cp_result[0] - 1
                                            query_5 = "UPDATE books SET available_copies = %s WHERE book_id = %s"
                                            self.cursor.execute(query_5, (rem_copies, bk_id,))
                                            self.connection.commit()
                                            query_6 = "INSERT INTO issues(issue_id, book_id, member_id, issue_date, " \
                                                      "due_date) VALUES(%s, %s, %s, %s, %s)"
                                            self.cursor.execute(query_6,
                                                                (ticket_number, bk_id, nm_result[0], issue_date,
                                                                 due_date))
                                            self.connection.commit()
                                            print(
                                                f"Book Issuance process was completed successfully. "
                                                f"Your ticket number is '{ticket_number}'")
                                            print(f"Your deadline for returning the book is '{due_date}'.\n"
                                                  f"Please ensure you return on or before the deadline.")
                                            print("Thank you for your time. Have a wonderful day!")
                                            loop_a = 0
                                            loop_1 = 0

                                elif not nm_result:
                                    print(f"There is no member with username '{name}' in the members table.")
                                    loop_1 = 1
                                    while loop_1 == 1:
                                        print("#1 Try again")
                                        print("#2 Join our membership")
                                        us_choice = int(input("Select your option(1 0r 2): "))
                                        if us_choice == 1:
                                            loop_a = 1
                                            loop_1 = 0
                                        elif us_choice == 2:
                                            loop_a = 0
                                            loop_1 = 0
                                            # Here I will call the function for creating a new member
                                        else:
                                            print("Invalid input! Please try again.")
                        elif id_result[0] == 0:
                            print(f"There are no other copies available for borrowing for book with ID {bk_id}!")
                            loop_2 = 0
                            loop_3 = 1
                            while loop_3 == 1:
                                print("#1 Choose another book.")
                                print("#2 Come back later.")
                                your_choice = int(input("Your choice(1 or 2): "))
                                if your_choice == 1:
                                    loop_3 = 0
                                elif your_choice == 2:
                                    print("Thank you for your time. Have a nice day :)")
                                    loop_3 = 0
                                    loop_1 = 0
                                else:
                                    print("Invalid choice! Please try again.")
                elif not books:
                    print(f"No books found containing '{name}' phrase in the title. Please try again!")

    def update_record(self, table_name):
        if table_name == 'members':
            n_loop = 1
            while n_loop == 1:
                user_name = input("Enter your username: ")
                sql = f"SELECT member_id FROM members WHERE username = '{user_name}'"
                self.cursor.execute(sql)
                user_result = self.cursor.fetchone()
                if user_result:
                    print("Below are fields that you can modify")
                    print("#1 full name")
                    print("#2 username")
                    print("#3 e-mail")
                    print("#4 password")
                    choice_1 = int(input("Select the choice_1 you wish to modify(Example: 1): "))
                    updates = []
                    if choice_1 == 1:
                        name = input("Enter the new name(full name): ")
                        updates.append(f"full_name = '{name}'")
                    elif choice_1 == 2:
                        user_name = input("Enter the username: ")
                        updates.append(f"username = '{user_name}'")
                    elif choice_1 == 3:
                        e_mail = input("Enter the new E-mail: ")
                        updates.append(f"email = '{e_mail}'")
                    elif choice_1 == 4:
                        passwd = input("Briefly enter the new passwd: ")
                        updates.append(f"member_password = '{passwd}'")
                    elif not updates:
                        print("No update values were provided!")
                        return
                    n_loop = 0

                    update_str = ", ".join(updates)
                    sql = f"UPDATE members SET {update_str} WHERE member_id = {user_result[0]}"
                    self.cursor.execute(sql)
                    self.connection.commit()
                    print(f"Member '{user_name}' updated successfully!")

                if not user_result:
                    m_loop = 1
                    while m_loop == 1:
                        print(f"The member '{user_name}' could not be found or does not exist!")
                        print("#1 Try again")
                        print("#2 Join membership")
                        m_choice = int(input("Select your option(1 or 2): "))
                        if m_choice == 1:
                            m_loop = 0
                            continue
                        elif m_choice == 2:
                            library_manager.add_record('members')
                            m_loop = 0
                            n_loop = 0
                        else:
                            print("Invalid b_choice. Please try again!")
        elif table_name == 'books':
            b_loop = 1
            while b_loop == 1:
                isbn = input("Enter the ISBN of the book: ")
                sql = f"SELECT book_id FROM books WHERE ISBN = '{isbn}'"
                self.cursor.execute(sql)
                user_result = self.cursor.fetchone()
                if user_result:
                    print("Below are fields of the book that you can modify")
                    print("#1 Book Title")
                    print("#2 Author")
                    print("#3 ISBN")
                    print("#4 Category")
                    print("#5 Description")
                    print("#6 Copies")
                    b_choice = int(input("Select the b_choice you wish to modify(Example: 1): "))
                    updates = []
                    if b_choice == 1:
                        title = input("Enter the new title: ")
                        updates.append(f"book_title = '{title}'")
                    elif b_choice == 2:
                        author = input("Enter the author's name: ")
                        updates.append(f"author = '{author}'")
                    elif b_choice == 3:
                        isbn_no = input("Enter the new ISBN number: ")
                        updates.append(f"ISBN = '{isbn_no}'")
                    elif b_choice == 4:
                        cat = input("Enter the new book category: ")
                        updates.append(f"category = '{cat}'")
                    elif b_choice == 5:
                        bk_desc = input("Briefly enter the new book description: ")
                        updates.append(f"book_description = '{bk_desc}'")
                    elif b_choice == 6:
                        av_copies = input("Enter the new value of copies: ")
                        updates.append(f"available_copies = {av_copies}")
                    elif not updates:
                        print("No update values were provided!")
                        return

                    update_str = ", ".join(updates)
                    sql = f"UPDATE books SET {update_str} WHERE book_id = {user_result[0]}"
                    self.cursor.execute(sql)
                    self.connection.commit()
                    print(f"The book with ID '{user_result[0]}' was updated successfully!")
                    b_loop = 0

                if not user_result:
                    print(f"The book with ID '{user_result[0]}' could not be found or does not exist!")
                    print("Please try again.\n")

    def display_record(self, table_name):
        if table_name == 'books':
            c_loop = 1
            while c_loop == 1:
                print("#1 Show the entire table")
                print("#2 Show a particular record")
                selection = int(input("Please select your option(1 or 2): "))
                if selection == 1:
                    # Count all rows
                    sql_count = f"SELECT COUNT(*) FROM books"
                    self.cursor.execute(sql_count)
                    # Fetch the result (should be a single row with one element)
                    my_count = self.cursor.fetchone()[0]
                    self.connection.commit()
                    if not my_count:
                        print(f"There is no data inserted in the books table yet!")
                        c_loop = 0
                    else:
                        sql_1 = f"SELECT book_id FROM books ORDER BY book_id ASC LIMIT 1"
                        self.cursor.execute(sql_1)
                        start_result = self.cursor.fetchone()
                        start_value = start_result[0]
                        sql_0 = f"SELECT book_id FROM books ORDER BY book_id DESC LIMIT 1"
                        self.cursor.execute(sql_0)
                        end_result = self.cursor.fetchone()
                        end_value = end_result[0]
                        for i in range(start_value, end_value + 1):
                            sql_select = f"SELECT * FROM books WHERE book_id = %s"
                            self.cursor.execute(sql_select, (i,))
                            product_result = self.cursor.fetchone()

                            if product_result is None:
                                continue  # Skip to the next iteration if no row is fetched

                            # Check if product_result is an integer
                            if isinstance(product_result, int):
                                product_result = (product_result,)  # Convert the integer to a tuple

                            # Continue with the rest of the code to format and print the row
                            # Get column names
                            column_names = [column[0] for column in self.cursor.description]

                            if i == start_value:
                                print(f"\nData from table: 'books'\n")
                                # Print column names as headers
                                print(" ".join([f"{name:^24}" for name in column_names]))
                                print("=" * (len(column_names) * 25))

                            # Fetch all rows and print them in a formatted way
                            formatted_row = [str(element).center(24) for element in product_result]
                            print(" ".join(formatted_row))
                            print("-" * (len(column_names) * 25))
                        c_loop = 0
                        self.connection.commit()

                elif selection == 2:
                    m_id = int(input("Please enter the id of the data you wish to view: "))
                    sql = f"SELECT * FROM books WHERE book_id = %s"
                    self.cursor.execute(sql, (m_id,))
                    purchase_result = self.cursor.fetchall()
                    if purchase_result:
                        # Get column names
                        column_names = [column[0] for column in self.cursor.description]
                        print(f"\nData from table: books\n")

                        # Print column names as headers
                        print(" ".join([f"{name:^24}" for name in column_names]))
                        print("=" * (len(column_names) * 25))

                        # Fetch all rows and print them in a formatted way
                        for row in purchase_result:
                            # Format each row element for better readability
                            formatted_row = [str(element).center(24) for element in row]
                            print(" ".join(formatted_row))
                            print("-" * (len(column_names) * 25))
                        self.connection.commit()
                        c_loop = 0
                    elif not purchase_result:
                        print(f"The books record with ID book_id could not be found or does not exist!")

                else:
                    print("Invalid i_choice. Please try again!")
        elif table_name == 'issues':
            loop_1 = 1
            while loop_1 == 1:
                print("#1 Display the entire table")
                print("#2 Display a particular table")
                i_choice = int(input("Select your i_choice(Press 1 or 2): "))
                if i_choice == 1:
                    query = "SELECT * FROM issues"
                    self.cursor.execute(query)
                    rows = self.cursor.fetchall()
                    sorted_data = sorted(rows, key=lambda x: datetime.datetime.strptime(str(x[3]), '%Y-%m-%d'))
                    print("{:<15} {:<10} {:<10} {:<15} {:<15} {:<15}".format("issue_id", "book_id", "member_id",
                                                                             "issue_date", "due_date", "return_date"))
                    print("=" * 90)
                    for row in sorted_data:
                        formatted_row = []
                        for item in row:
                            if item is None:
                                formatted_row.append("NULL")
                            elif isinstance(item, datetime.date):  # Check if the item is a date object
                                formatted_row.append(item.strftime('%Y-%m-%d'))  # Format date as YYYY-MM-DD

                            else:
                                formatted_row.append(item)
                        print("{:<15} {:<10} {:<10} {:<15} {:<15} {:<15}".format(*formatted_row))
                        print("-" * 90)
                    self.connection.commit()
                    loop_1 = 0
                elif i_choice == 2:
                    loop_2 = 1
                    while loop_2 == 1:
                        issue_id = input("Enter the ID of the data you wish to display: ")
                        query = "SELECT * FROM issues WHERE issue_id = %s"
                        self.cursor.execute(query, (issue_id,))
                        rows = self.cursor.fetchall()
                        if rows:
                            sorted_data = sorted(rows, key=lambda x: datetime.datetime.strptime(str(x[3]), '%Y-%m-%d'))
                            print("{:<15} {:<10} {:<10} {:<15} {:<15} {:<15}".format("issue_id", "book_id", "member_id",
                                                                                     "issue_date",
                                                                                     "due_date", "return_date"))
                            print("=" * 90)
                            for row in sorted_data:
                                formatted_row = []
                                for item in row:
                                    if item is None:
                                        formatted_row.append("NULL")
                                    elif isinstance(item, datetime.date):  # Check if the item is a date object
                                        formatted_row.append(item.strftime('%Y-%m-%d'))  # Format date as YYYY-MM-DD

                                    else:
                                        formatted_row.append(item)
                                print("{:<15} {:<10} {:<10} {:<15} {:<15} {:<15}".format(*formatted_row))
                                print("-" * 90)
                            self.connection.commit()
                            loop_2 = 0
                        elif not rows:
                            print(f"There is no data found with ID {issue_id}. Please try again.")
                        loop_1 = 0
                else:
                    print("Invalid i_choice! Please try again.")

    def delete_record(self, table_name):
        if table_name == 'members':
            """
            Removes a member from the library table.
            """
            mm_loop = 1
            while mm_loop == 1:
                mem_name = input("Enter the username of the member you wish to remove: ")
                msql = f"SELECT member_id FROM members WHERE username = %s"
                self.cursor.execute(msql, (mem_name,))
                pr_result = self.cursor.fetchone()
                if pr_result:
                    query = "SELECT * FROM issues WHERE member_id = %s ORDER BY issue_date DESC LIMIT 1"
                    self.cursor.execute(query, (pr_result[0],))
                    result = self.cursor.fetchone()
                    if not result[6]:
                        print(f"There is a book you were issued under ID {result[0]} that you have not yet returned.")
                        print("Please ensure you return the book so before you undertake this operation!")
                        mm_loop = 0
                    else:
                        sql = f"SELECT * FROM members WHERE username = %s"
                        self.cursor.execute(sql, (mem_name,))
                        mem_result = self.cursor.fetchall()
                        # Get column names
                        column_names = [column[0] for column in self.cursor.description]
                        print(f"\nData from table: books\n")

                        # Print column names as headers
                        print(" ".join([f"{name:^24}" for name in column_names]))
                        print("=" * (len(column_names) * 25))

                        # Fetch all rows and print them in a formatted way
                        for row in mem_result:
                            # Format each row element for better readability
                            formatted_row = [str(element).center(24) for element in row]
                            print(" ".join(formatted_row))
                            print("-" * (len(column_names) * 25))
                        self.connection.commit()
                        us_loop = 1
                        while us_loop == 1:
                            del_choice = int(input(f"Are you sure you wish to delete the data with ID {pr_result[0]}?"
                                                   f"(If yes press 1 if No press 0): "))
                            if del_choice == 1:
                                sql = f"DELETE FROM members WHERE member_id = {pr_result[0]}"
                                self.cursor.execute(sql)
                                self.connection.commit()
                                print(f"Member {mem_name} was deleted successfully!")
                                us_loop = 0
                                mm_loop = 0
                            elif not del_choice:
                                print("Delete procedure was cancelled successfully!")
                                us_loop = 0
                                mm_loop = 0
                            else:
                                print("Invalid choice. Please try again!")
                elif not pr_result:
                    m_loop = 1
                    while m_loop == 1:
                        print(f"The member with username {mem_name} could not be found or does not exist!\n")
                        print("#1 Try again")
                        print("#2 Join membership")
                        m_choice = int(input("Select your option(1 or 2): "))
                        if m_choice == 1:
                            m_loop = 0
                            continue
                        elif m_choice == 2:
                            library_manager.add_record('members')
                            m_loop = 0
                            mm_loop = 0
                        else:
                            print("Invalid choice. Please try again!")
        elif table_name == 'books':
            """
            Deletes a book from the books table.
            """
            my_loop = 1
            while my_loop == 1:
                isbn = input("Enter the ISBN number of the book you wish to remove: ")
                msql = f"SELECT book_id FROM books WHERE ISBN = %s"
                self.cursor.execute(msql, (isbn,))
                pr_result = self.cursor.fetchone()
                if pr_result:
                    sql = f"SELECT * FROM books WHERE ISBN = %s"
                    self.cursor.execute(sql, (isbn,))
                    bk_result = self.cursor.fetchall()
                    # Get column names
                    column_names = [column[0] for column in self.cursor.description]
                    print(f"\nData from table: books\n")

                    # Print column names as headers
                    print(" ".join([f"{name:^24}" for name in column_names]))
                    print("=" * (len(column_names) * 25))

                    # Fetch all rows and print them in a formatted way
                    for row in bk_result:
                        # Format each row element for better readability
                        formatted_row = [str(element).center(24) for element in row]
                        print(" ".join(formatted_row))
                        print("-" * (len(column_names) * 25))
                    self.connection.commit()
                    p_loop = 1
                    while p_loop == 1:
                        del_choice = int(
                            input(f"Are you sure you wish to remove the book with ID {pr_result[0]}?(If yes "
                                  f"press 1 if No press 0): "))
                        if del_choice == 1:
                            sql = f"DELETE FROM books WHERE book_id = {pr_result[0]}"
                            self.cursor.execute(sql)
                            self.connection.commit()
                            print(f"The book with ID {pr_result[0]} was deleted successfully!")
                            p_loop = 0
                        elif not del_choice:
                            print("Delete procedure was cancelled successfully!")
                            p_loop = 0
                        else:
                            print("Invalid choice. Please try again!")
                    my_loop = 0
                elif not pr_result:
                    print(f"The book with ISBN number {isbn} could not be found or does not exist!\n")

    def book_return(self):
        s_loop = 1
        while s_loop == 1:
            name = input("Enter the username of the member returning the book: ")
            bk_no = int(input("Enter the book ID of the book being returned: "))
            query = "SELECT member_id FROM members WHERE username = %s"
            self.cursor.execute(query, (name,))
            mem_result = self.cursor.fetchone()
            if mem_result:
                query_1 = "SELECT issue_id FROM issues WHERE member_id = %s AND book_id = %s"
                self.cursor.execute(query_1, (mem_result[0], bk_no,))
                res = self.cursor.fetchone()
                if res:
                    query_2 = "UPDATE issues SET return_date = %s WHERE issue_id = %s"
                    from datetime import datetime, timedelta
                    return_date = datetime.now().date()
                    self.cursor.execute(query_2, (return_date, res[0],))
                    self.connection.commit()
                    query_3 = "SELECT copies FROM issues WHERE issue_id = %s"
                    self.cursor.execute(query_3, (res[0]))
                    copies_res = self.cursor.fetchone()
                    query_4 = "SELECT book_id FROM issues WHERE issue_id = %s"
                    self.cursor.execute(query_4, (res[0],))
                    id_result = self.cursor.fetchone()
                    query_5 = "SELECT available_copies FROM books WHERE book_id = %s"
                    self.cursor.execute(query_5, (id_result[0],))
                    copies = self.cursor.fetchone()
                    new_copies = copies[0] + copies_res[0]
                    query_6 = "UPDATE books SET available_copies = %s WHERE book_id = %s"
                    self.cursor.execute(query_6, (new_copies, id_result[0],))
                    print(f"Process completed. The book under issue ID '{res[0]}' has been returned successfully.")
                    print("Thank you for your time. Have a lovely day!")
                    s_loop = 0
                elif not res:
                    print(f"There is no record with book ID {bk_no} under {name}. Please try again!")
            elif not mem_result:
                print(f"The record of {name} does not exist. Please try again!")

    def close_connection(self):
        """
        Closes the connection to the MySQL database.
        """
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    library_manager = LibraryManager(
        host="localhost",
        user="root",
        password="jeanette",
        database="library"
    )

    loop = 1
    while loop == 1:
        print("************Welcome to the Library Management System************")
        print("Here are the tables available for modifications")
        print("#1 Members table")
        print("#2 Books table")
        print("#3 Issues table")
        print("#0 End program")
        choice = int(input("Select the table you wish to execute: "))

        if choice == 1:
            prod_loop = 1
            while prod_loop == 1:
                print("The members table has the following functions:")
                print("#1 Add a new member")
                print("#2 Modify an existing member")
                print("#3 Delete a member")
                print("#0 Return to home page")
                prod_choice = int(input("Select the action you wish to undertake(Example: 1, 2 or 3): "))
                if not prod_choice:
                    print("Thank you for using the Members module!")
                    prod_loop = 0
                elif prod_choice == 1:
                    library_manager.add_record('members')
                elif prod_choice == 2:
                    library_manager.update_record('members')
                elif prod_choice == 3:
                    library_manager.delete_record('members')
                else:
                    print("Invalid choice. Please try again!")
        elif choice == 2:
            book_loop = 1
            while book_loop == 1:
                print("The books table has the following functions:")
                print("#1 Add a new book")
                print("#2 Display books in the library")
                print("#3 Edit book details")
                print("#4 Remove a book from the library")
                print("#0 Return to home page")
                bk_choice = int(input("Select the choice you wish to undertake(1 or 2): "))
                if not bk_choice:
                    print("Thank you for interacting with the Books module!")
                    book_loop = 0
                elif bk_choice == 1:
                    library_manager.add_record('books')
                elif bk_choice == 2:
                    library_manager.display_record('books')
                elif bk_choice == 3:
                    library_manager.update_record('books')
                elif bk_choice == 4:
                    library_manager.delete_record('books')
                else:
                    print("Invalid choice. Please try again!")
        elif choice == 3:
            iss_loop = 1
            while iss_loop == 1:
                print("The issues table has the following functions:")
                print("#1 Record an issued book")
                print("#2 Record a returned book")
                print("#3 Display book issuance records")
                print("#0 Return to home page")
                is_loop = int(input("Select the choice you wish to undertake(1 or 2): "))
                if not is_loop:
                    print("Thank you for capitalizing on the Book Issuance module!")
                    iss_loop = 0
                elif is_loop == 1:
                    library_manager.add_record('issues')
                elif is_loop == 2:
                    library_manager.book_return()
                elif is_loop == 3:
                    library_manager.display_record('issues')
                else:
                    print("Invalid choice. Please try again!")
        elif not choice:
            print("Thank you for your time!")
            print("***********************Program Terminated**********************")
            library_manager.close_connection()
            loop = 0
