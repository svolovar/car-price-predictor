import tkinter as tk
from tkinter import ttk


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Controller
        self.controller = None

        # Instructions label
        self.instructions = ttk.Label(self, text="Select the year, make, model, and miles to generate a price",
                                      font=('verdana', 12))
        self.instructions.grid(row=0, column=0, columnspan=3, pady=10, padx=30, sticky=tk.W)
        # Predicted price label
        self.price_label = ttk.Label(self, text='Suggested sale price: ', font=('verdana', 12))
        self.price_label.grid(row=2, column=0, columnspan=2, padx=30, sticky=tk.W)
        # Graphs and reports label
        self.graph_label = ttk.Label(self, text="Data visualizations and accuracy data for current database:",
                                     font=('verdana', 12))
        self.graph_label.grid(row=4, column=0, columnspan=3, padx=30, pady=(25, 10), sticky=tk.W)
        # Label that will show the calculated sale price
        self.price = tk.StringVar()
        self.price.set("-----")
        self.sale_price_label = ttk.Label(self, text="-----", font=('verdana', 12))
        self.sale_price_label.grid(row=2, column=1, columnspan=2, padx=(0, 5),sticky=tk.W)

        # Generate button
        self.generate_button = ttk.Button(self, text='Generate Price', command=self.generate_button_clicked, width=15)
        self.generate_button.grid(row=2, column=3, padx=(0,80), sticky=tk.E)
        # Graph 1 button
        self.graph_one_button = ttk.Button(self, text='Graph One', command=self.graph_one_button_clicked)
        self.graph_one_button.grid(row=5, column=0, padx=30, sticky=tk.W)
        # Graph 2 button
        self.graph_two_button = ttk.Button(self, text='Graph Two', command=self.graph_two_button_clicked)
        self.graph_two_button.grid(row=5, column=1, padx=10, sticky=tk.W)
        # Graph 3 button
        self.graph_three_button = ttk.Button(self, text='Graph Three', command=self.graph_three_button_clicked)
        self.graph_three_button.grid(row=5, column=2, padx=10, sticky=tk.W)
        # Model accuracy button
        self.accuracy_button = ttk.Button(self, text='Model Accuracy', command=self.accuracy_button_clicked)
        self.accuracy_button.grid(row=5, column=3, padx=10, sticky=tk.W)

        # Year combobox
        self.year_menu = ttk.Combobox(self, values=['Year'])
        self.year_menu.set("Year")
        self.year_menu.config(width=20)
        self.year_menu.grid(row=1, column=0, pady=10, padx=(30, 5), sticky=tk.W)

        # Make combobox
        self.make_menu = ttk.Combobox(self, values=['Make'])
        self.make_menu.set("Make")
        self.make_menu.bind("<<ComboboxSelected>>", self.make_combo_clicked)
        self.make_menu.config(width=20)
        self.make_menu.grid(row=1, column=1, padx=5, sticky=tk.W)

        # Model combobox
        self.model_menu = ttk.Combobox(self, values=['Model'])
        self.model_menu.set("Model")
        self.model_menu.config(width=20)
        self.model_menu.grid(row=1, column=2, padx=5, sticky=tk.W)

        # Mileage text entry
        self.input_mileage = tk.StringVar()
        self.input_mileage.set("Mileage")
        self.mileage_entry = tk.Entry(self, textvariable=self.input_mileage)
        self.mileage_entry.bind('<1>', self.mileage_entry_clicked)
        self.mileage_entry.config(width=20)
        self.mileage_entry.grid(row=1, column=3, padx=5, sticky=tk.W)

        # Table for displaying price calculations
        self.table = ttk.Treeview(self)
        self.table['columns'] = ('Entry ID', 'Year', 'Make', 'Model', 'Mileage', 'Price')
        self.id_num = 1
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("Entry ID", anchor=tk.W, width=50)
        self.table.column("Year", anchor=tk.W, width=80)
        self.table.column("Make", anchor=tk.W, width=80)
        self.table.column("Model", anchor=tk.W, width=80)
        self.table.column("Mileage", anchor=tk.W, width=80)
        self.table.column("Price", anchor=tk.W, width=110)
        self.table.heading('#0', text="Label", anchor=tk.W)
        self.table.heading('Entry ID', text="Entry ID", anchor=tk.W)
        self.table.heading("Year", text="Year", anchor=tk.W)
        self.table.heading("Make", text="Make", anchor=tk.W)
        self.table.heading("Model", text="Model", anchor=tk.W)
        self.table.heading("Mileage", text="Mileage", anchor=tk.W)
        self.table.heading("Price", text="Price", anchor=tk.W)
        self.table.grid(row=3, column=0, columnspan=6, pady=25)

    def set_controller(self, controller):
        self.controller = controller

    def generate_button_clicked(self):
        if self.controller:
            year = self.year_menu.get()
            make = self.make_menu.get()
            model = self.model_menu.get()
            mileage = self.mileage_entry.get()
            prediction = self.controller.generate_price(year, make, model, mileage)
            if (prediction == "Error: fields not complete") or (prediction == "Error: Mileage must be numbers only"):
                self.sale_price_label.config(text=prediction)
                return
            else:
                self.sale_price_label.config(text=prediction)
                self.table.insert('', 'end', iid=str(self.id_num), text='Parent',
                                  values=(str(self.id_num), year, make, model, mileage, prediction))
                self.id_num += 1

    def graph_one_button_clicked(self):
        if self.controller:
            g_one = self.controller.load_graph_one().get_tk_widget()
            g_one.grid(column=0, row=6, pady=20, columnspan=8)

    def graph_two_button_clicked(self):
        if self.controller:
            g_two = self.controller.load_graph_two().get_tk_widget()
            g_two.grid(column=0, row=6, pady=20, columnspan=8)

    def graph_three_button_clicked(self):
        if self.controller:
            g_three = self.controller.load_graph_three().get_tk_widget()
            g_three.grid(column=0, row=6, pady=20, columnspan=8)

    def accuracy_button_clicked(self):
        if self.controller:
            newWindow = tk.Toplevel()
            newWindow.title("Model report")
            newWindow.geometry("1000x1000")
            report_text = tk.Text(newWindow, width=800, height=800)
            for line in self.controller.load_accuracy():
                new_line = line + "'\n'"
                report_text.insert(tk.END, new_line)
            report_text.grid(column=0, row=0, pady=20)

    def populate_combobox(self, data, combobox):
        if self.controller:
            combobox.configure(value=())
            for item in data:
                combobox['values'] = tuple(list(combobox['values']) + [str(item)])

    def make_combo_clicked(self, event):
        # Update the "Models" combobox with models corresponding to the selected make
        if self.controller:
            if self.model_menu.get() != "Model":
                self.model_menu.configure(values=(['Model']))
                self.model_menu.set("Model")
                self.controller.load_models(self.make_menu.get())
            else:
                self.model_menu.configure(values=(['Model']))
                self.model_menu.set("Model")
                self.controller.load_models(self.make_menu.get())

    def mileage_entry_clicked(self, event):
        self.input_mileage.set('')
        self.mileage_entry.configure(textvariable=self.input_mileage)

