# Nutrition Info App

This is a simple web application to fetch and display nutrition information of food ingredients using the Nutritionix API. The app is developed with Python and Streamlit, and visualizes the data using pandas, matplotlib, and PIL. 

## Features

- Enter your food ingredients and get detailed nutrition information including weight, calories, macronutrients (fat, protein, carbohydrates), fiber, and vitamins (A, C, D, K), as well as minerals (calcium, phosphorus).
- Visualize the macronutrient distribution per ingredient with a stacked bar chart.
- See the total caloric distribution from macronutrients in a pie chart.
- View thumbnail images of your ingredients.

## Instructions

1. Clone the repository and navigate to the project directory.
2. Install the necessary Python packages listed in the `requirements.txt` file. You can do this by running `pip install -r requirements.txt`.
3. Set up your Nutritionix API credentials by creating a `.env` file in the project directory with the following structure:

    ```
    NUTRITIONIX_APP_ID=your_app_id
    NUTRITIONIX_APP_KEY=your_app_key
    ```

    Replace `your_app_id` and `your_app_key` with your actual Nutritionix app ID and app key.

4. Run the app by typing `streamlit run Nutritionix.py` in your terminal.

## Libraries Used

- Streamlit
- pandas
- numpy
- matplotlib
- Pillow
- requests
- json
- dotenv

## Notes

- This app is for educational purposes and is not intended for professional dietary advice.
- The app requires an API key from Nutritionix, which is subject to their terms and conditions. Make sure to understand and comply with those when using their API. 

I hope you find this app useful and enjoyable!
