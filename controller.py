import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_models(self, make):
        models = []
        for model in self.model.get_all_models(make):
            if str(model) != "nan":
                models.append(str(model))
        models.append("Not listed")
        self.view.populate_combobox(models, self.view.model_menu)

    def generate_price(self, year, make, model, mileage):
        predicted_price = self.model.calculate_listing_price(year, make, model, mileage)
        return predicted_price

    def load_graph_one(self):
        plt.rcParams["figure.figsize"] = [10, 5]
        plt.rcParams["figure.autolayout"] = True
        canvas = FigureCanvasTkAgg(self.model.generate_graph_one(), master=self.view)
        canvas.draw()
        return canvas

    def load_graph_two(self):
        plt.rcParams["figure.figsize"] = [10, 5]
        plt.rcParams["figure.autolayout"] = True
        canvas = FigureCanvasTkAgg(self.model.generate_graph_two(), master=self.view)
        canvas.draw()
        return canvas

    def load_graph_three(self):
        plt.rcParams["figure.figsize"] = [10, 5]
        plt.rcParams["figure.autolayout"] = True
        canvas = FigureCanvasTkAgg(self.model.generate_graph_three(), master=self.view)
        canvas.draw()
        return canvas

    def load_accuracy(self):
        entries = self.model.generate_accuracy_report()
        # Add the overall averages and column names to the beginning of the report
        report = ["Overall average R2 score: " + str(entries[0]),
                  "Average R2 score when model is included in calculation: " + str(entries[1]),
                  "Average R2 score when model is not included in calculation: " + str(entries[2]),
                  "Index, Make, R2 Rating with model data, R2 Rating without model data, "
                  "R2 score with model data, R2 score without model data"
                  ]
        # Add the data for each manufacturer to the report
        line_number = 1
        for entry in entries[1:]:
            maker = entry[0]
            rw = entry[1]
            rwo = entry[2]
            r2w = str(entry[3])
            r2wo = str(entry[4])
            new_line = (str(line_number) + ": " + maker + ", " + rw + ", " + rwo + ", " + r2w + ", " + r2wo)
            report.append(new_line)
            line_number += 1
        return report
