# constants.py

# Atwater Factors
atwater_factors = {
    "protein": 3.5,
    "carbohydrate": 3.5,
    "fat": 8.5,
}

# AAFCO Nutrient Profile target
aafco_cc_protein_targets = [
    #{"aafco_nutrient": "Protein", "attr_id": 203, "units per 1000 Kcal ME": "g", "Puppy & Growth": 9, "Adult": 7.2},
    {"aafco_nutrient": "Tryptophan", "attr_id": 501, "units per 1000 Kcal ME": "g", "Puppy & Growth": 0.50, "Adult": 0.40},
    {"aafco_nutrient": "Threonine", "attr_id": 502, "units per 1000 Kcal ME": "g", "Puppy & Growth": 2.60, "Adult": 1.20},
    {"aafco_nutrient": "Isoleucine", "attr_id": 503, "units per 1000 Kcal ME": "g", "Puppy & Growth": 1.78, "Adult": 0.95},
    {"aafco_nutrient": "Leucine", "attr_id": 504, "units per 1000 Kcal ME": "g", "Puppy & Growth": 3.23, "Adult": 1.70},
    {"aafco_nutrient": "Lysine", "attr_id": 505, "units per 1000 Kcal ME": "g", "Puppy & Growth": 2.25, "Adult": 1.58},
    {"aafco_nutrient": "Methionine", "attr_id": 506, "units per 1000 Kcal ME": "g", "Puppy & Growth": 0.88, "Adult": 0.83},
    {"aafco_nutrient": "Met-Cystine", "attr_id": 507, "units per 1000 Kcal ME": "g", "Puppy & Growth": 1.75, "Adult": 1.63},
    {"aafco_nutrient": "Phenylalanine", "attr_id": 508, "units per 1000 Kcal ME": "g", "Puppy & Growth": 2.08, "Adult": 1.13},
    {"aafco_nutrient": "Phe-Tyrosine", "attr_id": 509, "units per 1000 Kcal ME": "g", "Puppy & Growth": 3.25, "Adult": 1.85},
    {"aafco_nutrient": "Valine", "attr_id": 510, "units per 1000 Kcal ME": "g", "Puppy & Growth": 1.70, "Adult": 1.23},
    {"aafco_nutrient": "Arginine", "attr_id": 511, "units per 1000 Kcal ME": "g", "Puppy & Growth": 2.50, "Adult": 1.28},
    {"aafco_nutrient": "Histidine", "attr_id": 512, "units per 1000 Kcal ME": "g", "Puppy & Growth": 1.10, "Adult": 0.48},
]

aafco_cc_fat_targets = [
    #{"aafco_nutrient": "Crude Fat", "attr_id": 204, "units per 1000 Kcal ME": "g", "Puppy & Growth": 21.3, "Adult": 13.8},
    {"aafco_nutrient": "Linoleic acid", "attr_id": 675, "units per 1000 Kcal ME": "g", "Puppy & Growth": 3.3, "Adult": 2.8},
    {"aafco_nutrient": "PUFA 18:3 n-3 c,c,c (ALA)", "attr_id": 851, "units per 1000 Kcal ME": "g", "Puppy & Growth": 0.2, "Adult": 0.2},
    {"aafco_nutrient": "PUFA 20:5 n-3 (EPA)", "attr_id": 629, "units per 1000 Kcal ME": "g", "Puppy & Growth": 0.05, "Adult": 0.05},
    {"aafco_nutrient": "PUFA 22:6 n-3 (DHA)", "attr_id": 621, "units per 1000 Kcal ME": "g", "Puppy & Growth": 0.05, "Adult": 0.05}
]

aafco_cc_mineral_targets = [
    {"aafco_nutrient": "Calcium", "attr_id": 301, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 3000, "Adult": 1250,"Max":0.5},
    {"aafco_nutrient": "Phosphorus", "attr_id": 305, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 2500, "Adult": 1000},
    {"aafco_nutrient": "Potassium", "attr_id": 306, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 1500, "Adult": 1500},
    {"aafco_nutrient": "Sodium", "attr_id": 307, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 800, "Adult": 200},
    {"aafco_nutrient": "Magnesium", "attr_id": 304, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 150, "Adult": 150},
    {"aafco_nutrient": "Iron", "attr_id": 303, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 22, "Adult": 10},
    {"aafco_nutrient": "Copper", "attr_id": 312, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 3.1, "Adult": 1.83},
    {"aafco_nutrient": "Manganese", "attr_id": 315, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 1.8, "Adult": 1.25},
    {"aafco_nutrient": "Zinc", "attr_id": 309, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 25, "Adult": 20},
    {"aafco_nutrient": "Selenium", "attr_id": 317, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 90, "Adult": 80, "Max":500}
]

aafco_cc_vitamin_targets = [
    {"aafco_nutrient": "Vitamin A", "attr_id": 318, "units per 1000 Kcal ME": "IU", "Puppy & Growth": 1250, "Adult": 1250},
    {"aafco_nutrient": "Vitamin D", "attr_id": 324, "units per 1000 Kcal ME": "IU", "Puppy & Growth": 125, "Adult": 125},
    {"aafco_nutrient": "Choline", "attr_id": 421, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 340, "Adult": 340},
    {"aafco_nutrient": "Folic acid", "attr_id": 431, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 54, "Adult": 54},
    {"aafco_nutrient": "Thiamine", "attr_id": 404, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 0.56, "Adult": 0.56},
    {"aafco_nutrient": "Riboflavin", "attr_id": 405, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 1.3, "Adult": 1.3},
    {"aafco_nutrient": "Pantothenic acid", "attr_id": 410, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 3.0, "Adult": 3.0},
    {"aafco_nutrient": "Niacin", "attr_id": 406, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 3.4, "Adult": 3.4},
    {"aafco_nutrient": "Pyridoxine", "attr_id": 415, "units per 1000 Kcal ME": "mg", "Puppy & Growth": 0.38, "Adult": 0.38},
    {"aafco_nutrient": "Vitamin E", "attr_id": 323, "units per 1000 Kcal ME": "IU", "Puppy & Growth": 8.38, "Adult": 8.38},
    {"aafco_nutrient": "Vitamin B12", "attr_id": 578, "units per 1000 Kcal ME": "mcg", "Puppy & Growth": 7, "Adult": 7},
   
]

#Adds missing nutrient value

# 10g Sprouted Pea Protein
SPROUTED_PEA_PROTEIN_DATA = [
    {"aafco_nutrient": "Tryptophan", "attr_id": 501, "value": 0.099 / 2},
    {"aafco_nutrient": "Threonine", "attr_id": 502, "value": 0.4785 / 2},
    {"aafco_nutrient": "Isoleucine", "attr_id": 503, "value": 0.6105 / 2},
    {"aafco_nutrient": "Leucine", "attr_id": 504, "value": 1.089 / 2},
    {"aafco_nutrient": "Lysine", "attr_id": 505, "value": 0.8085 / 2},
    {"aafco_nutrient": "Methionine", "attr_id": 506, "value": 0.132 / 2},
    {"aafco_nutrient": "Phenylalanine", "attr_id": 508, "value": 0.7095 / 2},
    {"aafco_nutrient": "Valine", "attr_id": 510, "value": 0.6435 / 2},
]
# 3g Flaxseed meal
FLAXSEED_MEAL_DATA = [
    {"aafco_nutrient": "18:2 n-6 c,c(LA)", "attr_id": 675, "value": 0.18},
    {"aafco_nutrient": "18:3 n-3 c,c,c (ALA)", "attr_id": 851, "value": 0.68},
    {"aafco_nutrient": "PUFA 20:5 n-3 (EPA)", "attr_id": 629, "value": 0},
    {"aafco_nutrient": "PUFA 22:6 n-3 (DHA)", "attr_id": 621, "value": 0}
]

# 3g Nutritional Yeast
NUTRITIONAL_YEAST_DATA = [
    {"aafco_nutrient": "Sodium (mg)", "attr_id": 307, "value": 1.8},
    {"aafco_nutrient": "Thiamine HCl (B1)", "attr_id": 404, "value": 0.42},
    {"aafco_nutrient": "Riboflavin (B2)", "attr_id": 405, "value": 1.65},
    {"aafco_nutrient": "Niacin (B3)", "attr_id": 406, "value": 7.98},
    {"aafco_nutrient": "Pantothenic acid (B5)", "attr_id": 410, "value": 2.97},
    {"aafco_nutrient": "Pyridoxine (B6)", "attr_id": 415, "value": 0.69},
    {"aafco_nutrient": "Folic acid (B9)", "attr_id": 431, "value": 64.5},
    {"aafco_nutrient": "Cobalamin (B12)", "attr_id": 578, "value": 3.24}
]
