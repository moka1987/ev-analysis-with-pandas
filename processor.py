import sqlite3
import pandas as pd
import threading
import matplotlib.pyplot as plt
# კლასები
class EVDataprocessor:
    """
    კლასი ახდენს მონაცემების ჩატვირთვას
    ატრიბუტები: filename: ფაილის სახელი, df: მონაცემების DataFrame ობიექტი
    """
    def __init__(self, filename): #კონსტრუქტორი
        self.filename=filename
        self.df=None
    def load_data(self):
        """CSV ფაილკის ჩატვირთვა pandas-ის გამოყენებით"""
        try:
            self.df=pd.read_csv(self.filename)
            print("[INFO] მონაცემები ჩაიტვირთა წარმატებით.")
        except FileNotFoundError:
            print("[ERROR] CSV ფაილი ვერ მოიძებნა.")
        except Exception as e:
            print(f"[ERROR] შეცდომა: {e}.")
    def clean_data(self):
        """მონაცემების გასუფთავება"""
        if self.df is not None:
            self.df.dropna(subset=["Make", "Model", "City", "Electric Vehicle Type"], inplace=True)
            self.df["Make"]=self.df["Make"].str.strip().str.upper()
            self.df["City"]=self.df["City"].str.strip().str.title()
            print(f"[INFO] მონაცემები გასუფთავდა.")
        else:
            print("მონაცემები არ არის ჩატვირთული.")
    def get_top_makes(self, n=10):
        """აბრუნებს ყველაზე გავრცელებულ მწარმოებელს"""
        if self.df is not None:
            return self.df["Make"].value_counts().head(n)
        return pd.Series()
class SQLiteManager:
    """კლასი ინახავს ინფორმაციას მონაცემთა ბაზაში"""
    def __init__(self, db_name):
        self.db_name=db_name
    def save_to_db(self, df, table_name="ev_data"):
        """მონაცემების ჩასმა SQLite ბაზაში"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"[INFO] მონაცემები ჩაიწერა ბაზაში: {self.db_name}")
        except Exception as e:
            print(f"[ERROR] ბაზაში ჩაწერისას მოხდა შეცდომა: {e}.")
class EnhancedProcessor(EVDataprocessor):
    """
    კლასი, რომელიც მოიცავს ვიზუალიზაციასაც.
    მემკვიდრეობით იღებს EVDataProcessor-ს.
    """
    def plot_top_makes(self, n=10):
        """მთავარი მწარმოებლების დიაგრამა"""
        top=self.get_top_makes(n)
        if not top.empty:
            top.plot(kind="bar", color="cornflowerblue", title="Top EV Makes")
            plt.xlabel("Make")
            plt.ylabel("Count")
            plt.tight_layout()
            plt.grid(True)
            plt.show()
def save_summary_to_file(df):
    """შედეგების ჩაწერა ფაილში – ტოპ მწარმოებლები"""
    try:
        summary = df["Make"].value_counts().head(10)
        with open("top_makes.txt", "w", encoding="utf-8") as f:
            f.write("Top 10 EV Makers:\n")
            f.write(summary.to_string())
        print("[INFO] შედეგები ჩაიწერა top_makes.txt ფაილში.")
    except Exception as e:
        print(f"[ERROR] ფაილში ჩაწერისას მოხდა შეცდომა: {e}")
def run_threaded_summary(df):
    """შედეგების ჩაწერა ცალკე ნაკადში"""
    t = threading.Thread(target=save_summary_to_file, args=(df,))
    t.start()