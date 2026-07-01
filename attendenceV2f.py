from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import csv
from tkinter import filedialog

# attendance_gui.py

from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import csv

mydata = []

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1750x858+0+0")
        self.root.title("Attendance Window")
        self.root.configure(bg="#f0f0f0")

        # ===========VARIABLES==============
        self.atten_id_var = StringVar()
        self.atten_roll_var = StringVar()
        self.atten_dept_var = StringVar()
        self.atten_year_var = StringVar()
        self.atten_time_var = StringVar()
        self.atten_date_var = StringVar()
        self.atten_status_var = StringVar()

        # ======= COLORS ==========
        self.header_bg = "#2c3e50"
        self.header_fg = "white"
        self.frame_bg = "white"
        self.label_fg = "#333333"
        self.button_bg = "#3498db"
        self.button_fg = "white"

        # ======= TITLE LABEL ==========
        title_lbl = Label(self.root, text="Attendance", font=("Helvetica", 30, "bold"),
                          fg=self.header_fg, bg=self.header_bg, pady=10)
        title_lbl.place(x=0, y=0, width=1750, height=60)

        # ======= MAIN FRAME ==========
        main_frame = Frame(self.root, bg="#e6e6e6", bd=0)
        main_frame.place(x=10, y=70, width=1730, height=770)

        # ======= LEFT FRAME (Form Area) ==========
        left_frame = LabelFrame(main_frame, bd=2, bg=self.frame_bg, relief=GROOVE,
                                text="Attendance Management", font=("Helvetica", 12, "bold"),
                                fg=self.label_fg, padx=10, pady=10)
        left_frame.place(x=10, y=10, width=800, height=750)

        # ======= ENTRY FIELDS ==========
        # Label(left_frame, text="AttendanceID:", font=("Helvetica", 12, "bold"),
        #       bg=self.frame_bg, fg=self.label_fg).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        # ttk.Entry(left_frame, textvariable=self.atten_id_var, width=22, font=("Helvetica", 11)).grid(row=0, column=1, padx=10, pady=10, sticky=W)

        Label(left_frame, text="Roll No:", font=("Helvetica", 12, "bold"),
              bg=self.frame_bg, fg=self.label_fg).grid(row=2, column=0, padx=10, pady=10, sticky=W)
        ttk.Entry(left_frame, textvariable=self.atten_roll_var, width=22, font=("Helvetica", 11)).grid(row=2, column=1, padx=10, pady=10, sticky=W)

        Label(left_frame, text="Year:", font=("Helvetica", 12, "bold"),
              bg=self.frame_bg, fg=self.label_fg).grid(row=3, column=0, padx=10, pady=10, sticky=W)
        ttk.Entry(left_frame, textvariable=self.atten_year_var, width=22, font=("Helvetica", 11)).grid(row=3, column=1, padx=10, pady=10, sticky=W)

        Label(left_frame, text="Date:", font=("Helvetica", 12, "bold"),
              bg=self.frame_bg, fg=self.label_fg).grid(row=4, column=0, padx=10, pady=10, sticky=W)
        ttk.Entry(left_frame, textvariable=self.atten_date_var, width=22, font=("Helvetica", 11)).grid(row=4, column=1, padx=10, pady=10, sticky=W)

        Label(left_frame, text="Time:", font=("Helvetica", 12, "bold"),
              bg=self.frame_bg, fg=self.label_fg).grid(row=5, column=0, padx=10, pady=10, sticky=W)
        ttk.Entry(left_frame, textvariable=self.atten_time_var, width=22, font=("Helvetica", 11)).grid(row=5, column=1, padx=10, pady=10, sticky=W)

        Label(left_frame, text="Department:", font=("Helvetica", 12, "bold"),
              bg=self.frame_bg, fg=self.label_fg).grid(row=6, column=0, padx=10, pady=10, sticky=W)
        ttk.Entry(left_frame, textvariable=self.atten_dept_var, width=22, font=("Helvetica", 11)).grid(row=6, column=1, padx=10, pady=10, sticky=W)

        Label(left_frame, text="Attendance Status:", font=("Helvetica", 12, "bold"),
              bg=self.frame_bg, fg=self.label_fg).grid(row=7, column=0, padx=10, pady=10, sticky=W)
        ttk.Combobox(left_frame, textvariable=self.atten_status_var, values=["Present", "Absent"],
                     state="readonly", width=20, font=("Helvetica", 11)).grid(row=7, column=1, padx=10, pady=10, sticky=W)

        # ======= BUTTONS ==========
        btn_frame = Frame(left_frame, bg=self.frame_bg, bd=0)
        btn_frame.place(x=10, y=350, width=770, height=150)

        Button(btn_frame, text="Import CSV", command=self.importCSV, width=15, font=("Helvetica", 12, "bold"),
               bg=self.button_bg, fg="black", bd=0).grid(row=0, column=0, padx=5, pady=5)

        Button(btn_frame, text="Export CSV", command=self.exportCSV, width=15, font=("Helvetica", 12, "bold"),
               bg=self.button_bg, fg="black", bd=0).grid(row=0, column=1, padx=5, pady=5)

        Button(btn_frame, text="Update", width=15, font=("Helvetica", 12, "bold"),
               bg=self.button_bg, fg="black", bd=0).grid(row=0, column=2, padx=5, pady=5)

        Button(btn_frame, text="Reset", width=15,command=self.reset_data, font=("Helvetica", 12, "bold"),
               bg=self.button_bg, fg="black", bd=0).grid(row=0, column=3, padx=5, pady=5)

        # ======= RIGHT FRAME (Table Area) ==========
        right_frame = LabelFrame(main_frame, bd=2, bg=self.frame_bg, relief=GROOVE,
                                 text="Attendance Records", font=("Helvetica", 12, "bold"),
                                 fg=self.label_fg, padx=10, pady=10)
        right_frame.place(x=830, y=10, width=880, height=750)

        table_frame = Frame(right_frame, bg="gray", bd=0)
        table_frame.place(x=5, y=5, width=830, height=450)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.attendenceReportTable = ttk.Treeview(table_frame,
                                                  columns=("Roll", "Department", "Year", "Time", "Date", "Status"),
                                                  xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendenceReportTable.xview)
        scroll_y.config(command=self.attendenceReportTable.yview)

        for col in ("Roll", "Department", "Year", "Time", "Date", "Status"):
            self.attendenceReportTable.heading(col, text=col)
            self.attendenceReportTable.column(col, width=120)

        self.attendenceReportTable["show"] = "headings"
        self.attendenceReportTable.pack(fill=BOTH, expand=1)
        self.attendenceReportTable.bind("<ButtonRelease>", self.get_cursor)

    def fetchData(self, rows):
        # Clears and loads new data into the table
        self.attendenceReportTable.delete(*self.attendenceReportTable.get_children())
        for i in rows:
            self.attendenceReportTable.insert("", END, values=i)

    def importCSV(self):
        # Load CSV and populate table
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV",
                                         filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")), parent=self.root)
        if fln == "":
            return
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)

    def exportCSV(self):
        # Save current table data into a CSV
        try:
            if len(mydata) < 1:
                messagebox.showerror("No Data", "No Data Found", parent=self.root)
                return False
            script_dir = os.path.dirname(os.path.abspath(__file__))
            fln = filedialog.asksaveasfilename(initialdir=script_dir, title="Save CSV",
                                               filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")),
                                               defaultextension=".csv", parent=self.root)
            if fln == "":
                return
            with open(fln, mode="w", newline="") as myfile:
                exp_write = csv.writer(myfile, delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export", f"Your data was exported to {os.path.basename(fln)} successfully")
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def get_cursor(self, event=""):
        # When a row is clicked in the table, fill form fields with its data
        cursor_row = self.attendenceReportTable.focus()
        content = self.attendenceReportTable.item(cursor_row)
        row = content['values']

        if len(row) == 6:
            self.atten_roll_var.set(row[0])
            self.atten_dept_var.set(row[1])
            self.atten_year_var.set(row[2])
            self.atten_time_var.set(row[3])
            self.atten_date_var.set(row[4])
            self.atten_status_var.set(row[5])

    def reset_data(self):
        #when reset button is pressed it removes the data from entry fields, making them empty, without actuqally deleting the data
        self.atten_roll_var.set("")
        self.atten_dept_var.set("")
        self.atten_year_var.set("")
        self.atten_time_var.set("")
        self.atten_date_var.set("")
        self.atten_status_var.set("")



if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
