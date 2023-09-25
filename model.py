
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


class Model:
    def __init__(self, car_data):
        self.car_data = car_data
        self.overall_accuracy = None
        self.accuracy_with_model = None
        self.accuracy_without_model = None
        self.report_with_model = []
        self.report_without_model = []

    def get_years(self):
        df_years = self.car_data['Year'].unique().tolist()
        year_list = []
        for year in df_years:
            year_list.append(int(year))
        year_list.sort()
        return year_list

    def get_all_makes(self):
        return self.car_data['Make'].unique()

    def get_all_models(self, make):
        df_make = self.car_data.query("Make == @make")
        return df_make['Model'].unique()

    def calculate_listing_price(self, year, make, model, mileage):
        make_miles = self.car_data.query("Make == @make")
        max_miles = make_miles['Miles'].max()

        if not str.isdigit(mileage):
            # Check if mileage entry contains anything besides digits
            prediction = "Error: Mileage must be numbers only"
            return prediction

        if (year == "Year") or (make == "Make") or (model == "Model"):
            # Check if each input field has a valid entry
            prediction = "Error: fields not complete"
        else:
            if model != "Not listed":
                # Use the data from input fields to create an entry that the model can use for a prediction
                input_car = pd.DataFrame({'Year': [year], 'Make': [make], 'Model': [model], 'Miles': [mileage]})
                # Get the prediction model that corresponds with the input data
                testing_model = Model.gradient_boost(self, make, True)[0]
                # Get the encoding data so the input car has columns that match the original encoding
                testing_dummies = Model.gradient_boost(self, make, True)[2]
                # Use the encoding data to reindex the entry created from the input data
                testing_columns = input_car.reindex(labels=testing_dummies.columns, axis=1, fill_value=0).drop(
                    columns=['Price'])
                # Predict the price of the car
                prediction = int(testing_model.predict(testing_columns))
                # Get confidence based on r2 score
                for item in self.report_with_model:
                    if item[0] == make:
                        confidence = item[2]
                        break
            else:
                # If the "Model" input is "Not listed", use the prediction model without "Model" data
                input_car = pd.DataFrame({'Year': [year], 'Miles': [mileage]})
                testing_model = Model.gradient_boost(self, make, False)[0]
                prediction = int(testing_model.predict(input_car))
                for item in self.report_without_model:
                    if item[0] == make:
                        confidence = item[2]
                        break
        # Assign a confidence value
        if prediction < 1000:
            # Predictions below $1000 are considered inaccurate
            confidence = "weak"
        if int(mileage) > int(max_miles):
            # If the input mileage is higher than the maximum mileage value in the dataset, the model can't make an
            # accurate prediction
            confidence = "out of range"

        prediction = "$" + str(prediction) + " " + "(" + confidence + ")"

        return prediction

    def generate_graph_one(self):
        # Average selling price by year
        years = self.get_years()
        avg_sale_price = []

        # Average sale price per year chronologically
        for year in years:
            query_year = str(year)
            year_sales = self.car_data.query("Year == @query_year")
            average = year_sales['Price'].mean()
            avg_sale_price.append(int(average))

        # Create a plot
        x = years
        y = avg_sale_price
        fig, ax = plt.subplots()
        ax.bar(x, y)
        plt.title("Average sale price by year")
        plt.xlabel("Year")
        plt.ylabel("Sale Price")
        return fig

    def generate_graph_two(self):
        # Average selling price by make
        makes = self.get_all_makes()
        avg_sale_prices = []

        for make in makes:
            df_make_sales = self.car_data.query("Make == @make")
            avg_price = df_make_sales['Price'].mean()
            avg_sale_prices.append(int(avg_price))

        # Create a plot
        x = makes
        y = avg_sale_prices
        fig, ax = plt.subplots()
        ax.bar(x, y)
        plt.title("Average selling price by manufacturer")
        plt.xlabel("Manufacturer")
        plt.xticks(rotation=90, ha='right')
        plt.ylabel("Average Sale Price")
        return fig

    def generate_graph_three(self):
        # Scatter plot of correlation between year, miles and price
        x = self.car_data['Miles']
        y = self.car_data['Price']
        fig, ax = plt.subplots()
        ax.scatter(x, y, c='red', s=1)
        plt.title("Correlation between mileage and sale price")
        plt.xlabel("Mileage")
        plt.xticks(ha='right')
        plt.ylabel("Sale price")
        return fig

    def encode(self, make):
        # Encode the columns and drop outliers
        # Load dataset
        df_maker = self.car_data.query('Make == @make')
        df_maker = df_maker.drop(columns=['Make'])
        # Remove outlier prices
        mean = df_maker["Price"].mean()
        deviation = df_maker["Price"].std()
        df_maker = df_maker[(df_maker['Year'] <= mean + (3*deviation))]
        # Encode 'model' column
        df_maker_encoded = pd.get_dummies(df_maker, columns=['Model'], drop_first=True)
        # Save the encoded columns so they can be used for prediction of a new entry
        x = df_maker_encoded
        return x

    def gradient_boost(self, make, model):
        # Generate a gradient boost regression model
        results = []

        if model:
            # Generate a prediction model that includes "model" data
            # Encode the model column
            data = Model.encode(self, make)
            dummies = data
            # Define dependent and independent variables
            x = data.drop('Price', axis=1)
            y = data['Price']
            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            # Create and train the Gradient Boosting model
            model_with = GradientBoostingRegressor()
            model_with.fit(X_train, y_train)
            # Test prediction model
            y_pred = model_with.predict(X_test)
            # Get the model's r2 score
            r2_with = r2_score(y_test, y_pred)
            # Save the prediction model, r2 score, and encoded columns
            results.append(model_with)
            results.append(r2_with)
            results.append(dummies)
        else:
            # Generate a prediction model that does not include "model" data
            data = self.car_data.query('Make == @make')
            data = data.drop(columns=['Make', 'Model'])
            # Define dependent and independent variables
            x = data.drop('Price', axis=1)
            y = data['Price']
            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            # Create and train the Gradient Boosting model
            model_without = GradientBoostingRegressor()
            model_without.fit(X_train, y_train)
            # Test the prediction model
            y_pred = model_without.predict(X_test)
            # Get the model's r2 score
            r2_without = r2_score(y_test, y_pred)
            # Save the prediction model and r2 score
            results.append(model_without)
            results.append(r2_without)
        return results

    def generate_gradient_boost_model(self):
        # list of all scores
        all_scores = []
        # list of scores with model info
        scores_with_model = []
        # list of scores without model info
        scores_without_model = []
        # list of makes with insufficient samples for accurate model
        insufficient = []
        # encoded columns
        dummies = None
        # Generate models for all makes (with model data)
        for make in self.get_all_makes():
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    # Generate a prediction model
                    model = Model.gradient_boost(self, make, True)
                    score_with = model[1]
                    dummies = model[2]
                    # Assign a confidence metric
                    if score_with < 0:
                        rating_with = "negative"
                    elif (score_with > 0) and (score_with < 0.3):
                        rating_with = "weak"
                        scores_with_model.append(score_with)
                        scores_with_model.append(dummies)
                        all_scores.append(score_with)
                    elif (score_with >= 0.3) and (score_with <= 0.7):
                        rating_with = "moderate"
                        scores_with_model.append(score_with)
                        scores_with_model.append(dummies)
                        all_scores.append(score_with)
                    elif score_with > 0.7:
                        rating_with = "strong"
                        scores_with_model.append(score_with)
                        scores_with_model.append(dummies)
                        all_scores.append(score_with)
                    # Save the model and relevant data
                    self.report_with_model.append([make, score_with, rating_with])
                except Warning:
                    # Separate the manufacturers with insufficient entries for an accurate prediction model
                    insufficient.append(make)

        # Generate models for all makes (without model data)
        for make in self.get_all_makes():
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    # Generate a prediction model
                    model = Model.gradient_boost(self, make, False)
                    score_without = model[1]
                    # Assign a confidence metric
                    if score_without < 0:
                        rating_without = "negative"
                    elif (score_without > 0) and (score_without < 0.3):
                        rating_without = "weak"
                        scores_without_model.append(score_without)
                        all_scores.append(score_without)
                    elif (score_without >= 0.3) and (score_without <= 0.7):
                        rating_without = "moderate"
                        scores_without_model.append(score_without)
                        all_scores.append(score_without)
                    elif score_without > 0.7:
                        rating_without = "strong"
                        scores_without_model.append(score_without)
                        all_scores.append(score_without)
                    # Save the model and relevant data
                    self.report_without_model.append([make, score_without, rating_without])
                except Warning:
                    pass

        # Calculate average r2 score with and without model
        sum_with = 0
        sum_without = 0
        len_with = 0
        len_without = 0
        for entry in self.report_with_model:
            rscore_with = entry[1]
            if rscore_with < 0:
                # Exclude negative r2 values
                sum_with += 0
            else:
                sum_with += rscore_with
                len_with += 1
        for entry in self.report_without_model:
            rscore_without = entry[1]
            if rscore_without < 0:
                sum_without += 0
            else:
                sum_without += rscore_without
                len_without += 1

        # Save the overall r2 averages
        self.overall_accuracy = (sum(all_scores)) / len(all_scores)
        self.accuracy_with_model = sum_with / len_with
        self.accuracy_without_model = sum_without / len_without
        return dummies

    def generate_accuracy_report(self):
        # First line of accuracy report contains overall averages
        entries = [[self.overall_accuracy, self.accuracy_with_model, self.accuracy_without_model]]
        # Subsequent lines contain data for each manufacturer
        for entry in self.report_with_model[1:]:
            make = entry[0]
            rating_with = entry[2]
            r2_with = entry[1]
            rating_without = None
            r2_without = None
            for item in self.report_without_model:
                if item[0] == entry[0]:
                    rating_without = item[2]
                    r2_without = item[1]
            entries.append([make, rating_with, rating_without, r2_with, r2_without])
        return entries
