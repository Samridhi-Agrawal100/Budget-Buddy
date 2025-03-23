import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import matplotlib.pyplot as plt
import ast
import os

# Define the main Tkinter window
root = tk.Tk()
root.title("Budget Buddy")
root.geometry("800x600")
root.configure(bg="#F7F5E6")

file = ""  


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# Sign up/Login Page
def signup():
    clear_screen()
    root.title("Sign Up / Login")

    def on_submit():
        global file
        userid = userid_entry.get()
        password = password_entry.get()

        try:
            with open('passdict.txt', 'r+') as fh:
                try:
                    passdict = ast.literal_eval(fh.read())
                except:
                    passdict = {}
                
                if userid in passdict:
                    if passdict[userid] == password:
                        file = f"{userid}.txt"
                        if not os.path.exists(file):
                            open(file, 'a+').close()
                        main_menu()
                    else:
                        messagebox.showerror("Error", "Incorrect Password!")
                else:
                    passdict[userid] = password
                    file = f"{userid}.txt"
                    open(file, 'a+').close()
                    fh.seek(0)
                    fh.truncate()
                    fh.write(str(passdict))
                    messagebox.showinfo("Welcome", f"Account created for {userid}!")
                    main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    tk.Label(root, text="User ID:", bg="#F7F5E6", font=("Arial", 14)).pack(pady=10)
    userid_entry = tk.Entry(root, font=("Arial", 14))
    userid_entry.pack()

    tk.Label(root, text="Password:", bg="#F7F5E6", font=("Arial", 14)).pack(pady=10)
    password_entry = tk.Entry(root, show="*", font=("Arial", 14))
    password_entry.pack()

    tk.Button(root, text="Login / Sign Up", command=on_submit, font=("Arial", 12), bg="#B5CDA3").pack(pady=20)

# View Expenses
def view_exp():
    clear_screen()
    root.title("View Expenses")

    frame = tk.Frame(root, bg="#F7F5E6")
    frame.pack(expand=True, fill='both', padx=20, pady=20)

    text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12))
    text_widget.pack(expand=True, fill='both')

    try:
        with open(file, "r") as fh2:
            data = fh2.readlines()
            if not data or data == ["\n"]:
                text_widget.insert(tk.END, "NO history found\n")
            else:
                for i in data:
                    temp = ast.literal_eval(i.strip("\n"))
                    week = temp[0]
                    text_widget.insert(tk.END, f"\nWeek is: {week}\n")
                    
                    for item in temp[1]:
                        if isinstance(item, list) and item[0] in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                            text_widget.insert(tk.END, f"\nDAY: {item[0]}\n")
                        elif isinstance(item, dict):
                            for key, value in item.items():
                                text_widget.insert(tk.END, f"{key}: {value}\n")
                    text_widget.insert(tk.END, "\n")
    except Exception as e:
        text_widget.insert(tk.END, f"Error reading expenses: {str(e)}\n")

    text_widget.config(state=tk.DISABLED)
    tk.Button(frame, text="Back to Menu", command=main_menu, font=("Arial", 12), bg="#B5CDA3").pack(pady=10)

# Add Expense
def add_exp():
    clear_screen()
    root.title("Add Expense")

    def on_add():
        try:
            item = item_entry.get().lower()
            amount = float(amount_entry.get())

            with open(file, "r+") as fh2:
                data = fh2.readlines()
                if not data or data == ["\n"]:
                    week_data = [['week1'], [['Monday'], {item: [amount]}]]
                    data2 = [week_data]
                else:
                    tk = data[-1]
                    dt = ast.literal_eval(tk.strip("\n"))
                    dk = dt[-1]
                    dtbm = dk[-1]
                    
                    if item in dtbm:
                        temp = dtbm[item]
                        temp.append(amount)
                        dtbm[item] = temp
                    else:
                        dtbm[item] = [amount]
                    
                    data2 = []
                    for i in data:
                        k = ast.literal_eval(i.strip("\n"))
                        data2.append(k)
                    data2[-1][-1][-1].update(dtbm)

                fh2.seek(0)
                fh2.truncate()
                for i in data2:
                    fh2.write(str(i) + "\n")

            messagebox.showinfo("Success", "Expense added successfully!")
            main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")

    frame = tk.Frame(root, bg="#F7F5E6")
    frame.pack(expand=True, padx=20, pady=20)

    tk.Label(frame, text="Add Expense", font=("Arial", 18, "bold"), bg="#F7F5E6").pack(pady=10)
    
    tk.Label(frame, text="Item Name:", bg="#F7F5E6", font=("Arial", 12)).pack()
    item_entry = tk.Entry(frame, font=("Arial", 12))
    item_entry.pack(pady=5)

    tk.Label(frame, text="Amount:", bg="#F7F5E6", font=("Arial", 12)).pack()
    amount_entry = tk.Entry(frame, font=("Arial", 12))
    amount_entry.pack(pady=5)

    tk.Button(frame, text="Add", command=on_add, font=("Arial", 12), bg="#A9D6E5").pack(pady=10)
    tk.Button(frame, text="Back to Menu", command=main_menu, font=("Arial", 12), bg="#B5CDA3").pack(pady=10)

# Day End
def day_end():
    try:
        now = datetime.datetime.now()
        with open(file, "r+") as fh2:
            data = fh2.readlines()
            data2 = [ast.literal_eval(line.strip("\n")) for line in data]
            a = len(data)
            
            for entry in data2:
                if entry[0] == [f"week{a}"]:
                    entry[1].append([now.strftime("%A")])
                    entry[1].append({'food': [0]})
            
            fh2.seek(0)
            fh2.truncate()
            for item in data2:
                fh2.write(str(item) + "\n")
        
        messagebox.showinfo("Success", "Day successfully ended")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to end day: {str(e)}")
    main_menu()

# Week End
def week_end():
    try:
        with open(file, "r+") as fh2:
            data = fh2.readlines()
            data2 = []
            a = len(data)
            
            for i in data:
                k = ast.literal_eval(i.strip("\n"))
                data2.append(k)
            data2.append(([f'week{a+1}'], [["Monday"], {"food": [0]}]))
            
            fh2.seek(0)
            fh2.truncate()
            for i in data2:
                fh2.write(str(i) + "\n")
        messagebox.showinfo("Success", "Week successfully ended")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to end week: {str(e)}")
    main_menu()

# Display Total
def disp_total():
    clear_screen()
    root.title("Display Total")

    frame = tk.Frame(root, bg="#F7F5E6")
    frame.pack(expand=True, padx=20, pady=20)

    text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12))
    text_widget.pack(expand=True, fill='both')

    def show_total():
        try:
            choice = int(choice_var.get())
            with open(file, "r") as fh2:
                data = fh2.readlines()
                
                if choice == 1:  # Day total
                    week = int(week_entry.get())
                    day = int(day_entry.get())
                    temp = ast.literal_eval(data[week-1].strip("\n"))
                    dk = temp[-1]
                    j = dk[day*2-1]
                    
                    total_sums = {}
                    for key, values in j.items():
                        total_sums[key] = sum(values)
                    
                    text_widget.delete(1.0, tk.END)
                    text_widget.insert(tk.END, f"Week: {week}    Day: {day}\n\n")
                    tos = 0
                    for key, total in total_sums.items():
                        text_widget.insert(tk.END, f"Total for '{key}': {total}\n")
                        tos += total
                    text_widget.insert(tk.END, f"\nTotal for the day: {tos}\n")

                elif choice == 2:  # Week total
                    week = int(week_entry.get())
                    temp = ast.literal_eval(data[week-1].strip("\n"))
                    dk = temp[-1]
                    
                    total_sums = {}
                    for j in dk:
                        if isinstance(j, list) and j[0] in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                            continue
                        for key, values in j.items():
                            if key not in total_sums:
                                total_sums[key] = 0
                            total_sums[key] += sum(values)
                    
                    text_widget.delete(1.0, tk.END)
                    text_widget.insert(tk.END, f"Week: {week}\n\n")
                    tos = 0
                    for key, total in total_sums.items():
                        text_widget.insert(tk.END, f"Total for '{key}': {total}\n")
                        tos += total
                    text_widget.insert(tk.END, f"\nTotal for the week: {tos}\n")

                elif choice == 3:  # Monthly total
                    text_widget.delete(1.0, tk.END)
                    week = 1
                    for i in data:
                        temp = ast.literal_eval(i.strip("\n"))
                        dk = temp[-1]
                        
                        total_sums = {}
                        for j in dk:
                            if isinstance(j, list) and j[0] in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                                continue
                            for key, values in j.items():
                                if key not in total_sums:
                                    total_sums[key] = 0
                                total_sums[key] += sum(values)
                        
                        text_widget.insert(tk.END, f"Week: {week}\n")
                        tos = 0
                        for key, total in total_sums.items():
                            text_widget.insert(tk.END, f"Total for '{key}': {total}\n")
                            tos += total
                        text_widget.insert(tk.END, f"Total for the week: {tos}\n\n")
                        week += 1

        except Exception as e:
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, f"Error: {str(e)}\n")

    control_frame = tk.Frame(frame, bg="#F7F5E6")
    control_frame.pack(pady=10)

    choice_var = tk.StringVar(value="1")
    tk.Radiobutton(control_frame, text="Daily Total", variable=choice_var, value="1", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(control_frame, text="Weekly Total", variable=choice_var, value="2", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(control_frame, text="Monthly Total", variable=choice_var, value="3", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)

    input_frame = tk.Frame(frame, bg="#F7F5E6")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Week:", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)
    week_entry = tk.Entry(input_frame, width=5)
    week_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(input_frame, text="Day:", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)
    day_entry = tk.Entry(input_frame, width=5)
    day_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(frame, text="Show Total", command=show_total, font=("Arial", 12), bg="#A9D6E5").pack(pady=10)
    tk.Button(frame, text="Back to Menu", command=main_menu, font=("Arial", 12), bg="#B5CDA3").pack(pady=10)

# Graph Analysis
def graph():
    clear_screen()
    root.title("Graph Analysis")

    def show_graph():
        try:
            choice = int(choice_var.get())
            with open(file, "r") as fh2:
                data = fh2.readlines()
                
                if choice == 1:  # Single day
                    week = int(week_entry.get())
                    day = int(day_entry.get())
                    tup = data[week-1]
                    dk = ast.literal_eval(tup.strip("\n"))
                    ds = dk[-1]
                    day_data = ds[day*2-1]
                    
                    plt.figure()
                    plt.plot(day_data.keys(),[sum(k) for k in day_data.values()])
                    plt.title(f"Expenses for Week {week}, Day {day}")
                    plt.grid(True)
                    plt.tight_layout()
                    
                    plt.savefig('day_graph.png')
                    plt.show()

                elif choice == 2:  # Weekly
                    week = int(week_entry.get())
                    tup = data[week-1]
                    dk = ast.literal_eval(tup.strip("\n"))
                    ds = dk[-1]
                    
                    labels = []
                    values = []
                    for item in ds:
                        if isinstance(item, dict):
                            for key, value in item.items():
                                labels.append(key)
                                values.append(sum(value))
                    
                    plt.figure()
                    plt.bar(labels, values)
                    plt.xticks(rotation=90)
                    plt.title(f"Weekly Expenses for Week {week}")
                    plt.savefig('week_graph.png')
                    plt.show()

                elif choice == 3:  # Monthly
                    plt.figure()
                    labels = []
                    values = []
                    for i, line in enumerate(data):
                        dk = ast.literal_eval(line.strip("\n"))
                        ds = dk[-1]
                        for item in ds:
                            if isinstance(item, dict):
                                for key, value in item.items():
                                    if key not in labels:
                                        labels.append(key)
                                        values.append(sum(value))
                                    else:
                                        index = labels.index(key)
                                        values[index] += sum(value)
                    patches, texts, autotexts =plt.pie(values, labels=labels,explode=[0.01]*len(values),pctdistance=1.2,labeldistance=1.38,autopct='%1.1f%%')
                    plt.setp(autotexts, size=9, weight="bold")
                    plt.setp(texts, size=10)

                    # Add some spacing around the plot
                    #plt.tight_layout()
                    plt.title("Monthly Expenses",fontsize=20,pad=30)
                    plt.savefig('month_graph.png')
                    plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate graph: {str(e)}")

    control_frame = tk.Frame(root, bg="#F7F5E6")
    control_frame.pack(pady=10)

    choice_var = tk.StringVar(value="1")
    tk.Radiobutton(control_frame, text="View Single Day", variable=choice_var, value="1", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(control_frame, text="Veiw Weekly", variable=choice_var, value="2", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(control_frame, text="Veiw Monthly", variable=choice_var, value="3", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)

    input_frame = tk.Frame(root, bg="#F7F5E6")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Week:", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)
    week_entry = tk.Entry(input_frame, width=5)
    week_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(input_frame, text="Day:", bg="#F7F5E6").pack(side=tk.LEFT, padx=5)
    day_entry = tk.Entry(input_frame, width=5)
    day_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(root, text="Show Graph", command=show_graph, font=("Arial", 12), bg="#A9D6E5").pack(pady=10)
    tk.Button(root, text="Back to Menu", command=main_menu, font=("Arial", 12), bg="#B5CDA3").pack(pady=10)

def main_menu():
    clear_screen()
    root.title("Budget Buddy")

    main_frame = tk.Frame(root, bg="#F7F5E6")
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    tk.Label(main_frame, text="Budget Buddy", font=("Arial", 24, "bold"), bg="#F7F5E6").pack(pady=20)

    tk.Button(main_frame, text="View Expenses", command=view_exp, font=("Arial", 14), bg="#A9D6E5").pack(pady=10)
    tk.Button(main_frame, text="Add Expense", command=add_exp, font=("Arial", 14), bg="#A9D6E5").pack(pady=10)
    tk.Button(main_frame, text="Day End", command=day_end, font=("Arial", 14), bg="#A9D6E5").pack(pady=10)
    tk.Button(main_frame, text="Week End", command=week_end, font=("Arial", 14), bg="#A9D6E5").pack(pady=10)
    tk.Button(main_frame, text="Display Total", command=disp_total, font=("Arial", 14), bg="#A9D6E5").pack(pady=10)
    tk.Button(main_frame, text="Graph Analysis", command=graph, font=("Arial", 14), bg="#A9D6E5").pack(pady=10)
    tk.Button(main_frame, text="Logout", command=signup, font=("Arial", 14), bg="#B5CDA3").pack(pady=10)

if __name__ == "__main__":
    signup()
    root.mainloop()

