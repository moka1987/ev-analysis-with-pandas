import tkinter as tk  # tkinter ბიბლიოთეკა
from gui import EVGUI  # ჩვენი გრაფიკული ინტერფეისის კლასი
def main():
    """აპლიკაციის მთავარი ფანჯრის შექმნა და გაშვება"""
    root = tk.Tk()          # tkinter-ის ფანჯარა
    app = EVGUI(root)       # ჩვენი ინტერფეისის ობიექტი
    root.mainloop()         # გრაფიკული ციკლის დაწყება
if __name__ == "__main__":
    main()  # პროგრამის გაშვების წერტილი
