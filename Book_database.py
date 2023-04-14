# Import statements
# Create database and cursor
import sqlite3
db = sqlite3.connect('ebookstore')
cr = db.cursor()

# Empty lists for adding books into
book_list = []
id_list = []
title_list = []
author_list = []
qty_list = []


# Function to add books to table from txt if first run
def register_books():
    # Opens txt file with book inventory and formats it
    with open('books_inventory.txt', 'r') as books:

        for line in books:
            line_strip = line.strip("\n").split("-")
            book_list.append(line_strip)
        #print(line_strip[0])

        del book_list[0]    # Deletes row 1 with headers

        # Adds ids, titles, authors and quantities to lists
        for x in range(len(book_list)):
            ids = int(book_list[x][0])
            id_list.append(ids)

            titles = book_list[x][1]
            title_list.append(titles)

            authors = book_list[x][2]
            author_list.append(authors)

            qts = int(book_list[x][3])
            qty_list.append(qts)

        # Inserts into table the ids, titles, authors and quantities from txt file
        try:
            for i in range(len(book_list)):
                cr.execute('''
            INSERT INTO books(id, Title, Author, Qty) VALUES(?, ?, ?, ?)''',
                           (id_list[i], title_list[i], author_list[i], qty_list[i]))

        except Exception as exc:
            raise exc

        finally:
            db.commit()
            return


# Menu function
def menu():
    while True:
        # Variable storing choice of options
        choice = input("Menu:"
                       "\nAdd a book === '1'"
                       "\nUpdate book Qty === '2'"
                       "\nDelete Book === '3'"
                       "\nSearch Book === '4'"
                       "\nExit === '0'"
                       "\n---> ")
    
        # Carries out specific functions related to user choice
        if choice == "1":
            add_book()
    
        elif choice == "2":
            update()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_book()
        elif choice == "0":
            exit()
    
        else:
            print("Incorrect input ...")    # If input is not recognized ...


# Function to add book
def add_book():
    # Save title, author and qty in variables
    new_title = input("Book Title: ")
    new_author = input("Author: ")
    new_qty = int(input("Quantity: "))

    # Insert book into books table
    cr.execute('''
    INSERT INTO books(Title, Author, Qty) VALUES (?, ?, ?)''', (new_title, new_author, new_qty))
    db.commit()
    print("Book Added")


# Function for updating qty
def update():
    # Option to select book by author or title
    selection = input("\nSelect book by:"
                      "\nTitle === '1'"
                      "\nAuthor === '2'"
                      "\n---> ")
    # if title selected; enter book title, select book in table and print book details
    # Ask for new qty, update book qty
    # Print book with updated details
    if selection == "1":
        book_select = input("\nEnter book title: ")
        cr.execute('''
        SELECT Title, Author, Qty FROM books WHERE Title = ?''', (book_select,))
        book = cr.fetchone()
        print(book)
        updated_qty = int(input("New Quantity: "))
        cr.execute('''
        UPDATE books SET Qty = ? WHERE Title = ?''', (updated_qty, book_select))
        db.commit()
        print("\nQuantity updated")

        cr.execute('''
        SELECT Title, Author, Qty FROM books WHERE Title = ?''', (book_select,))
        book = cr.fetchone()
        print(book)

    # if author selected; enter book author, select book in table and print book details
    # Ask for new qty, update book qty
    # Print book with updated details
    elif selection == "2":
        book_select = input("\nEnter book author: ")
        cr.execute('''
        SELECT Title, Author, Qty FROM books WHERE Author = ?''', (book_select,))
        book = cr.fetchone()
        print(book)
        updated_qty = int(input("New Quantity: "))
        cr.execute('''
        UPDATE books SET Qty = ? WHERE Author = ?''', (updated_qty, book_select))
        db.commit()
        print("\nQuantity updated")

        cr.execute('''
        SELECT Title, Author, Qty FROM books WHERE Author = ?''', (book_select,))
        book = cr.fetchone()
        print(book)

    # Else if unrecognized input
    else:
        print("Incorrect input ...")


# Function to delete book
def delete_book():
    # Option to select book by author or title
    selection = input("\nSelect book by:"
                      "\nTitle === '1'"
                      "\nAuthor === '2'"
                      "\n---> ")
    # if title selected; enter book title, select book in table and print book details
    # delete book
    if selection == "1":
        book_select = input("\nEnter book title: ")
        cr.execute('''
            SELECT Title, Author, Qty FROM books WHERE Title = ?''', (book_select,))
        book = cr.fetchone()
        print(book)

        # Confirm deletion
        confirm = input("Delete this book? (Y)yes / (N)no: ").upper()
        if confirm == "Y":
            cr.execute('''
            DELETE FROM books WHERE Title = ?''', (book_select,))
            db.commit()
            print("Book entry deleted")
        # If No, rerun function
        else:
            delete_book()

    # if author selected; enter book author, select book in table and print book details
    # Delete book
    elif selection == "2":
        book_select = input("\nEnter book author: ")
        cr.execute('''
        SELECT Title, Author, Qty FROM books WHERE Author = ?''', (book_select,))
        book = cr.fetchone()
        print(book)

        # Confirm deletion
        confirm = input("Delete this book? (Y)yes / (N)no: ").upper()
        if confirm == "Y":
            cr.execute('''
                    DELETE FROM books WHERE Author = ?''', (book_select,))
            db.commit()
            print("Book entry deleted")
        # If No, rerun function
        else:
            delete_book()

    # For unrecognized input
    else:
        print("Incorrect input ...")


# Function for searching
def search_book():
    # Option to select book by title, author or id
    selection = input("\nSearch book by:"
                      "\nTitle === '1'"
                      "\nAuthor === '2'"
                      "\nID === '3'"
                      "\n---> ")
    # if title selected; enter book title, select book in table and print book details
    if selection == "1":
        book_select = input("\nEnter book title: ")
        cr.execute('''
        SELECT id, Title, Author, Qty FROM books WHERE Title = ?''', (book_select,))
        book = cr.fetchone()
        print(book)

    # if author selected; enter book author, select book in table and print book details
    elif selection == "2":
        book_select = input("\nEnter book author: ")
        cr.execute('''
        SELECT id, Title, Author, Qty FROM books WHERE Author = ?''', (book_select,))
        book = cr.fetchone()
        print(book)

    # if id selected; enter book id, select book in table and print book details
    elif selection == "3":
        book_select = input("\nEnter book ID: ")
        cr.execute('''
        SELECT id, Title, Author, Qty FROM books WHERE id = ?''', (book_select,))
        book = cr.fetchone()
        print(book)

    # For unrecognized input
    else:
        print("Incorrect input ...")


# === Start of program ===
# Creates table with types, saves id as primary key
cr.execute('''
CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
''')

# Runs register_books() to load books from txt file if needed
# Runs menu()
register_books()
menu()


# === Optional commands, when checking ===
#print(tabulate(book_list, headers=["ID", "Title", "Author", "Qty"]))
#view_all = '''SELECT * from books'''
#    cr.execute(view_all)
#    records = cr.fetchall()
#    print(records)
