import os
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from collections import Counter
from collections import defaultdict
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

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
    total_water = aggregated_nutrients.get(255, 0)
    calcium = aggregated_nutrients.get(301, 0)
    phosphorus = aggregated_nutrients.get(305, 0)
    
    for food in response.get("foods", []):
        food_name = food.get("food_name", "Unknown")
        serving_qty = food.get("serving_weight_grams", 0)
        serving_unit = food.get("serving_unit", "g")
        calories = food.get("nf_calories", 0)
        
        # Calculate total weight and total calories
        total_weight += serving_qty
        total_calories += calories
        
        summary_items.append((f"{food_name} ({serving_qty}{serving_unit})", serving_qty))
    
    summary_items.sort(key=lambda x: x[1], reverse=True)
    sorted_summary_strings = [item[0] for item in summary_items]
    
    # Calculate caloric density and metabolizable energy using the NutrientCalculator class
    caloric_content_info = nutrient_calculator.calculate_calorie_content_me(aggregated_nutrients)
    me = caloric_content_info['metabolizable_energy']  
    caloric_content_me = caloric_content_info['caloric_content']  
    
    water_percentage = (total_water / total_weight) * 100 if total_weight > 0 else 0
    ca_p_ratio =calcium / phosphorus if phosphorus != 0 else 0
    
    st.subheader("Recipe Snapshot:")
    st.write(", ".join(sorted_summary_strings))

    # Create a DataFrame for the table
    table_data = {
        "": ["Serving size", "Metabolizable energy (ME)", "Calorie Content_ME", "Ca:P Ratio", "Moisture %"],
        "Value": [
            f"{total_weight:.2f} g", 
            f"{me:.2f} kcal",
            f"{caloric_content_me:.2f} kcal/kg",
            f"{ca_p_ratio:.2f}:1",
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
    
# 3. Display how each food contribute each calorie source
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

# 4.1 Comparison to AAFCO target
def display_nutrient_radar_chart(comparison_results, title, response=None, shrink=False):
    # ... [rest of the function code]
    
    # Extract nutrient names, actual values, and target values from comparison_results
    # Note: The values are already in logarithmic scale.
    nutrient_names = list(comparison_results.keys())
    actual_values = [comparison_results[nutrient]['Actual'] for nutrient in nutrient_names]
    target_values_adult = [comparison_results[nutrient]['Target Adult'] for nutrient in nutrient_names]
    target_values_puppy = [comparison_results[nutrient]['Target Puppy'] for nutrient in nutrient_names]
    
    # Create a DataFrame for actual values
    df_actual = pd.DataFrame(dict(
        r=actual_values + actual_values[:1],
        theta=nutrient_names + nutrient_names[:1]
    ))
    
    # Initialize the figure with actual values trace
    fig = px.line_polar(df_actual, r='r', theta='theta', line_close=True, line_shape='linear')
    fig.update_traces(fill='toself', line=dict(color='red'))  # Set color for Actual
    fig.data[0].name = 'Actual'
    
    # Add Target Adult trace
    target_adult_df = pd.DataFrame(dict(
        r=target_values_adult + target_values_adult[:1],
        theta=nutrient_names + nutrient_names[:1]
    ))
    fig.add_trace(go.Scatterpolar(r=target_adult_df['r'], 
                                  theta=target_adult_df['theta'], fill='toself', 
                                  line=dict(color='blue'), name='Target Adult'))
    
    # Add Target Puppy trace
    target_puppy_df = pd.DataFrame(dict(
        r=target_values_puppy + target_values_puppy[:1],
        theta=nutrient_names + nutrient_names[:1]
    ))
    fig.add_trace(go.Scatterpolar(r=target_puppy_df['r'], 
                                  theta=target_puppy_df['theta'], fill='toself', 
                                  line=dict(color='green'), name='Target Puppy'))
    
    # Add legend and title
    fig.update_layout(
        title=title,
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )
    
    # Display the radar chart in Streamlit
    st.plotly_chart(fig)

# 4.2 Display how each food contribute each target key (Heatmap)
def food_item_nutrient_chart(response, targets, title):

    # Initialize a dictionary to hold data
    food_data = {}
    
    # Iterate through each food item in the response
    for food in response.get("foods", []):
        food_name = food.get("food_name", "Unknown")
        
        # Initialize a dictionary for this food item
        food_data[food_name] = {}
        
        # Iterate through each target nutrient and calculate the quantity in this food item
        for target in targets:
            attr_id = target["attr_id"]
            aafco_nutrient = target["aafco_nutrient"]
            
            # Get the quantity of this nutrient in the current food item
            nutrient_quantity = next((nutrient.get("value", 0) \
                                      for nutrient in food.get("full_nutrients", []) \
                                      if nutrient.get("attr_id") == attr_id), 0)
            
            # Add the nutrient quantity to the food_data dictionary
            food_data[food_name][aafco_nutrient] = nutrient_quantity
    
    # Convert the nested dictionary to a DataFrame
    df = pd.DataFrame.from_dict(food_data, orient='index')
    df = df.sort_index(axis=1)
    
    # Create a heatmap, converting Pandas Index objects to lists
    fig = ff.create_annotated_heatmap(z=df.values, x=df.columns.tolist(), 
                                      y=df.index.tolist(), 
                                      annotation_text=df.values, colorscale='YlGnBu')
    fig.update_layout(title=title)
    st.plotly_chart(fig)


# 5.final UI presentation
def get_nutrient_info():
    st.title("Dog Food Formulator_nutritionix api")
    ingredients_input = st.text_area("Enter ingredient list:")
    
    # Add a checkbox for the manually added food item
    is_pea_protein_added = st.checkbox("Include 10g Organic Raw Sprouted Pea Protein")
    is_flaxseed_meal_added = st.checkbox("Include 3g Flaxseed Meal")
    is_nutritional_yeast_added = st.checkbox("Include 3g Nutritional Yeast") 
    
    # Create a Streamlit button to trigger the API call
    if st.button("Get nutrient info"):
        if ingredients_input or is_pea_protein_added:
            response = nutritionix_api.get_nutrients\
                                        (query=ingredients_input) \
                                        if ingredients_input else {"foods": []}
            
            # Checkbox to import mannually added nutrient value
            if is_pea_protein_added:
                pea_protein_data = constants.SPROUTED_PEA_PROTEIN_DATA
                response["foods"].append({"food_name": "10g Organic Raw Sprouted Pea Protein", 
                                          "full_nutrients": pea_protein_data})
            if is_flaxseed_meal_added:  
                flaxseed_meal_data = constants.FLAXSEED_MEAL_DATA
                response["foods"].append({"food_name": "3g Flaxseed Meal", 
                                          "full_nutrients": flaxseed_meal_data})
            if is_nutritional_yeast_added:  
                nutritional_yeast_data = constants.NUTRITIONAL_YEAST_DATA 
                response["foods"].append({"food_name": "5g Nutritional Yeast", 
                                          "full_nutrients": nutritional_yeast_data})
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
                    display_macronutrient_pie_chart(aggregated_nutrients)
                    
                food_item_calorie_chart(response)
                
                #3 Compare actual to target
                st.subheader("Comparison to AAFCO nutrient Profile")
                
                # AAFCO protein target
                chart_title_protein = "AAFCO target - Amino acid"
                comparison_results_protein = nutrient_calculator.compare_against_targets(
                                            aggregated_nutrients, constants.aafco_cc_protein_targets)
                display_nutrient_radar_chart(comparison_results_protein, chart_title_protein)
                food_item_nutrient_chart(response, \
                                         constants.aafco_cc_protein_targets, \
                                         'Nutrient Component: Amino acid')
                
                # AAFCO fat target
                chart_title_fat = "AAFCO target - Fatty acids"
                comparison_results_fat = nutrient_calculator.compare_against_targets(
                                            aggregated_nutrients, constants.aafco_cc_fat_targets)
                display_nutrient_radar_chart(comparison_results_fat, chart_title_fat)
                food_item_nutrient_chart(response, \
                                         constants.aafco_cc_fat_targets, \
                                         'Nutrient Component: Fats')

                # AAFCO mineral target
                st.subheader("AAFCO Target - Minerals")

                # Radar chart split
                chart_title_mineral = "AAFCO Target - Minerals"
                comparison_results_mineral = nutrient_calculator.\
                                            compare_against_targets(
                                            aggregated_nutrients, 
                                            constants.aafco_cc_mineral_targets)
               
                display_nutrient_radar_chart(comparison_results_mineral, \
                                             chart_title_mineral, response, shrink=True)

                food_item_nutrient_chart(response,\
                                        constants.aafco_cc_mineral_targets,
                                        'Nutrient Component: Vitamin') 
                
                
                # AAFCO vitamin target
                chart_title_v = "AAFCO Target - Vitamin"
                comparison_results_v = nutrient_calculator.\
                                        compare_against_targets(
                                        aggregated_nutrients, constants.aafco_cc_vitamin_targets)
                                        
                display_nutrient_radar_chart(comparison_results_v, \
                                             chart_title_v, response, shrink=True)
                
                food_item_nutrient_chart(response,\
                                        constants.aafco_cc_vitamin_targets,
                                        'Nutrient Component: Vitamin')
                

                #4 Display full details
                st.subheader("Full Details:")
                st.json(response)


# Call the function to get nutrient info based on user input
get_nutrient_info()
