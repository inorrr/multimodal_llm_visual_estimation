"""
Python Script Disclaimer

Date: Dec 1, 2024
Author: Yinuo Zhao
Purpose: This script is designed to select random images from a specified directory, copy them to a new directory, and update a CSV file with image class and annotation details. It is intended for academic and research purposes to assist in data processing and analysis.
Project: Improving Multi-modal Language Model on Object Counting with Self-Generated Side Information

Note: This script is provided 'as is' without warranty. The user assumes all responsibility for its use and the results thereof. Please verify all outputs and data for accuracy.

"""

import random
import os
import shutil
import csv
import json
import pandas as pd

source_folder = 'FSC147_384_V2/images_384_VarV2'
destination_folder = 'FSC147_384_V2/selected_300_images'
source_txt_path = 'FSC147_384_V2/ImageClasses_FSC147.txt'
destination_csv_path = 'FSC147_384_V2/300_image_labels.csv'
annotation_json_path = 'FSC147_384_V2/annotation_FSC147_384.json'


def select_random_300_images():
    random.seed(42)

    with open(source_txt_path, 'r') as file:
        valid_images = [line.split('\t')[0] for line in file if '\t' in line and os.path.exists(os.path.join(source_folder, line.split('\t')[0]))]

    if len(valid_images) < 300:
        raise ValueError(f"Not enough images with classes. Required: {300}, available: {len(valid_images)}")

    selected_filenames = random.sample(valid_images, 300)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in selected_filenames:
        shutil.copy(os.path.join(source_folder, filename), os.path.join(destination_folder, filename))

    return selected_filenames


def create_class_file_for_selected_images(selected_filenames):

    with open(source_txt_path, 'r') as file:
        lines = file.readlines()

    filename_to_class = {line.split('\t')[0]: line.strip().split('\t')[1] for line in lines if '\t' in line}

    with open(destination_csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['filename', 'class'])  # Write header
        for filename in selected_filenames:
            if filename in filename_to_class:
                writer.writerow([filename, filename_to_class[filename]])


def update_csv_with_object_counts(selected_filenames):

    with open(annotation_json_path, 'r') as file:
        annotations = json.load(file)
    
    image_object_counts = {filename: len(annotations[filename]['points']) if filename in annotations else 0 for filename in selected_filenames}

    with open(destination_csv_path, newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)
    
    if 'object_count' not in rows[0]:
        rows[0].append('object_count')
    
    for row in rows[1:]:  # skip header
        if row[0] in image_object_counts:
            row.append(str(image_object_counts[row[0]]))
    
    with open(destination_csv_path, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

def cleaning():

    df = pd.read_csv(destination_csv_path)

    filenames_in_csv = set(df['filename'].tolist())

    # Directory containing the images
    image_directory = destination_folder

    # Iterate over files in the image directory
    for filename in os.listdir(image_directory):
        if filename not in filenames_in_csv:
            file_path = os.path.join(image_directory, filename)
            if os.path.isfile(file_path):
                print(f"Removing {file_path}")  # For logging purposes
                os.remove(file_path)  # Remove the file

    print("Cleaning up complete.")   

if __name__ == "__main__":
    # selected_filenames = select_random_300_images()
    # create_class_file_for_selected_images(selected_filenames)
    # update_csv_with_object_counts(selected_filenames)
    cleaning()