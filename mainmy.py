import tkinter as tk
from tkinter import filedialog
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


e = 2.71828
x_exp = []
y_exp = []


def open_csv_file():
    global x_exp, y_exp
    # Prompt the user to select a CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    # Check if the user selected a file
    if file_path:

        # Read and process the data from the CSV file
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)

            for row in reader:
                x_exp.append(float(row[0]))
                y_exp.append(float(row[1]))
                # Process each row of data here (e.g., display it in the GUI or perform calculations)
                
        update_graph()

# надо вывести гамму которую получаем с Гуи
# Ughe equation
def ughe_calculation(gamma, Ut, Ul):
    # Calculate Ughe using the equation Ughe = gamma * Ut + (1 - gamma) * Ul
    Ughe = gamma * Ut + (1 - gamma) * Ul
    return Ughe

# Ul equation
def ul_velocity(y, V0, L):
    ul = 4 * V0 * y * (L - y) / (L**2)
    return ul

# Ut equation
def ut_velocity(y, V0, delta):
    ut = V0 * (1 - e ** (1 - e ** (y/delta)))
    return ut


# Function to update the graph
def update_graph():
    try:
        Gamma = entry4.get()
        V0 = float(entry2.get())
        L = float(entry1.get())
        delta = float(entry3.get())

        y_values = np.linspace(0, 0.5, 100)

        if Gamma:
            ul_profile = ul_velocity(y_values, V0, L)
            ut_profile = ut_velocity(y_values, V0, delta)
            ughe_profile = ughe_calculation(float(Gamma), ut_profile, ul_profile)

            plt.clf()  # Clear previous plot
            plt.plot(y_values, ut_profile, label='Ut', color="blue")
            plt.ylim(0, 1 + 0.05)
            plt.plot(y_values, ul_profile, label='Ul', color="green")
            plt.xlim(0, 0.5)
            plt.plot(y_values, ughe_profile, label='Ughe', color="red")
            plt.plot(x_exp, np.array(y_exp)/19.3743, label='Experiment', marker='o', color="blue", markersize=3)

            plt.xlabel('y-Distance from Channel Side')
            plt.ylabel('U- Velocity')
            plt.title('Ut and Ul solutions')
            plt.legend(loc="lower right")
            plt.grid(True)
        else:
            ul_profile = ul_velocity(y_values, V0, L)
            ut_profile = ut_velocity(y_values, V0, delta)

            plt.clf()  # Clear previous plot
            plt.plot(y_values, ut_profile, label='Ut', color="blue")
            plt.ylim(0, 1 + 0.05)
            plt.plot(y_values, ul_profile, label='Ul', color="green")
            plt.xlim(0, 0.5)
            plt.xlabel('y-Distance from Channel Side')
            plt.ylabel('U- Velocity')
            plt.title('Ut and Ul solutions')
            plt.legend(loc="lower right")
            plt.grid(True)

        # Update the plot
        canvas.draw()

    except ValueError:
        print("Please enter valid values in all fields.")


# Create the main application window
root = tk.Tk()
root.title("Ut and Ul solutions")

# Labels and Textfields
label1 = tk.Label(root, text="L:")
label1.grid(row=0, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

label2 = tk.Label(root, text="V0:")
label2.grid(row=1, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

label3 = tk.Label(root, text="Delta:")
label3.grid(row=2, column=0)
entry3 = tk.Entry(root)
entry3.grid(row=2, column=1)

label4 = tk.Label(root, text="Gamma:")
label4.grid(row=3, column=0)
entry4 = tk.Entry(root)
entry4.grid(row=3, column=1)

# Set default values for V0, L, and delta
entry2.insert(tk.END, "1.0")
entry1.insert(tk.END, "1.0")
entry3.insert(tk.END, "0.030")
entry4.insert(tk.END, "0.35")

# Buttons
def on_button_click():
    open_csv_file()

button = tk.Button(root, text="Open CSV File", command=on_button_click)
button.grid(row=6, column=0, columnspan=2, pady=10)

update_button = tk.Button(root, text="Update Graph", command=update_graph)
update_button.grid(row=4, column=0, columnspan=2, pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.grid(row=5, column=0, columnspan=2)

# Create a figure and canvas for the graph
fig = plt.figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=6)

# Start the GUI event loop
root.mainloop()