import requests
import sqlite3
import datetime

class Recipe:
    def __init__(self, db_filename):
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, recipe_name TEXT, recipe_category TEXT, recipe_country TEXT, recipe_instructions TEXT, timestamp TEXT)""")
        self.conn.commit()
        
    def fetch_recipe(self, rec):
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={rec}"
        
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                data = response.json()
                meals = data["meals"]
                if meals:
                    for meal in meals:
                        nm = meal['strMeal']
                        ctg = meal['strCategory']
                        ctr = meal['strArea']
                        instr = meal['strInstructions']
                        
                        print(f"{ctg}: {nm}({ctr})\n{instr}\n———")
                        self.save_history(nm, ctg, ctr, instr)
                else:
                    print("There is no found recipe.")
                    return None
            else:
                print(f"Error occured! {response.status_code}!")
                return None
        except requests.exceptions.ConnectionError:
            print("Connection lost! Check your internet!")
            return None
        
    def save_history(self, name, category, country, instructions):
        now = datetime.datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M")
        
        self.cursor.execute("INSERT INTO history(recipe_name, recipe_category, recipe_country, recipe_instructions, timestamp) VALUES(?, ?, ?, ?, ?)", (name, category, country, instructions, formatted))
        self.conn.commit()
        
    def show_history(self):
        self.cursor.execute("SELECT * FROM history ORDER BY id")
        history = self.cursor.fetchall()
        if history:
            print("\nHere is the history:")
            for row in history:
                print(f"{row[5]}\n{row[1]}, {row[2]}({row[3]})\n{row[4]}")
        else:
            print("There is no history!")
            return None
            
    def run(self):
        while True:
            print("\n ---Recipe--- \n")
            print("1. Search recipe.")
            print("2. Show history.")
            print("3. Quit.")
        
            while True:
                try:
                    answer = int(input("Choose the number: "))
                    break
                except ValueError:
                    print("That is not a number!")
            
            if answer == 1:
                recipe = input("Write the name of your dish: ")
                self.fetch_recipe(recipe)
            elif answer == 2:
                self.show_history()
            elif answer == 3:
                print("Bye!")
                break
            else:
                print("Invalid!")
            
    def close(self):
        self.conn.close()
        
if __name__ == "__main__":
    app = Recipe("recipe.db")
    app.run()
    app.close()