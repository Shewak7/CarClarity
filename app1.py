from flask import Flask, render_template, request, send_file
from mongodb import Collection
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import json
from PyPDF2 import PdfWriter
import PyPDF2
from PIL import Image
import spacy
import re

app = Flask(__name__)

def readtext(textfile):
    with open(textfile, 'r') as file:
        conversation = file.read()
    return conversation

def readPDF(pdffile):
    text = ""
    with open(pdffile, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def extract_information(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    # Initialize extraction results
    extracted_info = {
        "Customer Requirements": {
            "Car Type": None,
            "Fuel Type": None,
            "Color": None,
            "Distance Travelled": None,
            "Make Year": None,
            "Transmission Type": None
        },
        "Company Policies": {
            "Free RC Transfer": None,
            "5-Day Money Back Guarantee": None,
            "Free RSA for One Year": None,
            "Return Policy": None
        },
        "Customer Objections": {
            "Refurbishment Quality": None,
            "Car Issues": None,
            "Price Issues": None,
            "Customer Experience Issues": None
        }
    }

    # Define patterns for extraction
    patterns = {
        "Car Type": ["Hatchback", "SUV", "Sedan"],
        "Fuel Type": ["Diesel", "Petrol", "Electric"],
        "Color": ["White", "Black", "Red", "Blue", "Silver", "Grey"],
        "Distance Travelled": r"\b\d{1,4}\s*(?:km|miles)\b",
        "Make Year": r"\b(20\d{2})\b",
        "Transmission Type": ["Automatic", "Manual"],
        "Company Policies": ["Free RC Transfer", "5-Day Money Back Guarantee", "Free RSA for One Year", "Return Policy"],
        "Customer Objections": ["Refurbishment Quality", "Car Issues", "Price Issues", "Customer Experience Issues"]
    }

    # Extract car requirements
    for requirement, keywords in patterns.items():
        if requirement in ["Car Type", "Fuel Type", "Color", "Transmission Type"]:
            for token in doc:
                if token.text in keywords:
                    extracted_info["Customer Requirements"][requirement] = token.text
        elif requirement == "Distance Travelled":
            match = re.search(patterns[requirement], text)
            if match:
                extracted_info["Customer Requirements"][requirement] = match.group()
        elif requirement == "Make Year":
            match = re.search(patterns[requirement], text)
            if match:
                extracted_info["Customer Requirements"][requirement] = match.group()

    # Extract company policies
    for policy in patterns["Company Policies"]:
        if policy in text:
            extracted_info["Company Policies"][policy] = True

    # Extract customer objections
    for objection in patterns["Customer Objections"]:
        if objection in text:
            extracted_info["Customer Objections"][objection] = True

    return extracted_info
    

def insert_data(data):
    Collection.insert_one(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        textFile = request.form.get('textFileInput')
        pdfFile = request.form.get('pdfInput')

        if textFile:
            conversation = readtext(textFile)
            extracted_info = extract_information(conversation)
            insert_data(extracted_info)
            
        if pdfFile:
            conversation = readPDF(pdfFile)
            extracted_info = extract_information(conversation)
            insert_data(extracted_info)

    return render_template('home.html')


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        data = list(Collection.find())  # Replace with your actual data retrieval method
        Btn = request.form.get('Btn')
        
        if Btn == "jsonBtn":
            json_data = json.dumps(data, default=str, indent=4)
            with open('car.json', 'w') as json_file:
                json_file.write(json_data)
            return send_file('car.json', as_attachment=True)
        
        elif Btn == "reportBtn":
            df = pd.DataFrame(data)
            req = df['CustomerRequirements']
            obj = df['CustomerObjections']

            carType = req.apply(lambda x: x['CarType']).value_counts()
            fuelType = req.apply(lambda x: x['FuelType']).value_counts()
            color = req.apply(lambda x: x['Color']).value_counts()
            makeYear = req.apply(lambda x: x['MakeYear']).value_counts()
            transmissionType = req.apply(lambda x: x['TransmissionType']).value_counts()

            carIssues = obj.apply(lambda x: x['CarIssues']).value_counts()
            priceIssues = obj.apply(lambda x: x['PriceIssues']).value_counts()
            refurbishmentQuality = obj.apply(lambda x: x['RefurbishmentQuality']).value_counts()

            # First Figure with Car Types and Fuel Types
            plt.figure(figsize=(14, 5))
            plt.subplot(1, 2, 1)
            plt.title("Car Types")
            plt.pie(carType, labels=carType.index, autopct='%1.1f%%')

            plt.subplot(1, 2, 2)
            plt.title("Fuel Types")
            plt.pie(fuelType, labels=fuelType.index, autopct='%1.1f%%')

            plt.suptitle('Car Types and Fuel Types')
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig('car_type_fuel.png')

            # Second Figure with Car Colours and Transmission Types
            plt.figure(figsize=(14, 5))
            plt.subplot(1, 2, 1)
            plt.title("Car Colours")
            plt.pie(color, labels=color.index, autopct='%1.1f%%')

            plt.subplot(1, 2, 2)
            plt.title("Transmission Types")
            plt.pie(transmissionType, labels=transmissionType.index, autopct='%1.1f%%')

            plt.suptitle('Car Colours and Transmission Types')
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig('car_color_transmission.png')

            # Third Figure with Distance Travelled and Manufacturing Year
            plt.figure(figsize=(14, 5))
            plt.title("Manufacturing Year")
            plt.bar(makeYear.index, makeYear)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig('car_manufacture.png')


            plt.figure(figsize=(14, 5))
            plt.title("Car Issues")
            wedges, texts, autotexts = plt.pie(carIssues, autopct='%1.1f%%')
            plt.legend(wedges, carIssues.index, title="Car Issues", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig('car_issue.png')

            plt.figure(figsize=(14, 5))
            plt.title("Price Issues")
            wedges, texts, autotexts = plt.pie(priceIssues, autopct='%1.1f%%')
            plt.legend(wedges, priceIssues.index, title="Price Issues", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig('price.png')

            plt.figure(figsize=(14, 5))
            plt.title("RefurbishmentQuality")
            wedges, texts, autotexts = plt.pie(refurbishmentQuality, autopct='%1.1f%%')
            plt.legend(wedges, refurbishmentQuality.index, title="Refurbishment Quality", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            plt.savefig('refurb.png')

            # Create a PDF and combine the images into the PDF using PyPDF2
            pdf_writer = PdfWriter()

            for image_file in ['car_type_fuel.png', 'car_color_transmission.png', 'car_manufacture.png','car_issue.png','refurb.png','price.png']:
                image = Image.open(image_file)
                pdf_image = image.convert('RGB')
                pdf_image.save(f"{image_file.replace('.png', '.pdf')}")
                pdf_writer.append(f"{image_file.replace('.png', '.pdf')}")

            pdf_file = "car_report.pdf"
            with open(pdf_file, "wb") as output_pdf:
                pdf_writer.write(output_pdf)

            # Send the PDF file as a download
            return send_file(pdf_file, as_attachment=True)

    return render_template('dashboard.html')  

        
    return render_template('dashboard.html')

if __name__ =='__main__':
    app.run(debug=True)