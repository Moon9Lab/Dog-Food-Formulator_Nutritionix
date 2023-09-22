import os
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from nutritionix_api import NutritionixAPI
from collections import Counter
from collections import defaultdict


# Load API keys from .env file
load_dotenv("../Credential/.env")
app_id = os.getenv('NUTRITIONIX_APP_ID')
app_key = os.getenv('NUTRITIONIX_APP_KEY')

# Initialize the Nutritionix API client
nutritionix_api = NutritionixAPI(app_id=app_id, app_key=app_key)


def display_recipe_summary(response):
    # Create a summary of the recipe with food names and quantities
    summary_items = []
    total_weight = 0
    total_calories = 0
    total_water = 0  
    for food in response.get("foods", []):
        food_name = food.get("food_name", "Unknown")
        serving_qty = food.get("serving_weight_grams", 0)
        serving_unit = food.get("serving_unit", "g")
        calories = food.get("nf_calories", 0)
        
        # Calculate total weight and total calories
        total_weight += serving_qty
        total_calories += calories
        
        # Calculate total water content
        for nutrient in food.get("full_nutrients", []):
            if nutrient.get("attr_id") == 255:  # 255 is the attr_id for water
                total_water += nutrient.get("value", 0)
        
        summary_items.append((f"{food_name} ({serving_qty}{serving_unit})", serving_qty))
    
    # Sort summary_items based on serving_qty in descending order
    summary_items.sort(key=lambda x: x[1], reverse=True)
    
    # Extract the summary strings from the sorted list
    sorted_summary_strings = [item[0] for item in summary_items]
    
    # Calculate caloric density (in kcal/kg)
    caloric_density = (total_calories / total_weight) * 1000
    
    # Calculate Water content in percentage
    water_percentage = (total_water / total_weight) * 100
    
    # Display the recipe summary
    st.subheader("Recipe Snapshot:")
    st.write(", ".join(sorted_summary_strings))
    
    # Create a DataFrame for the table
    table_data = {
        "": ["Serving size", "Energy", "Caloric Density", "Water"],
        "Value": [f"{total_weight:.2f} g", f"{total_calories:.2f} Kcal", f"{caloric_density:.2f} kcal/kg", f"{water_percentage:.2f} %"]
    }
    table_df = pd.DataFrame(table_data)
    
    # Display the table in Streamlit
    st.table(table_df.set_index(""))

def aggregate_nutrients(response):
    # Aggregate nutrient values based on attr_id
    aggregated_nutrients = Counter()
    for food in response.get("foods", []):
        for nutrient in food.get("full_nutrients", []):
            attr_id = nutrient.get("attr_id")
            value = nutrient.get("value", 0)
            aggregated_nutrients[attr_id] += value
    return aggregated_nutrients    
    
def display_top_10_nutrients(aggregated_nutrients):
    # Translate attr_id to nutrient name and unit, and get the top 10 nutrients
    nutrients_with_names_and_units = {
        nutritionix_api.id_to_name_mapping.get(attr_id, f"Unknown ({attr_id})"): f"{value} {nutritionix_api.id_to_unit_mapping.get(attr_id, 'unit')}"
        for attr_id, value in aggregated_nutrients.items()
    }
    top_10_nutrients = dict(sorted(nutrients_with_names_and_units.items(), key=lambda item: item[1], reverse=True)[:10])
    
    # Display the top 10 nutrients alphabetically
    st.subheader("Top 10 Nutrients:")
    st.json({k: top_10_nutrients[k] for k in sorted(top_10_nutrients)})

def display_macronutrient_pie_chart(response):
    # Extract macronutrient data from the response
    carbohydrates = sum(food['nf_total_carbohydrate'] for food in response['foods'])
    proteins = sum(food['nf_protein'] for food in response['foods'])
    fats = sum(food['nf_total_fat'] for food in response['foods'])
    
    # Calculate caloric contribution of each macronutrient
    carbohydrate_calories = carbohydrates * 4
    protein_calories = proteins * 4
    fat_calories = fats * 9
    total_calories = carbohydrate_calories + protein_calories + fat_calories
    
    # Compute percentages
    sizes = [fat_calories, protein_calories, carbohydrate_calories]
    labels = ['Fats', 'Proteins', 'Carbohydrates']
    percentages = [(calories/total_calories)*100 for calories in sizes]
    
    # Define custom colors for each macronutrient
    colors = ['#B4217D', '#F0AB02', '#19A6B8']
    
    # Plotting the Pie chart with updated visual elements
    fig, ax = plt.subplots()
    ax.pie(sizes, colors=colors, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    plt.title('Sources of Calories')
    
    # Adding a legend with macronutrient name and its corresponding percentage
    legend_labels = [f'{label} {percentage:.1f}%' for label, percentage in zip(labels, percentages)]
    font_size = 10
    ax.legend(legend_labels,loc="lower right", bbox_to_anchor=(1.2, -0.01), fontsize=font_size, frameon=False)
    
    plt.text(1, -0.01, 'Data source: Nutritionix', 
             verticalalignment='bottom', horizontalalignment='right',
             transform=fig.transFigure, color='grey', fontsize=font_size)
    st.pyplot(fig)  
    
def get_nutrient_info():
    
    st.title("Nutritionix api")
    # Create a Streamlit text area for user input
    ingredients_input = st.text_area("Enter ingredient list:")

    # Create a Streamlit button to trigger the API call
    if st.button("Get nutrient info"):
        if ingredients_input:
            # Call the get_nutrients function of the NutritionixAPI class
            response = nutritionix_api.get_nutrients(query=ingredients_input)
            
            if isinstance(response, dict):
                # Display full details
                st.subheader("Full Details:")
                st.json(response)

                # Display the recipe summary
                display_recipe_summary(response)

                # Aggregate and display the top 10 nutrients
                aggregated_nutrients = aggregate_nutrients(response)
                
                # Create columns for Top 10 Nutrients and Pie Chart
                col1, col2 = st.columns(2)
                
                with col1:
                    display_top_10_nutrients(aggregated_nutrients)
                
                with col2:
                    display_macronutrient_pie_chart(response)
            else:
                st.write("Error:", response)
        else:
            st.warning("Please enter a list of ingredients.")

# Call the function to get nutrient info based on user input
get_nutrient_info()