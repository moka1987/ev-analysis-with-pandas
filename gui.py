import tkinter as tk  # tkinter — გრაფიკული ინტერფეისის ბიბლიოთეკა
from tkinter import messagebox  # შეტყობინებების ფანჯრების გამოსაყენებლად
from processor import EnhancedProcessor, SQLiteManager, run_threaded_summary  # ჩვენი ლოგიკური კლასი
class EVGUI:
    """გრაფიკული ინტერფეისის კლასი ელექტრო მანქანის მონაცემებისთვის"""
    def __init__(self, master):
        """ინიციალიზაცია — ქმნის ფანჯარას და ღილაკებს"""
        self.master = master
        self.master.title("EV მონაცემთა დამუშავება")  # ფანჯრის სათაური
        # → ფონის ფერი ფანჯარაზე
        self.master.configure(bg="#f0f8ff")  # ღია ლურჯი (Alice Blue)
        # მონაცემების დამმუშავებელი ობიექტი (CSV ფაილით)
        self.processor = EnhancedProcessor("Electric_Vehicle_Population_Data.csv")
        # თითოეული ღილაკი და მასზე მიბმული ფუნქცია
        self.load_btn = tk.Button(master, text="მონაცემების ჩატვირთვა", command=self.load_data,bg="#4caf50", fg="white")
        self.clean_btn = tk.Button(master, text="გასუფთავება", command=self.clean_data,bg="#2196f3", fg="white")
        self.save_btn = tk.Button(master, text="ბაზაში შენახვა", command=self.save_to_db,bg="#ff9800", fg="white")
        self.plot_btn = tk.Button(master, text="გრაფიკის ნახვა", command=self.show_plot,bg="#9c27b0", fg="white")
        self.summary_btn = tk.Button(master, text="შეჯამება Thread-ში", command=self.threaded_summary,bg="#f44336", fg="white")

        # ღილაკების განლაგება (ვერტიკალურად დაშორებით)
        self.load_btn.pack(pady=5)
        self.clean_btn.pack(pady=5)
        self.save_btn.pack(pady=5)
        self.plot_btn.pack(pady=5)
        self.summary_btn.pack(pady=5)
    def load_data(self):
        """CSV ფაილის ჩატვირთვა და შეტყობინების გამოტანა"""
        self.processor.load_data()
        messagebox.showinfo("ჩატვირთვა", "მონაცემები ჩაიტვირთა!")
    def clean_data(self):
        """მონაცემების გასუფთავება და შეტყობინება"""
        self.processor.clean_data()
        messagebox.showinfo("გასუფთავება", "მონაცემები გასუფთავდა!")
    def save_to_db(self):
        """ბაზაში შენახვა და შეტყობინება"""
        db = SQLiteManager("ev_database.db")  # ბაზის ფაილის სახელი
        db.save_to_db(self.processor.df)  # მონაცემების ჩაწერა
        messagebox.showinfo("ბაზაში შენახვა", "მონაცემები ჩაიწერა ბაზაში.")
    def show_plot(self):
        """გრაფიკის ჩვენება — მწარმოებლების რაოდენობით"""
        self.processor.plot_top_makes()
    def threaded_summary(self):
        """შეჯამების ფაილში ჩაწერა — ცალკე ნაკადში"""
        run_threaded_summary(self.processor.df)
        messagebox.showinfo("შეჯამება", "შედეგები ჩაიწერება ფაილში (ფონურად).")