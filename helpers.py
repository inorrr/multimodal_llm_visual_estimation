import base64

def encode_image(image_path):
    """
    Encodes an image to a base64 string.

    Parameters:
    image_path (str): The path to the image file to be encoded.

    Returns:
    str: The base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def basic_count_prompt(object_name):
    prompt = f"Please count the number of {object_name} visible in this image and respond with only the numeric answer."
    return prompt

def side_information_prompt(object_name):
    prompt = f"""
    Please generate informations that can help someone on counting the number of {object_name} in this image. You need to provide the following:\n
    1. Description: details of the objects in this image.\n
    2. Direct hint: guidlines on methods to count the number of objects\n
    3. Indirect hint: the contextual or background information about the object that will help in counting.\n
    For example, if you are seeing an image of geese, you should provide the following:\n
    1. Description: The image features a group of Canada geese in flight against a clear blue sky. The geese are dispersed across the image in various flight positions, with their wings in different phases of the flapping cycle.\n
    2. Direct hint: To count the number of geese, start from one corner of the image and move your eyes in a grid-like pattern—left to right, top to bottom—marking each bird as counted to avoid recounting the same goose.\n
    3. Indirect hint: Geese often travel in V-shaped formations or smaller groups, which can help you estimate their numbers more effectively. When counting, keep in mind that the number will likely reflect typical group sizes seen in nature, rather than a sparse or overly dense arrangement."""
    return prompt

def count_with_hint_prompt(object_name, description, direct_hint, indirect_hint):
    base_prompt = f"""Please count the number of {object_name} visible in this image and respond with only the numeric answer.\n"""
    start = """You have the following information availiable to help you:\n"""
    prompt = start + f"""{description}""" + '\n' + f"""{direct_hint}""" + '\n' + f"""{indirect_hint}""" + '\n' + base_prompt
    return prompt

if __name__ == "__main__":
    print(count_with_hint_prompt("apples", "description", "direct hint", "indirect hint"))
    # print(side_information_prompt("apples"))