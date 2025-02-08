def calculate_nutrition_score(product_data):
    # Define weights for different nutritional factors
    positive_weights = {
    'protein': 2,
    'carbohydrates': 1,
    'fiber': 2,
    'sugars': -1,
    'calcium': 0.1,  # Decreasing weight for calcium
    'iron': 0.5  # Decreasing weight for iron
    }

    negative_weights = {
    'fat': 1,
    'saturated_fat': 2,
    'trans_fat': 3,
    'cholesterol': 2,
    'sodium': 0.01  # Decreasing weight for sodium
    }


    # Extract nutritional information from product data
    nutritional_data = product_data.get('nutritional_information', {})

    # Initialize positive and negative scores
    positive_score = 0
    negative_score = 0

    # Calculate positive score based on nutritional data and positive weights
    for nutrient, value in nutritional_data['positive'].items():

        if nutrient in positive_weights:
            #print(nutrient, value)
            #print (positive_weights[nutrient])
            positive_score += value * positive_weights[nutrient]

    # Calculate negative score based on nutritional data and negative weights
    for nutrient, value in nutritional_data['negative'].items():
        if nutrient in negative_weights:
            negative_score += value * negative_weights[nutrient]

    # Subtract negative score from positive score to get final score
    print(positive_score, negative_score)
    total_score = positive_score - negative_score

    # Constrain the score within the range of -15 to 40
    total_score = min(40, max(-15, total_score))

    # Return the total score
    return total_score

# Example product data
product_data =  {
        "product_id": "0123456789129",
        "name": "Potato Chips",
        "image": "https://img.freepik.com/free-photo/colorful-design-with-spiral-design_188544-9588.jpg",
        "brand": "Crunchy Snacks Inc.",
        "category": "Packed Food",
        "ingredients": ["Potatoes", "Vegetable oil", "Salt"],
        "allergens": [],
        "additives": ["Anti-caking agents"],
        "nutritional_information": {
            "calories": 160,
            "negative": {
                "fat": 10,
                "saturated_fat": 3,
                "trans_fat": 0,
                "cholesterol": 0,
                "sodium": 180
            },
            "positive": {
                "carbohydrates": 15,
                "fiber": 1,
                "sugars": 0,
                "protein": 2,
                "vitamin_a": 0,
                "vitamin_c": 10,
                "calcium": 0,
                "iron": 2
            }
        },
        "price": 30.00
}



# Calculate nutrition score
score = calculate_nutrition_score(product_data)
print("Nutrition Score:", score)
