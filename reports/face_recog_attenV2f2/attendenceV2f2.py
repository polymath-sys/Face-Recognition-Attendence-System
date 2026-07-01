from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import csv


class Attendance:
    """
    Attendance management system for recording and managing attendance records.
    Supports importing/exporting attendance data in CSV format.
    """
    
    def __init__(self, root: Tk):
        """
        Initialize the attendance management window.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.geometry("1200x650+100+50")  # Adjusted for smaller screens
        self.root.title("Attendance Management")
        self.root.configure(bg="#f0f0f0")

        # Data storage
        self.attendance_records = []

        # Form variables
        self.var_roll = StringVar()
        self.var_dept = StringVar()
        self.var_year = StringVar()
        self.var_time = StringVar()
        self.var_date = StringVar()
        self.var_status = StringVar()

        self._setup_ui()

    def _setup_ui(self):
        """Setup the user interface components."""
        # Title Label
        title_lbl = Label(
            self.root,
            text="Attendance Management",
            font=("Helvetica", 20, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title_lbl.pack(fill=X, pady=10)

        # Main Frame
        main_frame = Frame(self.root, bg="#e6e6e6")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Left Frame (Form)
        left_frame = LabelFrame(
            main_frame,
            text="Attendance Details",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        left_frame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        left_frame.pack_propagate(False)
        left_frame.configure(width=400)

        self._setup_form(left_frame)

        # Right Frame (Table)
        right_frame = LabelFrame(
            main_frame,
            text="Attendance Records",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

        self._setup_table(right_frame)

    def _setup_form(self, parent: Frame):
        """Setup the attendance form in the left frame."""
        form_frame = Frame(parent, bg="white")
        form_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Form fields
        fields = [
            ("Roll No:", self.var_roll),
            ("Department:", self.var_dept),
            ("Year:", self.var_year),
            ("Date (DD-MM-YYYY):", self.var_date),
            ("Time (HH:MM):", self.var_time),
            ("Status:", self.var_status)
        ]

        for row, (label_text, var) in enumerate(fields):
            Label(
                form_frame,
                text=label_text,
                font=("Helvetica", 11),
                bg="white"
            ).grid(row=row, column=0, padx=5, pady=5, sticky=W)

            if label_text == "Status:":
                ttk.Combobox(
                    form_frame,
                    textvariable=var,
                    values=["Present", "Absent"],
                    state="readonly",
                    font=("Helvetica", 10),
                    width=18
                ).grid(row=row, column=1, padx=5, pady=5)
            else:
                ttk.Entry(
                    form_frame,
                    textvariable=var,
                    font=("Helvetica", 10),
                    width=20
                ).grid(row=row, column=1, padx=5, pady=5)

        # Buttons Frame
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)

        buttons = [
            ("Import CSV", self.import_csv),
            ("Export CSV", self.export_csv),
            ("Reset", self.reset_form)
        ]

        for col, (text, command) in enumerate(buttons):
            Button(
                btn_frame,
                text=text,
                command=command,
                font=("Helvetica", 10, "bold"),
                bg="#3498db",
                fg="white",
                width=12,
                bd=0
            ).grid(row=0, column=col, padx=5, pady=5)

    def _setup_table(self, parent: Frame):
        """Setup the attendance records table in the right frame."""
        # Scrollbars
        scroll_x = ttk.Scrollbar(parent, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(parent, orient=VERTICAL)

        # Attendance Table
        self.attendance_table = ttk.Treeview(
            parent,
            columns=("roll", "dept", "year", "date", "time", "status"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        # Configure columns
        columns = {
            "roll": ("Roll No", 100),
            "dept": ("Department", 120),
            "year": ("Year", 80),
            "date": ("Date", 100),
            "time": ("Time", 80),
            "status": ("Status", 80)
        }

        for col, (heading, width) in columns.items():
            self.attendance_table.heading(col, text=heading)
            self.attendance_table.column(col, width=width, anchor=CENTER)

        self.attendance_table["show"] = "headings"
        self.attendance_table.pack(fill=BOTH, expand=True)
        self.attendance_table.bind("<ButtonRelease-1>", self._load_selected_record)

    def _load_selected_record(self, event):
        """Load selected record from table into form fields."""
        selected_item = self.attendance_table.focus()
        if not selected_item:
            return

        record = self.attendance_table.item(selected_item)["values"]
        if len(record) == 6:
            self.var_roll.set(record[0])
            self.var_dept.set(record[1])
            self.var_year.set(record[2])
            self.var_date.set(record[3])
            self.var_time.set(record[4])
            self.var_status.set(record[5])

    def import_csv(self):
        """Import attendance records from CSV file."""
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select CSV File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )

        if not file_path:
            return

        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                self.attendance_records = [row for row in csv_reader if row]

            self._update_table()
            messagebox.showinfo(
                "Success",
                f"Imported {len(self.attendance_records)} records",
                parent=self.root
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to import CSV:\n{str(e)}",
                parent=self.root
            )

    def export_csv(self):
        """Export attendance records to CSV file."""
        if not self.attendance_records:
            messagebox.showwarning(
                "No Data",
                "No attendance records to export",
                parent=self.root
            )
            return

        file_path = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )

        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.attendance_records)

            messagebox.showinfo(
                "Success",
                f"Exported {len(self.attendance_records)} records to:\n{file_path}",
                parent=self.root
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to export CSV:\n{str(e)}",
                parent=self.root
            )

    def _update_table(self):
        """Update the table with current attendance records."""
        self.attendance_table.delete(*self.attendance_table.get_children())
        for record in self.attendance_records:
            if len(record) == 6:  # Ensure record has all required fields
                self.attendance_table.insert("", END, values=record)

    def reset_form(self):
        """Reset all form fields to empty values."""
        self.var_roll.set("")
        self.var_dept.set("")
        self.var_year.set("")
        self.var_date.set("")
        self.var_time.set("")
        self.var_status.set("")


if __name__ == "__main__":
    root = Tk()
    app = Attendance(root)
    root.mainloop()