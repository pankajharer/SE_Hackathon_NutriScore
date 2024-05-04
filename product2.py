from flask import Flask, request, jsonify, Response, render_template, send_file
from flask_cors import CORS
from pymongo import MongoClient
import cv2
from pyzbar import pyzbar
from bson import ObjectId
import barcode
from barcode.writer import ImageWriter
import numpy as np
import io

app = Flask(__name__)
CORS(app)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://Aditya:aditya@cluster0.9ex6qts.mongodb.net/")
db = client["SE_FINAL"]
collection = db["product"]

is_scanning = False
last_frame = None

# Sample data
sample_data = [
    {
        "product_id": "0123456789128",
        "name": "Instant Noodles",
        "image": "https://i.ibb.co/bFJ3pNz/pngwing-com.png",
        "brand": "Quick Meals Ltd.",
        "category": "Packed Food",
        "ingredients": ["Noodles", "Seasoning"],
        "allergens": [],
        "additives": ["Flavor enhancers", "Preservatives"],
        "nutritional_information": {
            "calories": 300,
            "negative": {
                "fat": 12,
                "saturated_fat": 6,
                "trans_fat": 0,
                "cholesterol": 0,
                "sodium": 800
            },
            "positive": {
                "carbohydrates": 40,
                "fiber": 2,
                "sugars": 2,
                "protein": 6,
                "vitamin_a": 0,
                "vitamin_c": 0,
                "calcium": 2,
                "iron": 8
            }
        },
        "price": 50.00
    },
    {
        "product_id": "0123456789129",
        "name": "Potato Chips",
        "image": "https://i.ibb.co/L9ptbjM/2.png",
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
    },
    {
        "product_id": "0123456789130",
        "name": "Canned Soup",
        "image": "https://i.ibb.co/6nX45CT/3.png",
        "brand": "SoupMaster Inc.",
        "category": "Packed Food",
        "ingredients": ["Water", "Vegetables", "Chicken", "Spices"],
        "allergens": ["Chicken"],
        "additives": ["Flavor enhancers", "Thickeners"],
        "nutritional_information": {
            "calories": 120,
            "negative": {
                "fat": 5,
                "saturated_fat": 1,
                "trans_fat": 0,
                "cholesterol": 5,
                "sodium": 800
            },
            "positive": {
                "carbohydrates": 10,
                "fiber": 2,
                "sugars": 3,
                "protein": 8,
                "vitamin_a": 40,
                "vitamin_c": 10,
                "calcium": 4,
                "iron": 6
            }
        },
        "price": 70.00
    },
    {
        "product_id": "0123456789131",
        "name": "Chocolate Bar",
        "image": "https://i.ibb.co/7VS61pR/4.png",
        "brand": "Sweet Delights Ltd.",
        "category": "Packed Food",
        "ingredients": ["Cocoa", "Sugar", "Milk", "Emulsifiers"],
        "allergens": ["Milk"],
        "additives": ["Emulsifiers", "Flavorings"],
        "nutritional_information": {
            "calories": 200,
            "negative": {
                "fat": 12,
                "saturated_fat": 7,
                "trans_fat": 0,
                "cholesterol": 5,
                "sodium": 20
            },
            "positive": {
                "carbohydrates": 25,
                "fiber": 1,
                "sugars": 20,
                "protein": 3,
                "vitamin_a": 2,
                "vitamin_c": 0,
                "calcium": 10,
                "iron": 4
            }
        },
        "price": 20.00
    },
    {
        "product_id": "0123456789132",
        "name": "Cereal Bars",
        "image": "https://images.kglobalservices.com/www.kelloggs.co.za/en_za/product/product_969493/prod_img-1428304_za_06001306002761_2204262126_p_1.png",
        "brand": "Healthy Snacks Inc.",
        "category": "Packed Food",
        "ingredients": ["Oats", "Honey", "Nuts", "Dried fruits"],
        "allergens": ["Nuts"],
        "additives": ["Sweeteners"],
        "nutritional_information": {
            "calories": 150,
            "negative": {
                "fat": 6,
                "saturated_fat": 1,
                "trans_fat": 0,
                "cholesterol": 0,
                "sodium": 50
            },
            "positive": {
                "carbohydrates": 20,
                "fiber": 4,
                "sugars": 10,
                "protein": 3,
                "vitamin_a": 0,
                "vitamin_c": 2,
                "calcium": 4,
                "iron": 6
            }
        },
        "price": 40.00
    },
    {
    "product_id": "7622201756697",
    "name": "Oreo Cookies",
    "image": "https://i.ibb.co/7VS61pR/4.png",
    "brand": "Oreo",
    "category": "Cookies",
    "ingredients": ["Wheat Flour", "Sugar", "Palm Oil", "Cocoa Powder", "Glucose Syrup", "Salt", "Leavening Agent (E500)", "Emulsifier (Soy Lecithin)", "Artificial Flavor (Vanillin)"],
    "allergens": ["Wheat", "Soy"],
    "additives": ["E500", "Soy Lecithin"],
    "nutritional_information": {
        "calories": 160,
        "negative": {
            "fat": 7,
            "saturated_fat": 3,
            "trans_fat": 0,
            "cholesterol": 0,
            "sodium": 75
        },
        "positive": {
            "carbohydrates": 21,
            "fiber": 1,
            "sugars": 13,
            "protein": 2,
            "vitamin_a": 0,
            "vitamin_c": 0,
            "calcium": 4,
            "iron": 6
        }
    },
    "price": 10
    }
]

# Function to generate barcode image and link it with product
def generate_and_link_barcode(product):
    barcode_data = str(product["product_id"])[-4:]
    output_filename = f"barcode_{barcode_data}.png"

    # Generate barcode image
    barcode_class = barcode.get_barcode_class('code128')
    barcode_instance = barcode_class(barcode_data, writer=ImageWriter())
    barcode_instance.save(output_filename)
    barcode_instance = str(barcode_instance)
    
    # Link barcode to product in the database
    collection.update_one({"product_id": product["product_id"]}, {"$set": {"barcode": barcode_instance}})

# Insert sample data and link each product with a barcode
for data in sample_data:
    existing_product = collection.find_one({"product_id": data["product_id"]})
    if not existing_product:
        collection.insert_one(data)
        generate_and_link_barcode(data)

def scan_barcode():
    global is_scanning
    is_scanning = True
    camera = cv2.VideoCapture(0)
    barcode_data = None

    while True:
        _, frame = camera.read()
        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            break

        if barcode_data:
            break

    camera.release()
    cv2.destroyAllWindows()

    return barcode_data

def get_product_info(barcode_data):
    product = collection.find_one({"barcode": barcode_data})
    if product:
        product['_id'] = str(product['_id'])
    return product







@app.route('/')
def index():
    return render_template('index.html')




@app.route('/scan', methods=['GET'])
def scan():
    global is_scanning
    barcode_data = scan_barcode()
    product_info = get_product_info(barcode_data)
    return jsonify({'productInfo': product_info})


if __name__ == '__main__':
    app.run(debug=True)