import requests
import pandas as pd
from typing import Any, Dict, Optional, Union
from collections import Counter

class NutritionixAPI:
    BASE_URL = "https://trackapi.nutritionix.com"
    
    def __init__(self, app_id: str, app_key: str):
        self.app_id = app_id
        self.app_key = app_key
        self.headers = {
            'x-app-id': self.app_id,
            'x-app-key': self.app_key,
            'Content-Type': 'application/json'
        }
        self.id_to_name_mapping = self._load_id_to_name_mapping()

    def _load_id_to_name_mapping(self) -> Dict[int, str]:
        mapping_file_path = "data/Nutrition_mapping.csv"
        mapping_df = pd.read_csv(mapping_file_path)
        self.id_to_unit_mapping = dict(zip(mapping_df['attr_id'], mapping_df['unit']))
        return dict(zip(mapping_df['attr_id'], mapping_df['name']))


    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None,
                      data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], str]:
        """
        Makes a request to the Nutritionix API and returns the JSON response.
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(method, url, headers=self.headers, params=params, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            return response.text

    def get_nutrients(self, query: str) -> Union[Dict[str, Any], str]:
        """
        Get detailed nutrient breakdown of any natural language text.
        """
        endpoint = "/v2/natural/nutrients"
        data = {"query": query}
        return self._make_request("POST", endpoint, data=data)

    def search_instant(self, query: str) -> Union[Dict[str, Any], str]:
        """
        Populate any search interface with common foods and branded foods from Nutritionix.
        """
        endpoint = "/v2/search/instant"
        params = {"query": query}
        return self._make_request("GET", endpoint, params=params)

    def get_item(self, nix_item_id: str) -> Union[Dict[str, Any], str]:
        """
        Look up the nutrition information for any branded food item by the nix_item_id.
        """
        endpoint = "/v2/search/item"
        params = {"nix_item_id": nix_item_id}
        return self._make_request("GET", endpoint, params=params)

    def estimate_exercise(self, query: str, user_data: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], str]:
        """
        Estimate calories burned for various exercises using natural language.
        """
        endpoint = "/v2/natural/exercise"
        data = {"query": query, "user_data": user_data} if user_data else {"query": query}
        return self._make_request("POST", endpoint, data=data)

    def get_locations(self, lat: float, lng: float) -> Union[Dict[str, Any], str]:
        """
        Returns a list of restaurant locations near a given lat/long coordinate.
        """
        endpoint = "/v2/locations"
        params = {"ll": f"{lat},{lng}"}
        return self._make_request("GET", endpoint, params=params)

    
class NutrientCalculator:
    
    def __init__(self):
        # Initialize Atwater factors for dogs
        self.atwater_factors = {
            "protein": 3.5,
            "fat": 8.5,
            "carbohydrate": 3.5
        }
    
    def aggregate_nutrients(self, response):
        # Aggregate nutrient values based on attr_id
        aggregated_nutrients = Counter()
        total_calories = 0  # Initialize total_calories
        for food in response.get("foods", []):
            for nutrient in food.get("full_nutrients", []):
                attr_id = nutrient.get("attr_id")
                value = nutrient.get("value", 0)
                aggregated_nutrients[attr_id] += value
            total_calories += food.get("nf_calories", 0)  # Sum up the nf_calories for each food item
        aggregated_nutrients['total_calories'] = total_calories 
        return aggregated_nutrients

    
    def calculate_calorie_content_me(self, aggregated_nutrients):
        # Extract the macronutrients from the aggregated nutrients
        protein = aggregated_nutrients.get(203, 0)
        fat = aggregated_nutrients.get(204, 0)
        carbohydrate = aggregated_nutrients.get(205, 0) 
        
        # convert to calories per atwater_factor
        protein_me = protein * self.atwater_factors["protein"] 
        fat_me = fat * self.atwater_factors["fat"] 
        carbohydrate_me = carbohydrate * self.atwater_factors["carbohydrate"]
            
        metabolizable_energy = protein_me + fat_me + carbohydrate_me
        caloric_content = metabolizable_energy * 10  # kcal/kg

        
        return {
        "caloric_content": caloric_content,
        "protein_me": protein_me,
        "fat_me": fat_me,
        "carbohydrate_me": carbohydrate_me,
        "metabolizable_energy": metabolizable_energy}

    def display_top_10_nutrients(self, aggregated_nutrients, id_to_name_mapping, id_to_unit_mapping):
        nutrients_with_names_and_units = {
            id_to_name_mapping.get(attr_id, f"Unknown ({attr_id})"): 
                f"{value} {id_to_unit_mapping.get(attr_id, 'unit')}"
            for attr_id, value in aggregated_nutrients.items()
        }
        sorted_nutrients = sorted(
            nutrients_with_names_and_units.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
        top_10_nutrients = dict(sorted_nutrients[:10])
        return top_10_nutrients
    