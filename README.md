
# Dog Food Formulator using Nutritionix API

This project utilizes the Nutritionix API to analyze nutrient content in dog food recipes and compares them to the AAFCO dog food nutrient profiles.

## Features

- **Recipe Analysis:** Break down nutrient content of user-input recipes.
- **Comparison with AAFCO Nutrient Profiles:** Visualize how the nutrient content of a recipe compares with AAFCO nutrient profiles using radar charts and heatmaps.
- **Detailed Nutrient Breakdown:** Explore detailed nutrient breakdown for each ingredient and the entire recipe.

## Requirements

- Python 3.x
- Streamlit
- Plotly
- Requests
- Pandas

## Setup & Running the Application

1. Clone the repository:
   ```shell
   git clone [repo-link]
   ```
2. Install the dependencies:
   ```shell
   pip install -r requirements.txt
   ```
3. Obtain API credentials from [Nutritionix](https://developer.nutritionix.com/) and set them in `nutritionix_api.py`.
4. Run the application using Streamlit:
   ```shell
   streamlit run nutritionix_UI.py
   ```

## Usage Instructions

1. Input your ingredients into the provided text area.
2. Select additional options if desired (e.g., including specific protein sources).
3. Click "Get nutrient info" to retrieve and display the nutrient data.

## Future Enhancements

In the pipeline for future development is the integration of the USDA food database, aiming to cross-validate nutrient data obtained from the Nutritionix API, thereby bolstering the reliability and comprehensiveness of nutrient analysis by amalgamating data from diverse sources. Other anticipated enhancements include the introduction of a user authentication system to facilitate recipe and nutrient analysis saving, the generation of recipe adjustment suggestions for alignment with AAFCO nutrient profiles, the expansion to accommodate nutrient analysis for various pets, improvements in data visualization and interactivity, the incorporation of diverse unit inputs with automated conversions, and the capability to export analytical data and visuals in various formats for offline utilization and sharing.


## License
This project is distributed under the MIT License. 

## Acknowledgments

- **Nutritionix API:** For providing comprehensive nutrient data.
- **AAFCO:** For establishing nutrient profiles and guidelines.
