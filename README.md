

# CarClarity: PDF-Based Car Information Extraction and Analysis Tool

### Video : https://drive.google.com/file/d/1IknwSg99N8OvzW4FaOzzHRIthKsTjdXq/view?usp=drive_link

## Overview

# CarClarity is a tool designed to extract and analyze key information from car-related PDFs, providing structured insights from unstructured data. 
# It leverages a combination of frontend and backend technologies including HTML, Tailwind CSS, Python Flask, Matplotlib, Pandas, PyMongo, PyPDF2, and Transformers.

## Problem Statement

# Extracting and analyzing information from car-related PDFs is challenging due to the unstructured nature of the data. 
# CarClarity addresses this need by efficiently parsing PDFs, extracting relevant data, and providing structured insights.

## Solution Architecture

# CarClarity’s architecture consists of:

# Frontend: HTML, Tailwind CSS
# Backend: Python Flask
# Data Processing: Matplotlib, Pandas
# PDF Handling: PyPDF2
# NLP: Transformers
# Database: PyMongo

## Key Features

# PDF Upload: Users can upload car-related PDF files.
# Information Extraction: Extracts key details like car specifications, sales data.
# Data Analysis: Visualizes data using Matplotlib and Pandas.
# Structured Output: Provides JSON output.
# User Interface: Simple web interface for interaction.

## Technologies Used

# Frontend: HTML, Tailwind CSS
# Backend: Python Flask
# Data Visualization: Matplotlib, Pandas
# Database: PyMongo
# PDF Parsing: PyPDF2
# NLP: Transformers

## Workflow 

# The Document given by the user will be read using PyPDF2 , if it is PDF file. The text obtained will be classified using spacy which will be helpful for the Car sellers. The obtained JSON detail will be stored in MongoDB for future use. 
# The Dashboard enables the car sellers to get Statistical Analysis, as well as all the json details can be downloaded.
