
import tkinter as tk
import pandas as pd


from controller import Controller
from model import Model
from view import View


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Car sale price generator')
        # create a model
        df_original = pd.read_csv('carvana.csv')
        column_names = ["Year", "Make", "Model", "Miles", "Price"]
        df_modified = pd.DataFrame(columns=column_names)
        # Populate the columns
        df_modified['Year'] = [int(x[:4]) for x in df_original['Year'].astype(str)]
        df_modified['Make'] = [x.split()[0] for x in df_original['Name']]
        df_modified['Model'] = df_original['Name'].str.split(n=1).str[1]
        df_modified['Miles'] = df_original['Miles']
        df_modified['Price'] = df_original['Price']
        model = Model(df_modified)

        # Generate predictive model for each make with and without model information
        model.generate_gradient_boost_model()
        # create a view and place it on the root window
        view = View(self)
        self.geometry("1050x1050")
        view.grid(row=0, column=0, padx=30, pady=20)
        # create a controller
        controller = Controller(model, view)
        # set the controller to view
        view.set_controller(controller)
        # populate combo boxes with data from csv
        # year
        view.populate_combobox(model.get_years(), view.year_menu)
        # make
        view.populate_combobox(model.get_all_makes(), view.make_menu)
        # Show a graph
        view.graph_one_button_clicked()


if __name__ == '__main__':
    app = App()
    app.mainloop()
