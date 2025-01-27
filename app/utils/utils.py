from datetime import datetime
import requests
import os
import pandas as pd
from flask import current_app
import csv
import zipfile
import joblib

# Function to extract models if not already extracted
def extract_model(zip_path, extract_to):
    if not os.path.exists(extract_to):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(os.path.dirname(extract_to))

# Function to load model
def load_model(model_path):
    return joblib.load(model_path)


def get_timestamp():
    # Funcao que retorna time stamp atual.
    now = datetime.now()
    return now.strftime("%d/%m/%Y, %H:%M:%S")


# Function to fetch car images
def fetch_car_image(brand, trade_name):
    # Replace these with your actual API key and CSE ID
    api_key = "AIzaSyDnHUNpYQyvFzmDBswYR4ygLZ_kskkcHz8"
    cse_id = "90f8be4f8e9874169"

    search_query = f"{brand} {trade_name} car"
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": api_key,
        "cx": cse_id,
        "q": search_query,
        "searchType": "image",  # Fetch only images
        "num": 1  # Limit to the first result
    }

    try:
        response = requests.get(url, params=params)
        # print(f"API Request URL: {response.url}")  # Debugging
        # print(f"API Response Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            # print("Response:", data)
            if "items" in data and len(data["items"]) > 0:
                # Extract the first image URL
                return data["items"][0]["link"]
        print("No image found. Using placeholder.")
        return "https://via.placeholder.com/150"  # Default placeholder image
    except Exception as e:
        print(f"Error fetching image: {e}")
        return "https://via.placeholder.com/150"


def load_dataset(data_path):
    """
    Loads a dataset located in the 'data' directory.

    :param data_path: relative path to the dataset file.
    :return: pandas dataframe with dataset
    """
    data_dir = os.path.join(current_app.root_path, '../data/csv_datasets')
    file_path = os.path.join(data_dir, data_path)

    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset not found at {file_path}")
    except Exception as e:
        raise Exception(f"Error loading dataset: {e}")


def load_csv(file_path, selected_alternatives, alternatives_column_name):
    """
    Utility function to load a CSV file and return the dataset and columns.

    :param file_path: The full path to the CSV file
    :return: A tuple containing the dataset (list of rows) and column names
    """
    dataset = {}
    columns = []

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            columns = reader.fieldnames
            for row in reader:
                # dataset.append(row)
                if row[alternatives_column_name] in selected_alternatives:
                        dataset[row[alternatives_column_name]] = row
    except Exception as e:
        # print(f"Error loading CSV file: {e}")
        return {}, []

    # car_data = {}
    # all_columns = []
    #
    # # le dados do CSV
    # with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #
    #     # busca nomes de todas colunas
    #     all_columns = reader.fieldnames
    #     for row in reader:
    #         if row[alternatives_column] in selected_alternatives:
    #             car_data[row[alternatives_column]] = row

    return dataset, columns

def get_csv_column_names(file_path):
    """
    Utility function to load a CSV file and return the dataset and columns.

    :param file_path: The full path to the CSV file
    :return: A tuple containing the dataset (list of rows) and column names
    """
    dataset = {}
    all_columns_names = []

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            all_columns_names = reader.fieldnames

            dataset=reader
    except Exception as e:
        # print(f"Error loading CSV file: {e}")
        return []

    return dataset, all_columns_names
