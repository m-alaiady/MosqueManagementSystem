"""
    Mosque Management System
        enable users to add, update, delete, search, display,
        as well as display on map mosques around the world

        @author: Mohammed Alaiadhy
        @timestamp: 2022-05-01 06:53 AM
    """
import sqlite3
import re
from tkinter import Tk, Label, Button, Listbox, Entry, OptionMenu, StringVar, END
from tkinter import messagebox
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


class Mosque:
    """
        Mosque Class
            @methods
                1. display
                2. insert
                3. delete
                4. update
                5. search
                6. display map
        """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-local-variables
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-boolean-expressions-in-if-statement
    conn = ""
    cursor = ""
    WINDOW_SIZE = "975x150"
    SUCCESS_OPERATION_TEXT = "Success Operation"
    FAILED_OPERATION_TEXT = "Failed Operation"
    TABLE_NAME = "Mosq"
    id_entry = ""
    name_entry = ""
    type_entry = ""
    type_value = ""
    address_entry = ""
    coordinates_entry = ""
    imam_name_entry = ""
    list_box = ""
    format_row = 1
    format_column_offset = 1

    def __init__(self):
        self.conn = sqlite3.connect("mosque.db")
        self.cursor = self.conn.cursor()

        window = Tk()
        window.title("Mosque Management System")
        window.geometry(self.WINDOW_SIZE)

        id_label = Label(window, text='ID')
        self.id_entry = Entry(window)

        name_label = Label(window, text='Name')
        self.name_entry = Entry(window)

        type_label = Label(window, text='Type')
        options_list = ["Jama", "Masjid", "Musalla"]
        value_inside = StringVar(window)

        value_inside.set("Select an Option")
        self.type_entry = OptionMenu(
            window, value_inside, *options_list, command=self.__get_selected_value
        )

        address_label = Label(window, text='Address')
        self.address_entry = Entry(window)

        coordinates_label = Label(window, text='Coordinates')
        self.coordinates_entry = Entry(window)

        imam_name_label = Label(window, text='Imam name')
        self.imam_name_entry = Entry(window)

        self.__format_labels_and_entries(id_label, self.id_entry)
        self.__format_labels_and_entries(name_label, self.name_entry)
        self.__format_labels_and_entries(type_label, self.type_entry)
        self.__format_labels_and_entries(address_label, self.address_entry)
        self.__format_labels_and_entries(coordinates_label, self.coordinates_entry)
        self.__format_labels_and_entries(imam_name_label, self.imam_name_entry)

        self.list_box = Listbox(window, width=100)
        self.list_box.place(x=450, y=0, height=145, width=500)

        display_all_button = Button(window, text="Display All", command=self.display)
        search_by_name_button = Button(window, text="Search by name", command=self.search)
        update_entry_button = Button(window, text="Update Entry", command=lambda: self.update(
            self.id_entry.get(), self.imam_name_entry.get()
        ))
        add_entry_button = Button(window, text="Add Entry ", command=lambda: self.insert(
            self.id_entry.get(), self.name_entry.get(),
            self.type_value, self.address_entry.get(),
            self.coordinates_entry.get(), self.imam_name_entry.get()
        ))
        delete_entry_button = Button(
            window, text="Delete Entry", command=lambda: self.delete(self.id_entry.get())
        )
        display_on_map_button = Button(
            window, text="Display on Map", command=self.display_map
        )

        display_all_button.grid(row=4, column=1, pady=10, padx=2)
        search_by_name_button.grid(row=4, column=2, padx=2)
        update_entry_button.grid(row=4, column=3, padx=2)
        add_entry_button.grid(row=5, column=1, padx=2)
        delete_entry_button.grid(row=5, column=2, padx=2)
        display_on_map_button.grid(row=5, column=3, padx=2)

        window.mainloop()

    def __execute(self, sql, return_flag=False):
        if return_flag:
            info = self.cursor.execute(sql)
            return info
        return self.cursor.execute(sql)

    def __format_labels_and_entries(self, label, entry):
        col = 0
        if self.format_column_offset % 2 == 0:
            label.grid(row=self.format_row, column=col + 2, padx=(25, 0))
            entry.grid(row=self.format_row, column=col + 3)
            self.format_row += 1
        else:
            label.grid(row=self.format_row, column=col)
            entry.grid(row=self.format_row, column=col + 1)

        self.format_column_offset += 1

    def __clean_list_box(self):
        self.list_box.delete(0, END)

    def __get_selected_value(self, value):
        self.type_value = value

    def display(self):
        """
             display method
                 display all records from the table into list box
         """
        self.__execute(f"SELECT * FROM {self.TABLE_NAME}")
        self.__clean_list_box()

        exist = self.cursor.fetchone()
        if exist is None:
            messagebox.showwarning("No data", "There is no data to display!")
        else:
            self.__execute(f"SELECT * FROM {self.TABLE_NAME}")
            rows = self.cursor.fetchall()
            for data in rows:
                self.list_box.insert("end", data)

    def search(self):
        """
            Search method
                searches for a specific mosque name
        """
        get_name = self.name_entry.get()
        if get_name == "":
            messagebox.showwarning("Name is Required", "Name is Empty!")
        else:
            self.__clean_list_box()
            info = self.__execute(f"SELECT * FROM {self.TABLE_NAME} WHERE name LIKE '%{get_name}%'")
            empty = True
            for data in info:
                self.list_box.insert("end", data)
                return data
            if empty:
                self.list_box.insert("end", "No Result!")

    def insert(self, mosque_id, name, type, address, coordinates, imam_name):
        """
            insert method
               insert a new entry into the table
        """
        if mosque_id == "" or name == "" or type == "" \
                or address == "" or coordinates == "" or imam_name == "":
            messagebox.showwarning("All fields required", "All fields are required!")
        else:
            regexp = re.compile(
                r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?'
                r'(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(''\\.\\d+)?)$'
            )
            if not regexp.search(coordinates):
                messagebox.showwarning(
                    "Invalid coordinates format", "Invalid coordinates!"
                )
            else:
                self.__execute(f" SELECT * FROM {self.TABLE_NAME} WHERE id = '{mosque_id}'")
                exist = self.cursor.fetchone()
                if exist:
                    messagebox.showwarning(
                        "ID already taken", "ID already taken, choose another one"
                    )
                    return

                self.__clean_list_box()
                self.__execute(f"""
                    INSERT INTO {self.TABLE_NAME} 
                    VALUES('{mosque_id}','{name}','{address}','{type.strip()}','{coordinates}','{imam_name}')
                """)
                self.conn.commit()
                messagebox.showinfo(
                    self.SUCCESS_OPERATION_TEXT, "New Record Inserted Successfully!"
                )

    def delete(self, mosque_id):
        """
            delete method
               delete a record from the table from the specified mosque_id
        """
        if self.id_entry.get() == "":
            messagebox.showwarning("ID is Required", "ID is Empty!")
            return
        self.__execute(f" SELECT * FROM {self.TABLE_NAME} WHERE id = '{mosque_id}'")
        exist = self.cursor.fetchone()
        if exist is None:
            messagebox.showwarning("Unknown ID", "Cannot find the specified ID")
            return

        self.__execute(f"""
                     DELETE FROM {self.TABLE_NAME} WHERE id = '{mosque_id}'
                 """)
        self.conn.commit()
        messagebox.showinfo(
            self.SUCCESS_OPERATION_TEXT, "Record Deleted Successfully!"
        )
        self.display()
        return

    def update(self, mosque_id, imam_name):
        """
          update method
             update imam name column from existing record by using mosque_id
        """
        if self.id_entry.get() == "" or self.imam_name_entry.get() == "":
            messagebox.showwarning(
                "ID and imam type required", "ID and Imam name are required!"
            )
            return
        self.__execute(f" SELECT * FROM {self.TABLE_NAME} WHERE id = '{mosque_id}'")
        exist = self.cursor.fetchone()
        if exist is None:
            messagebox.showwarning("Unknown ID", "Cannot find the specified ID")
            return

        self.__execute(
            f"UPDATE {self.TABLE_NAME} SET imam_name = '{imam_name}' WHERE ID = '{mosque_id}'"
        )
        self.conn.commit()
        messagebox.showinfo(
            self.SUCCESS_OPERATION_TEXT, "Record Updated Successfully!"
        )
        self.display()
        return

    def display_map(self):
        """
          display_map method
             it shows the mosque's coordinates in a map
        """
        plt.figure("Mosque Location", figsize=(8, 8))
        basemap_map = Basemap(projection='nsper', lon_0=40, lat_0=20)
        # basemap_map = Basemap(width=100, height=100, projection='mill')
        basemap_map.drawcoastlines()

        basemap_map.drawcountries()
        basemap_map.bluemarble()
        coordinates = []
        labels = []
        self.__execute(f"SELECT coordinates FROM {self.TABLE_NAME}")
        exist = self.cursor.fetchone()

        if exist is None:
            messagebox.showwarning(
                "No data", "There is no data to display on map!"
            )
        else:
            self.__execute(f"SELECT coordinates,name FROM {self.TABLE_NAME}")
            rows = self.cursor.fetchall()
            for data in rows:
                x_y = data[0].split(',')
                labels.append(data[1])
                coordinates.append(x_y)
            label_index = 0

            for coordinate in coordinates:
                # Latitude = coordinate[1], Longitude = coordinate[0]
                xpt, ypt = basemap_map(float(coordinate[1]), float(coordinate[0]))
                basemap_map.plot(xpt, ypt, 'ro', markersize=5)
                plt.text(xpt, ypt, labels[label_index], color='white', fontsize=7)
                label_index += 1

            plt.title("Mosques Coordinates")
            plt.show()

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    mosque = Mosque()
