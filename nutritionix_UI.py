import os
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from collections import Counter
from collections import defaultdict

# Importing necessary modules and functions from nutritionix_api.py
from nutritionix_api import NutritionixAPI, NutrientCalculator

# Load API keys from .env file
load_dotenv("../Credential/.env")
app_id = os.getenv('NUTRITIONIX_APP_ID')
app_key = os.getenv('NUTRITIONIX_APP_KEY')

# Initialize the Nutritionix_api client
nutritionix_api = NutritionixAPI(app_id=app_id, app_key=app_key)
nutrient_calculator = NutrientCalculator()
atwater_factors = {
    "protein": 3.5,
    "carbohydrate": 3.5,
    "fat": 8.5,
}

def display_recipe_summary(response):
    # Create a summary of the recipe with food names and quantities
    summary_items = []
    total_weight = 0
    total_water = 0
    total_calories = 0
    aggregated_nutrients = nutrient_calculator.aggregate_nutrients(response)
    
    for food in response.get("foods", []):
        food_name = food.get("food_name", "Unknown")
        serving_qty = food.get("serving_weight_grams", 0)
        serving_unit = food.get("serving_unit", "g")
        calories = food.get("nf_calories", 0)
        
        # Calculate total weight and total calories
        total_weight += serving_qty
        total_calories += calories
        
        # Calculate total water (attr_id == 255) 
        total_water += sum(nutrient.get("value", 0) \
                           for nutrient in food.get("full_nutrients", []) \
                           if nutrient.get("attr_id") == 255)
        
        summary_items.append((f"{food_name} ({serving_qty}{serving_unit})", serving_qty))
    
    summary_items.sort(key=lambda x: x[1], reverse=True)
    sorted_summary_strings = [item[0] for item in summary_items]
    
    # Calculate caloric density and metabolizable energy using the NutrientCalculator class
    caloric_content_info = nutrient_calculator.calculate_calorie_content_me(aggregated_nutrients)
    caloric_content_me = caloric_content_info['caloric_content']  
    
    water_percentage = (total_water / total_weight) * 100 if total_weight > 0 else 0

    st.subheader("Recipe Snapshot:")
    st.write(", ".join(sorted_summary_strings))

    # Create a DataFrame for the table
    table_data = {
        "": ["Serving size", "Gross Energy", "Calorie Content (ME)", "Moisture %"],
        "Value": [
            f"{total_weight:.2f} g", 
            f"{total_calories:.2f} Kcal",
            f"{caloric_content_me:.2f} kcal/kg",  # Using 'caloric_content_me' here
            f"{water_percentage:.2f} %"
        ]
    }

    table_df = pd.DataFrame(table_data)

    # Display the table in Streamlit
    st.table(table_df.set_index(""))


def display_macronutrient_pie_chart(aggregated_nutrients):
    # Extract data from calculate_calorie_content_me
    caloric_content_info = nutrient_calculator.calculate_calorie_content_me(aggregated_nutrients)
    protein_me = caloric_content_info['protein_me']
    fat_me = caloric_content_info['fat_me']
    carbohydrate_me = caloric_content_info['carbohydrate_me']
    metabolizable_energy = caloric_content_info['metabolizable_energy']
    
    # Compute percentages, handling NaN values
    sizes = [protein_me, fat_me, carbohydrate_me]
    percentages = [np.nan_to_num((calories / metabolizable_energy) * 100) for calories in sizes]
    
    # Define labels and custom colors for each macronutrient
    labels = ['Proteins', 'Fats', 'Carbohydrates']
    colors = ['#19A6B8','#B4217D','#F0AB02']
    

    # Plotting the Pie chart with updated visual elements
    labels_with_percentages = [
    f"{label} {percentage:.1f}%"
    for label, percentage in zip(labels, percentages)]

    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(percentages, colors=colors, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Sources of Calories')

    # Adjust the location of the legend and place it in the upper right corner without overlap
    ax.legend(labels_with_percentages, loc='upper right', bbox_to_anchor=(1.1, 1))

    st.pyplot(fig)

def get_nutrient_info():
    # UI presentation
    
    st.title("Nutritionix API")
    ingredients_input = st.text_area("Enter ingredient list:")
    
    # Create a Streamlit button to trigger the API call
    if st.button("Get nutrient info"):
        if ingredients_input:
            response = nutritionix_api.get_nutrients(query=ingredients_input)       
            if isinstance(response, dict):
                
                #1 recipe summary
                display_recipe_summary(response)

                #2 Aggregate and display the top 10 nutrients
                aggregated_nutrients = nutrient_calculator.aggregate_nutrients(response)
                top_10_nutrients = nutrient_calculator.display_top_10_nutrients(
                                    aggregated_nutrients,
                                    nutritionix_api.id_to_name_mapping,
                                    nutritionix_api.id_to_unit_mapping)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Top 10 Nutrients:")
                    st.json({k: top_10_nutrients[k] for k in sorted(top_10_nutrients)})

                with col2:
                    # Corrected the function call with the right parameters
                    display_macronutrient_pie_chart(aggregated_nutrients)

                # Display full details
                st.subheader("Full Details:")
                st.json(response)

# Call the function to get nutrient info based on user input
get_nutrient_info()