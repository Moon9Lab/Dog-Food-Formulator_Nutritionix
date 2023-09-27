import os
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from collections import Counter
from collections import defaultdict
import seaborn as sns

# Importing necessary modules and functions from nutritionix_api.py
from nutritionix_api import NutritionixAPI, NutrientCalculator
import constants

# Load API keys from .env file
load_dotenv("../Credential/.env")
app_id = os.getenv('NUTRITIONIX_APP_ID')
app_key = os.getenv('NUTRITIONIX_APP_KEY')

# Initialize the Nutritionix_api client
nutritionix_api = NutritionixAPI(app_id=app_id, app_key=app_key)
nutrient_calculator = NutrientCalculator()

# 1. Create a summary of the recipe with food names and quantities
def display_recipe_summary(response):
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

# 2. Dsipaly pie chart for calorie source
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
    
# 4. Display how each food contribute each calorie source
def food_item_calorie_chart(response):
    # Initialize lists to hold data
    food_names = []
    proteins_list = []
    fats_list = []
    carbohydrates_list = []
    
    # Iterate through each food item in the response
    for food in response.get("foods", []):
        food_name = food.get("food_name", "Unknown")
        
        # Use Atwater factors to calculate the calorie content of each macronutrient
        proteins = food.get("nf_protein", 0) * constants.atwater_factors["protein"]
        fats = food.get("nf_total_fat", 0) * constants.atwater_factors["fat"]
        carbohydrates = food.get("nf_total_carbohydrate", 0) * constants.atwater_factors["carbohydrate"]
        
        # Append to lists
        food_names.append(food_name)
        proteins_list.append(proteins)
        fats_list.append(fats)
        carbohydrates_list.append(carbohydrates)
    
    # Create a DataFrame
    df = pd.DataFrame({
        'Proteins': proteins_list,
        'Fats': fats_list,
        'Carbohydrates': carbohydrates_list
    }, index=food_names)
    
    # Sort the DataFrame by Carbohydrates, Proteins, and Fats
    df = df.sort_values(by=['Proteins','Fats','Carbohydrates'], ascending=[False, False, False])
    
    # Plotting
    ax = df.plot(kind='barh', stacked=True, color=['#19A6B8','#B4217D','#F0AB02'])
    plt.title('Calories for Each Food Item')
    plt.ylabel('Food Items')
    plt.xlabel('Calories (kcal)')
    plt.legend(loc='upper right')
    
    # Display in Streamlit
    st.pyplot(ax.figure)

# 3.1 Comparison to AAFCO target
def display_nutrient_radar_chart(comparison_results, title):
    # Extract nutrient names, actual values, and target values from comparison_results
    nutrient_names = list(comparison_results.keys())
    actual_values = [comparison_results[nutrient]['Actual'] for nutrient in nutrient_names]
    target_values_adult = [comparison_results[nutrient]['Target Adult'] for nutrient in nutrient_names]
    target_values_puppy = [comparison_results[nutrient]['Target Puppy'] for nutrient in nutrient_names]
    
    # Compute angle for each axis in the radar chart
    num_vars = len(nutrient_names)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    # Repeat the first value to close the circle in radar chart
    actual_values += actual_values[:1]
    target_values_adult += target_values_adult[:1]
    target_values_puppy += target_values_puppy[:1]
    
    # Plot the radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, actual_values, color='red', alpha=0.25, label='Actual')
    ax.fill(angles, target_values_adult, color='blue', alpha=0.25, label='Target Adult')
    ax.fill(angles, target_values_puppy, color='green', alpha=0.25, label='Target Puppy')
    ax.plot(angles, actual_values, color='red', linewidth=2)
    ax.plot(angles, target_values_adult, color='blue', linewidth=2)
    ax.plot(angles, target_values_puppy, color='green', linewidth=2)
    
    # Label the axes with nutrient names
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(nutrient_names)
    
    # Add legend and title
    ax.legend(loc='upper right')
    plt.title(title)
    
    # Display the radar chart in Streamlit
    st.pyplot(fig)

# 3.2 Display how each food contribute each target key
# def food_item_nutrient_chart(response):
#     # Initialize a dictionary to hold data
#     food_data = {}
    
#     # Iterate through each food item in the response
#     for food in response.get("foods", []):
#         food_name = food.get("food_name", "Unknown")
        
#         # Initialize a dictionary for this food item
#         food_data[food_name] = {}
        
#         # Iterate through each target nutrient and calculate the quantity in this food item
#         for target in aafco_cc_protein_targets:
#             attr_id = target["attr_id"]
#             aafco_nutrient = target["aafco_nutrient"]
            
#             # Get the quantity of this nutrient in the current food item
#             nutrient_quantity = food.get("full_nutrients", {}).get(attr_id, 0)
            
#             # Add the nutrient quantity to the food_data dictionary
#             food_data[food_name][aafco_nutrient] = nutrient_quantity
    
#     # Convert the nested dictionary to a DataFrame
#     df = pd.DataFrame.from_dict(food_data, orient='index')
    
#     # Create a heatmap
#     plt.figure(figsize=(10, len(food_data)/2))  # Adjust size as needed
#     sns.heatmap(df, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Quantity'})
#     plt.title('Nutrient Composition for Each Food Item')
#     plt.ylabel('Food Items')
#     plt.xlabel('Nutrients')
    
#     # Display in Streamlit
#     st.pyplot(plt)



# 5.final UI presentation
def get_nutrient_info():
 
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
                
                #3 Compare actual to target
                st.subheader("Compare to AAFCO_nutrient Profile")
                comparison_results = nutrient_calculator.compare_against_targets(aggregated_nutrients)
                #food_item_nutrient_chart(response)
                
                # AAFCO protein target
                chart_title = "AAFCO Amino acid target"
                display_nutrient_radar_chart(comparison_results, chart_title) 
                
                #4 Display full details
                st.subheader("Full Details:")
                food_item_calorie_chart(response)
                st.json(response)

# Call the function to get nutrient info based on user input
get_nutrient_info()