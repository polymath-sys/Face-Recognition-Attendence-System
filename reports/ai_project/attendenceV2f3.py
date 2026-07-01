from tkinter import Tk, Label, Button, Frame, ttk, messagebox, filedialog,StringVar, LabelFrame
from PIL import Image, ImageTk
import os
import csv

mydata = []

class Attendance:
    def __init__(self, root):
        """Initialize the Attendance management window."""
        self.root = root
        self.root.geometry("1280x720+0+0")  # Adjusted for smaller screens
        self.root.title("Attendance Window")
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.atten_roll_var = StringVar()
        self.atten_dept_var = StringVar()
        self.atten_year_var = StringVar()
        self.atten_time_var = StringVar()
        self.atten_date_var = StringVar()
        self.atten_status_var = StringVar()

        # Colors
        self.header_bg = "#2c3e50"
        self.header_fg = "white"
        self.frame_bg = "white"
        self.label_fg = "#333333"
        self.button_bg = "#3498db"
        self.button_fg = "white"

        # Title label
        title_lbl = Label(self.root, text="Attendance", font=("Helvetica", 24, "bold"),
                         fg=self.header_fg, bg=self.header_bg, pady=10)
        title_lbl.place(relx=0, rely=0, relwidth=1)

        # Main frame
        main_frame = Frame(self.root, bg="#e6e6e6")
        main_frame.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.88)
        main_frame.columnconfigure((0, 1), weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Left frame (Form)
        left_frame = LabelFrame(main_frame, bg=self.frame_bg, relief="groove",
                               text="Attendance Management", font=("Helvetica", 12, "bold"),
                               fg=self.label_fg, padx=10, pady=10)
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Form fields
        fields = [
            ("Roll No:", self.atten_roll_var),
            ("Year:", self.atten_year_var),
            ("Date:", self.atten_date_var),
            ("Time:", self.atten_time_var),
            ("Department:", self.atten_dept_var),
            ("Attendance Status:", self.atten_status_var, ["Present", "Absent"])
        ]

        for i, field in enumerate(fields):
            label = Label(left_frame, text=field[0], font=("Helvetica", 12, "bold"),
                         bg=self.frame_bg, fg=self.label_fg)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            if len(field) == 3:  # Combobox for status
                combo = ttk.Combobox(left_frame, textvariable=field[1], values=field[2],
                                    state="readonly", font=("Helvetica", 11))
                combo.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            else:  # Entry field
                entry = ttk.Entry(left_frame, textvariable=field[1], font=("Helvetica", 11))
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")

        # Buttons frame
        btn_frame = Frame(left_frame, bg=self.frame_bg)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)

        buttons = [
            ("Import CSV", self.importCSV),
            ("Export CSV", self.exportCSV),
            ("Update", lambda: None),  # Placeholder, no functionality provided
            ("Reset", self.reset_data)
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = Button(btn_frame, text=text, command=cmd, font=("Helvetica", 12, "bold"),
                        bg=self.button_bg, fg=self.button_fg, width=12, bd=0)
            btn.grid(row=0, column=i, padx=5, pady=5)

        # Right frame (Table)
        right_frame = LabelFrame(main_frame, bg=self.frame_bg, relief="groove",
                                text="Attendance Records", font=("Helvetica", 12, "bold"),
                                fg=self.label_fg, padx=10, pady=10)
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Table frame
        table_frame = Frame(right_frame, bg=self.frame_bg)
        table_frame.pack(fill="both", expand=True)

        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")

        # Treeview table
        self.attendenceReportTable = ttk.Treeview(table_frame,
                                                 columns=("Roll", "Department", "Year", "Time", "Date", "Status"),
                                                 xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        scroll_x.config(command=self.attendenceReportTable.xview)
        scroll_y.config(command=self.attendenceReportTable.yview)

        # Table columns
        for col in ("Roll", "Department", "Year", "Time", "Date", "Status"):
            self.attendenceReportTable.heading(col, text=col)
            self.attendenceReportTable.column(col, width=100)  # Adjusted for smaller screens

        self.attendenceReportTable["show"] = "headings"
        self.attendenceReportTable.pack(fill="both", expand=True)
        self.attendenceReportTable.bind("<ButtonRelease>", self.get_cursor)

    def fetchData(self, rows):
        """Populate the table with data."""
        self.attendenceReportTable.delete(*self.attendenceReportTable.get_children())
        for row in rows:
            self.attendenceReportTable.insert("", "end", values=row)

    def importCSV(self):
        """Import attendance data from a CSV file."""
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV",
                                        filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")), parent=self.root)
        if fln:
            with open(fln) as myfile:
                csvread = csv.reader(myfile, delimiter=",")
                for row in csvread:
                    mydata.append(row)
                self.fetchData(mydata)

    def exportCSV(self):
        """Export table data to a CSV file."""
        try:
            if not mydata:
                messagebox.showerror("No Data", "No data found to export", parent=self.root)
                return
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV",
                                              filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")),
                                              defaultextension=".csv", parent=self.root)
            if fln:
                with open(fln, mode="w", newline="") as myfile:
                    exp_write = csv.writer(myfile, delimiter=",")
                    for row in mydata:
                        exp_write.writerow(row)
                    messagebox.showinfo("Data Export", f"Data exported to {os.path.basename(fln)} successfully")
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def get_cursor(self, event=""):
        """Populate form fields when a table row is clicked."""
        cursor_row = self.attendenceReportTable.focus()
        content = self.attendenceReportTable.item(cursor_row)
        row = content['values']
        if row and len(row) == 6:
            self.atten_roll_var.set(row[0])
            self.atten_dept_var.set(row[1])
            self.atten_year_var.set(row[2])
            self.atten_time_var.set(row[3])
            self.atten_date_var.set(row[4])
            self.atten_status_var.set(row[5])

    def reset_data(self):
        """Clear all form fields."""
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