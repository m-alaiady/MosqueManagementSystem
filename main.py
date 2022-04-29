import sqlite3
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox

apiKey = 'AIzaSyAAzp_8Ulsle3lbUhscWGFrsfIDu_hgCJA'

iteration = -1
row = 0
type = ""
SUCCESS_OPERATION_TEXT = "Success Operation"
FAILED_OPERATION_TEXT = "Failed Operation"

conn = sqlite3.connect("mosque.db")
cursor = conn.cursor()


def display_on_map():
    plt.figure(figsize=(10,10))
    # m = Basemap(projection='nsper', lon_0=-105, lat_0=40)
    m = Basemap(projection='mill')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    # x,y = 43.89296888589738, 26.390715512939977
    coordinates = []

    info = execute("SELECT coordinates FROM users")

    for data in info:
        x_y = data[0].split(',')
        print(x_y)

        # coordinates.append(x_y)

    print(coordinates[0])
    # xpt, ypt = m(x,y)
    # m.plot(xpt,ypt,'ro', markersize=5)
    # plt.title("Mosques Coordinates")
    # plt.show()


def selected_item_listbox(lb):
    for i in lb.curselection():
        return lb.get(i)


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
        messagebox.showwarning("Name is Required", "Name is Empty!")
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
        messagebox.showinfo(SUCCESS_OPERATION_TEXT, "New Record Inserted Successfully!")


def delete_entry(lb):
    data = selected_item_listbox(lb)
    if data:
        id_to_remove = data[0]
        if isinstance(id_to_remove, int):
            execute(f"""
                         DELETE FROM users WHERE id = '{id_to_remove}'
                     """)
            conn.commit()
            messagebox.showinfo(SUCCESS_OPERATION_TEXT, "Record Deleteed Successfully!")
            return

    messagebox.showwarning("Warning", "Display records and select from it")


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

lb = Listbox(window, width=100)
lb.place(x=450,y=0, height=145, width=300)

display_all_button = Button(window, text="Display All", command=lambda: show_all(lb))
search_by_name_button = Button(window, text="Search by name", command=lambda: search_by_name(lb))
update_entry_button = Button(window, text="  Update Entry   ")
add_entry_button = Button(window, text="Add Entry ", command=lambda: add_entry(lb))
delete_entry_button = Button(window, text="    Delete Entry   ", command=lambda: delete_entry(lb))
display_on_map_button = Button(window, text="Display on Map", command=display_on_map)

display_all_button.grid(row=4, column=1, pady=10, padx=2)
search_by_name_button.grid(row=4, column=2, padx=2)
update_entry_button.grid(row=4, column=3, padx=2)
add_entry_button.grid(row=5, column=1, padx=2)
delete_entry_button.grid(row=5, column=2, padx=2)
display_on_map_button.grid(row=5, column=3, padx=2)


window.mainloop()