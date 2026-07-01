from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import csv
from tkinter import filedialog


mydata = []

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1750x858+0+0")
        self.root.title("Attendance Window")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Custom colors and fonts
        self.header_bg = "#2c3e50"  # Dark blue
        self.header_fg = "white"
        self.frame_bg = "white"
        self.label_fg = "#333333"  # Dark gray
        self.button_bg = "#3498db"  # Blue
        self.button_fg = "white"

        # Title Label with improved styling
        title_lbl = Label(self.root, text="Attendance", font=("Helvetica", 30, "bold"), 
                        fg=self.header_fg, bg=self.header_bg, pady=10)
        title_lbl.place(x=0, y=0, width=1750, height=60)

        # Main Frame with better background
        main_frame = Frame(self.root, bg="#e6e6e6", bd=0)  # Light gray
        main_frame.place(x=10, y=70, width=1730, height=770)

        # Left Frame with improved styling
        left_frame = LabelFrame(main_frame, bd=2, bg=self.frame_bg, relief=GROOVE, 
                              text="Attendance Management", font=("Helvetica", 12, "bold"), 
                              fg=self.label_fg, padx=10, pady=10)
        left_frame.place(x=10, y=10, width=800, height=750)

        # Attendance ID
        attendence_id = Label(left_frame, text="AttendanceID:", font=("Helvetica", 12, "bold"), 
                            bg=self.frame_bg, fg=self.label_fg)
        attendence_id.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.attendence_id_entry = ttk.Entry(left_frame, width=22, font=("Helvetica", 11))
        self.attendence_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Roll No
        roll_no = Label(left_frame, text="Roll No:", font=("Helvetica", 12, "bold"), 
                      bg=self.frame_bg, fg=self.label_fg)
        roll_no.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        self.roll_no_entry = ttk.Entry(left_frame, width=22, font=("Helvetica", 11))
        self.roll_no_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # Time
        time = Label(left_frame, text="Time:", font=("Helvetica", 12, "bold"), 
                   bg=self.frame_bg, fg=self.label_fg)
        time.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        self.time_entry = ttk.Entry(left_frame, width=22, font=("Helvetica", 11))
        self.time_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W)

        # Date
        date = Label(left_frame, text="Date:", font=("Helvetica", 12, "bold"), 
                   bg=self.frame_bg, fg=self.label_fg)
        date.grid(row=4, column=0, padx=10, pady=10, sticky=W)

        self.date_entry = ttk.Entry(left_frame, width=22, font=("Helvetica", 11))
        self.date_entry.grid(row=4, column=1, padx=10, pady=10, sticky=W)

        # Department
        department = Label(left_frame, text="Department:", font=("Helvetica", 12, "bold"), 
                         bg=self.frame_bg, fg=self.label_fg)
        department.grid(row=5, column=0, padx=10, pady=10, sticky=W)

        self.department_entry = ttk.Entry(left_frame, width=22, font=("Helvetica", 11))
        self.department_entry.grid(row=5, column=1, padx=10, pady=10, sticky=W)

        # Attendance Status
        status = Label(left_frame, text="Attendance Status:", font=("Helvetica", 12, "bold"), 
                     bg=self.frame_bg, fg=self.label_fg)
        status.grid(row=6, column=0, padx=10, pady=10, sticky=W)

        self.status_combo = ttk.Combobox(left_frame, width=20, font=("Helvetica", 11),
                                       values=["Present", "Absent"], state="readonly")
        self.status_combo.current(0)
        self.status_combo.grid(row=6, column=1, padx=10, pady=10, sticky=W)

       
       
       
        # Buttons Frame with improved styling
        btn_frame = Frame(left_frame, bg=self.frame_bg, bd=0)
        btn_frame.place(x=10, y=350, width=770, height=150)

        # Save Button
        save_btn = Button(btn_frame, text="Import CSV",command=self.importCSV, width=15, font=("Helvetica",12, "bold"),
                         bg=self.button_bg, fg="black", bd=0)
        save_btn.grid(row=0, column=0, padx=5, pady=5)

        # Update Button
        update_btn = Button(btn_frame, text="Export CSV",command=self.exportCSV, width=15, font=("Helvetica",12, "bold"),
                           bg=self.button_bg, fg="black", bd=0)
        update_btn.grid(row=0, column=1, padx=5, pady=5)

        # Delete Button
        delete_btn = Button(btn_frame, text="Update", width=15, font=("Helvetica", 12,"bold"),
                           bg=self.button_bg, fg="black", bd=0)  # Red color for delete
        delete_btn.grid(row=0, column=2, padx=5, pady=5)

        # Reset Button
        reset_btn = Button(btn_frame, text="Reset", width=15, font=("Helvetica", 12,"bold"),
                          bg=self.button_bg, fg="black", bd=0)  # Orange color for reset
        reset_btn.grid(row=0, column=3, padx=5, pady=5)

        # # Take Photo Sample Button
        # take_photo_btn = Button(btn_frame, text="Take Photo Sample", width=17, 
        #                       font=("Helvetica", 12,"bold"), bg=self.button_bg, fg="black", bd=0)  # Green color
        # take_photo_btn.grid(row=1, column=0, padx=5, pady=5)

        # # Update Photo Sample Button
        # update_photo_btn = Button(btn_frame, text="Update Photo Sample", width=17,
        #                         font=("Helvetica", 12,"bold"), bg=self.button_bg, fg="black", bd=0)  # Purple color
        # update_photo_btn.grid(row=1, column=1, padx=5, pady=5)


 # Right Frame with improved styling
        right_frame = LabelFrame(main_frame, bd=2, bg=self.frame_bg, relief=GROOVE, 
                               text="Attendance Records", font=("Helvetica", 12,"bold"), 
                               fg=self.label_fg, padx=10, pady=10)
        right_frame.place(x=830, y=10, width=880, height=750)


        table_frame = Frame(right_frame, bg="gray", bd=0)
        table_frame.place(x=5, y=5, width=830, height=450)
        #scroll bar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)


        self.attendenceReportTable = ttk.Treeview(table_frame, columns=("Roll","Department","Year","Time","Date","Status"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.attendenceReportTable.xview)
        scroll_y.config(command=self.attendenceReportTable.yview)


        self.attendenceReportTable.heading("Roll", text="Roll No")
        self.attendenceReportTable.heading("Department", text="Department")
        self.attendenceReportTable.heading("Year", text="Year")
        self.attendenceReportTable.heading("Time", text="Time")
        self.attendenceReportTable.heading("Date", text="Date")
        self.attendenceReportTable.heading("Status", text="Attendance")

        self.attendenceReportTable["show"] = "headings"

        self.attendenceReportTable.column("Roll", width=100)
        self.attendenceReportTable.column("Department", width=120)
        self.attendenceReportTable.column("Year", width=100)
        self.attendenceReportTable.column("Time", width=100)
        self.attendenceReportTable.column("Date", width=100)
        self.attendenceReportTable.column("Status", width=120)

        self.attendenceReportTable.pack(fill=BOTH, expand=1)



        #========================face data===================

    def fetchData(self, rows):
        self.attendenceReportTable.delete(*self.attendenceReportTable.get_children())
        for i in rows:
            self.attendenceReportTable.insert("",END, values=i)

#IMPORT CSV
    def importCSV(self):
        global mydata
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title = "Open CSV", filetypes=(("CSV File", "*csv"),("ALl File","*.*")),parent = self.root)
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)


#EXPORT CSV
    def exportCSV(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data","No Data Found", parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title = "Open CSV", filetypes=(("CSV File", "*csv"),("ALl File","*.*")),parent = self.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write = csv.writer(myfile, delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export", "Your Data Exported to"+os.path.basename(fln)+"successfully")
        
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

            

    







if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()