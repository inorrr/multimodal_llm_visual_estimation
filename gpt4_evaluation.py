import pandas as pd
from openai import OpenAI
import os
# import base64
import helpers

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
        prompt = f"Please count the number of {object_name} visible in this image and respond with only the numeric answer."
        
        # Getting the base64 string
        base64_image = helpers.encode_image(image_path)

        # Send the prompt and image to the model
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

def get_inital_count(images_path, csv_path):
    """
    Processes a CSV file to count objects in each listed image, updating the CSV with these counts.

    Parameters:
    images_path (str): The directory path where images are stored.
    csv_path (str): The path to the CSV file containing image filenames and object names.
    """
    df = pd.read_csv(csv_path)
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
            df.to_csv(csv_path, index=False)
        else:
            print(f"Image {filename} not found at {image_path}")
            df.to_csv(csv_path, index=False)
    
    # Save the updated CSV
    #df.to_csv(csv_path, index=False)
    #print("Updated CSV saved.")

if __name__ == "__main__":
    images_path = "FSC147_384_V2/selected_300_images" 
    csv_path = "FSC147_384_V2/selected_300_image_annotation.csv" 
    gpt4_evaluation_csv_path = "results/gpt4_evaluationn.csv"
    get_inital_count(images_path, csv_path)