import sqlite3
from tkinter import *
from tkinter import messagebox

iteration = -1
row = 0
type = ""

conn = sqlite3.connect("mosque.db")
cursor = conn.cursor()


def clean_list_box(lb):
    lb.delete(0, END)


def execute(sql, return_flag=False):
    if return_flag:
        info = cursor.execute(sql)
        return info
    else:
        return cursor.execute(sql)


def show_all(lb):
    info = execute("SELECT * FROM users")
    clean_list_box(lb)
    for data in info:
        lb.insert("end", data)


def search_by_name(lb):
    global name_entry
    get_name = name_entry.get()
    if get_name == "":
        messagebox.showwarning("Warning", "Name is Empty!")
    else:
        clean_list_box(lb)
        info = execute(f"SELECT * FROM users WHERE name LIKE '%{get_name}%'")
        empty = True
        for data in info:
            if data != "":
                empty = False
            lb.insert("end", data)
        if empty:
            lb.insert("end", "No Result!")


def get_selected_value(value):
    global type
    type = value


def add_entry(lb):
    global id_entry,name_entry,type_entry,address_entry,coordinates_entry,imam_name_entry
    id = id_entry.get()
    name = name_entry.get()
    address = address_entry.get()
    coordinates = coordinates_entry.get()
    imam_name = imam_name_entry.get()
    
    if id == "" or name == "" or type == "" or address == "" or coordinates == "" or imam_name == "":
        messagebox.showwarning("Warning", "All fields are required!")
    else:
        clean_list_box(lb)
        execute(f"""
            INSERT INTO users VALUES('{id}','{name}','{address}','{type.strip()}','{coordinates}','{imam_name}')
        """)
        conn.commit()
        lb.insert("end", "Inserted Successfully!")


def format_labels_and_entries(label, entry):
    global row, iteration
    col = 0
    if iteration % 2 == 0:
        label.grid(row=row, column=col+2, padx=(25,0))
        entry.grid(row=row, column=col+3)
        row += 1
    else:
        label.grid(row=row, column=col)
        entry.grid(row=row, column=col+1)

    iteration += 1


window = Tk()
window.geometry("775x150")

id_label = Label(window, text='ID')
id_entry = Entry(window)

name_label = Label(window, text='Name')
name_entry = Entry(window)

type_label = Label(window, text='Type')
options_list = ["         Jama          ", "       Masjid          ", "        Musalla      "]
value_inside = StringVar(window)

value_inside.set("Select an Option")
# type_entry = Entry(window)
type_entry = OptionMenu(window, value_inside, *options_list, command=get_selected_value)

address_label = Label(window, text='Address')
address_entry = Entry(window)

coordinates_label = Label(window, text='Coordinates')
coordinates_entry = Entry(window)

imam_name_label = Label(window, text='Imam name')
imam_name_entry = Entry(window)

format_labels_and_entries(id_label,id_entry)
format_labels_and_entries(name_label,name_entry)
format_labels_and_entries(type_label,type_entry)
format_labels_and_entries(address_label,address_entry)
format_labels_and_entries(coordinates_label,coordinates_entry)
format_labels_and_entries(imam_name_label,imam_name_entry)

lb = Listbox(window)
lb.place(x=450,y=0, height=145, width=300)

display_all_button = Button(window, text="Display All", command=lambda: show_all(lb))
search_by_name_button = Button(window, text="Search by name", command=lambda: search_by_name(lb))
update_entry_button = Button(window, text="  Update Entry   ")
add_entry_button = Button(window, text="Add Entry ", command=lambda: add_entry(lb))
delete_entry_button = Button(window, text="    Delete Entry   ")
display_on_map_button = Button(window, text="Display on Map")

display_all_button.grid(row=4, column=1, pady=10, padx=2)
search_by_name_button.grid(row=4, column=2, padx=2)
update_entry_button.grid(row=4, column=3, padx=2)
add_entry_button.grid(row=5, column=1, padx=2)
delete_entry_button.grid(row=5, column=2, padx=2)
display_on_map_button.grid(row=5, column=3, padx=2)



window.mainloop()