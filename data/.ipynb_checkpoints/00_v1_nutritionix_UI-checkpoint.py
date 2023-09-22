import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import requests

# Load environment variables from .env file
load_dotenv("../Credential/.env")

def get_nutrition_info(recipe):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        'x-app-id': os.getenv('NUTRITIONIX_APP_ID'),
        'x-app-key': os.getenv('NUTRITIONIX_APP_KEY'),
        'Content-Type': 'application/json',
    }
    data = {
        'query': recipe,
        'timezone': 'Australia/Sydney',
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return None
 
def main():
    st.title('Nutrition Info')
    recipe_text = st.text_area('Enter your recipe (natural language):', height=200)
    if recipe_text:
        recipe = recipe_text.split('\n')
        serving_size = 1
        for line in recipe:
            if "Serving size:" in line:
                serving_size = int(line.split(":")[1].strip())
        nutrition_info = []
        images = []
        for ingredient in recipe:
            info = get_nutrition_info(ingredient)
            if info:
                nutrition_info.extend(info['foods'])
                response = requests.get(info['foods'][0]['photo']['thumb'])
                img = Image.open(BytesIO(response.content))
                images.append(img)
        if nutrition_info:
            totals = {
                'Weight (g)': 0,
                'Calories (kcal)': 0,
                'Fat (g)': 0,
                'Protein (g)': 0,
                'Carbs (g)': 0,
                'Fiber (g)': 0,
                'Vit A (µg)': 0,
                'Vit C (mg)': 0,
                'Vit D (µg)': 0,
                'Vit K (µg)': 0,
                'Calcium (mg)': 0,
                'Phosph. (mg)': 0,
            }
            data = []

            for item in nutrition_info:
                row = {
                    'Food': item['food_name'],
                    'Weight (g)': int(item['serving_weight_grams']),
                    'Calories (kcal)': int(item['nf_calories']),
                    'Fat (g)': int(item['nf_total_fat']),
                    'Protein (g)': int(item['nf_protein']),
                    'Carbs (g)': int(item['nf_total_carbohydrate']),
                    'Fiber (g)': int(item['nf_dietary_fiber']),
                    'Vit A (µg)': int(next((nutrient['value'] for nutrient in item['full_nutrients'] if nutrient['attr_id'] == 318), 1)),
                    'Vit C (mg)': int(next((nutrient['value'] for nutrient in item['full_nutrients'] if nutrient['attr_id'] == 401), 1)),
                    'Vit D (µg)': int(next((nutrient['value'] for nutrient in item['full_nutrients'] if nutrient['attr_id'] == 324), 1)),
                    'Vit K (µg)': int(next((nutrient['value'] for nutrient in item['full_nutrients'] if nutrient['attr_id'] == 430), 1)),
                    'Calcium (mg)': int(next((nutrient['value'] for nutrient in item['full_nutrients'] if nutrient['attr_id'] == 301), 1)),
                    'Phosph. (mg)': int(next((nutrient['value'] for nutrient in item['full_nutrients'] if nutrient['attr_id'] == 305), 1)),
                }

                for key in totals.keys():
                    if key in row:
                        totals[key] += row[key]
                data.append(row)
            totals['Food'] = 'Total'
            data.append(totals)
            df = pd.DataFrame(data)
            df = df[['Food', 'Weight (g)', 'Calories (kcal)', 'Fat (g)', 'Protein (g)', 'Carbs (g)', 'Fiber (g)', 
                     'Vit A (µg)', 'Vit C (mg)', 'Vit D (µg)', 'Vit K (µg)', 'Calcium (mg)', 'Phosph. (mg)']]
            df.index = np.arange(1, len(df) + 1)
            df.index.name = None

            # Sort the DataFrame by 'Weight (g)' column, except the last row
            sorted_data = df.iloc[:-1].sort_values('Weight (g)', ascending=False)

            # Append the totals row
            sorted_data = sorted_data.append(df.iloc[-1])

            df_styler = sorted_data.style.set_properties(**{'text-align': 'left'}).set_table_styles([
                dict(selector='th', props=[('text-align', 'left')]),
                dict(selector='caption', props=[('caption-side', 'bottom')]),
            ]).set_table_attributes('style="font-family: Arial; font-size: 14px"').hide_index()

            st.table(df_styler)

            # Display images in a grid-like format
            cols = st.columns(5)
            for i, image in enumerate(images):
                cols[i%5].image(image, width=100)

            # Stacked Bar Chart
            df_copy = df.copy()
            df_copy.drop(df_copy.tail(1).index, inplace=True)

            # Sort by 'Protein > Fat
            df_copy.sort_values(['Protein (g)', 'Fat (g)'], ascending=[False, False], inplace=True)
            fig = plt.figure(figsize=(10, 5))
            bar_l = np.arange(len(df_copy['Food']))
            ax = fig.add_axes([0,0,1,1])

            ax.barh(bar_l, df_copy['Carbs (g)'], color='#eab676', align='center')
            ax.barh(bar_l, df_copy['Protein (g)'], left=df_copy['Carbs (g)'], color='#a0e1e7', align='center')
            ax.barh(bar_l, df_copy['Fat (g)'], left=[i+j for i, j in zip(df_copy['Carbs (g)'], df_copy['Protein (g)'])], color='#C6259c', align='center')

            ax.legend(labels=['Carbs', 'Protein', 'Fat'])
            plt.title('Macronutrients Distribution per Ingredient')
            plt.xlabel('Macronutrients (grams)')
            plt.ylabel('Ingredients')

            # Setting the y-tick labels as the food names
            ax.set_yticks(bar_l)
            ax.set_yticklabels(df_copy['Food'])

            # Adding data source to the plot
            fig.subplots_adjust(bottom=0.2)
            plt.text(0.95, -0.1, 'Data source: Nutritionix', 
                    verticalalignment='bottom', horizontalalignment='right',
                    transform=fig.transFigure, color='grey', fontsize=10)

            st.pyplot(fig)

            # Convert grams of each macronutrient to calories
            fat_calories = totals['Fat (g)'] * 9
            protein_calories = totals['Protein (g)'] * 4
            carb_calories = totals['Carbs (g)'] * 4

            # Pie Chart
            fig1, ax1 = plt.subplots()
            sizes = [fat_calories, protein_calories, carb_calories]
            labels = 'Fat', 'Protein', 'Carbs'
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#C6259c', '#a0e1e7', '#eab676'])
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title('Sources of Calories')
            plt.text(0.95, 0.01, 'Data source: Nutritionix', 
                    verticalalignment='bottom', horizontalalignment='right',
                    transform=fig.transFigure, color='grey', fontsize=10)

            st.pyplot(fig1)
                
if __name__ == "__main__":
    main()
