import pandas as pd
from openai import OpenAI
import os
# import base64
import helpers
import re

client = OpenAI()
# Function to encode the image
# def encode_image(image_path):
#     """
#     Encodes an image to a base64 string.

#     Parameters:
#     image_path (str): The path to the image file to be encoded.

#     Returns:
#     str: The base64 encoded string of the image.
#     """
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

def count_objects(image_path, object_name):
    """
    Sends an image to the GPT model to count the number of specific objects visible in the image.

    Parameters:
    image_path (str): The path to the image file.
    object_name (str): The name of the object to be counted in the image.

    Returns:
    str or None: The count of objects as a string if successful, None otherwise.
    """
    try:
        prompt = helpers.basic_count_prompt(object_name)
        base64_image = helpers.encode_image(image_path)

        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt,},
                {
                "type": "image_url",
                "image_url": {"url":  f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
            }
        ],
        )
        content = response.choices[0].message.content
        return content.strip()
    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def get_inital_count(images_path, csv_to_read, csv_to_write):
    """
    Processes a CSV file to count objects in each listed image, updating the CSV with these counts.

    Parameters:
    images_path (str): The directory path where images are stored.
    csv_path (str): The path to the CSV file containing image filenames and object names.
    """
    df = pd.read_csv(csv_to_read)
    df['gpt_4_initial_answer'] = None
    
    for index, row in df.iterrows():
        filename = row['filename']
        object_name = row['class']
        image_path = os.path.join(images_path, filename)
        
        if os.path.exists(image_path):
            # Get the object count from the model
            count = count_objects(image_path, object_name)
            try:
                # Attempt to convert count to an integer
                int_count = int(count)
                df.at[index, 'gpt_4_initial_answer'] = int_count
            except ValueError:
                # If conversion fails, set the count to pd.NA
                df.at[index, 'gpt_4_initial_answer'] = pd.NA
            print("-------------------------")
            print(count)
            df.to_csv(csv_to_write, index=False)
        else:
            print(f"Image {filename} not found at {image_path}")
            df.to_csv(csv_to_write, index=False)
    
    # Save the updated CSV
    #df.to_csv(csv_path, index=False)
    #print("Updated CSV saved.")

def generate_side_information(image_path, object_name):
    try:
        prompt = helpers.side_information_prompt(object_name)
        base64_image = helpers.encode_image(image_path)

        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt,},
                {
                "type": "image_url",
                "image_url": {"url":  f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
            }
        ],
        )
        content = response.choices[0].message.content

        full_response = content.strip()
        # parts = full_response.split('\n\n')
        # description = parts[1].split(": ", 1)[1] if len(parts) > 1 else ""
        # direct_hint = parts[2].split(": ", 1)[1] if len(parts) > 2 else ""
        # indirect_hint = parts[3].split(": ", 1)[1] if len(parts) > 3 else ""

        # # print("Description:", description)
        # # print("Direct hint:", direct_hint)
        # # print("Indirect hint:", indirect_hint)
        # print(image_path + " done")
        # print("Description: " + description)
        # print("direct_hint: " + direct_hint)
        # print("indirect_hint: " + indirect_hint)
        # print("======================================")
        # return description, direct_hint, indirect_hint
        return full_response
    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def get_hints(images_path, csv_to_read, csv_to_write):
    df = pd.read_csv(csv_to_read)
    df['full_response'] = None
    df['description'] = None
    df['direct_hint'] = None
    df['indirect_hint'] = None
    
    for index, row in df.iterrows():
        filename = row['filename']
        object_name = row['class']
        image_path = os.path.join(images_path, filename)

        if os.path.exists(image_path):
            # Get the object count from the model
            # full_response, (description, direct, indirect) = generate_side_information(image_path, object_name)
            full_response = generate_side_information(image_path, object_name)
            df.at[index, 'full_response'] = full_response
            # df.at[index, 'description'] = description
            # df.at[index, 'direct_hint'] = direct
            # df.at[index, 'indirect_hint'] = indirect
        else:
            print(f"Image {filename} not found at {image_path}")
        df.to_csv(csv_to_write, index=False)

    # Save the DataFrame after processing all rows to minimize I/O operations
    # df.to_csv(csv_to_write, index=False)

def extract_section(full_response, section):
    # Check if the response exists and is not NaN
    if pd.isna(full_response):
        return None
    
    # Define possible start and stop strings for each section
    if section == "description":
        starts = ["1. **Description:**", "### 1. Description:", "1. **Description**:", 
                  "### 1. Description:", "1. **Description:**", "1. **Description**:"]
        stops = ["2. **Direct hint:**", "### 2. Direct Hint:", "2. **Direct hint**:", 
                 "### 2. Direct hint:", "2. **Direct Hint:**", "2. **Direct Hint**:"]
    elif section == "direct_hint":
        starts = ["2. **Direct hint:**", "### 2. Direct Hint:", "2. **Direct hint**:", 
                  "### 2. Direct hint:", "2. **Direct Hint:**", "2. **Direct Hint**:"]
        stops = ["3. **Indirect hint:**", "### 3. Indirect Hint:", "3. **Indirect hint**:", 
                 "### 3. Indirect hint:", "3. **Indirect Hint:**", "3. **Indirect Hint**:"]
    elif section == "indirect_hint":
        starts = ["3. **Indirect hint:**", "### 3. Indirect Hint:", "3. **Indirect hint**:", 
                  "### 3. Indirect hint:", "3. **Indirect Hint:**", "3. **Indirect Hint**:"]
        stops = [None]  # Last section has no stop
    
    # Find the start and stop indices of the sections
    start_idx = -1
    stop_idx = len(full_response)
    for start in starts:
        index = full_response.find(start)
        if index != -1:
            start_idx = index + len(start)
            break
    
    if start_idx == -1:  # No start found
        return None
    
    for stop in stops:
        if stop is not None:
            index = full_response.find(stop, start_idx)
            if index != -1:
                stop_idx = index
                break
    
    # Extract and return the section, if the start is found
    return full_response[start_idx:stop_idx].strip()

def split_response(csv_in, csv_out):
    df = pd.read_csv(csv_in)
    df['description'] = df['full_response'].apply(lambda x: extract_section(x, "description"))
    df['direct_hint'] = df['full_response'].apply(lambda x: extract_section(x, "direct_hint"))
    df['indirect_hint'] = df['full_response'].apply(lambda x: extract_section(x, "indirect_hint"))

    # Count NA values in each of the specified columns
    na_description = df['description'].isna().sum()
    na_direct_hint = df['direct_hint'].isna().sum()
    na_indirect_hint = df['indirect_hint'].isna().sum()

    print(f"Number of NA's in Description: {na_description}")
    print(f"Number of NA's in Direct Hint: {na_direct_hint}")
    print(f"Number of NA's in Indirect Hint: {na_indirect_hint}")

    df.to_csv(csv_out, index=False)
    print("CSV file has been modified and saved.")

if __name__ == "__main__":
    images_path = "FSC147_384_V2/selected_300_images" 
    csv_path = "FSC147_384_V2/300_image_labels.csv" 
    gpt4_evaluation_csv_path = "results/gpt4_evaluation.csv"
    gpt4_splited_response = "results/gpt4_evaluation_splited.csv"
    # get_inital_count(images_path, csv_to_read=csv_path, csv_to_write=gpt4_evaluation_csv_path)
    # get_hints(images_path, csv_to_read=csv_path, csv_to_write=gpt4_evaluation_csv_path)
    split_response(csv_in=gpt4_evaluation_csv_path, csv_out=gpt4_evaluation_csv_path)