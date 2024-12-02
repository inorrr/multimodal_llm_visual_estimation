import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
from os.path import join

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    # Check if 'human' column exists, add it if not
    if 'human' not in df.columns:
        df['human'] = pd.NA  
    return df

def save_data(df, csv_path):
    # Save the DataFrame back to CSV
    df.to_csv(csv_path, index=False)

def next_image():
    global current_index, img_label, prompt_label, entry_human_guess

    # Save the current guess to the DataFrame if valid and increment index
    if current_index != -1:  # Check to ensure not first run where index is -1
        try:
            human_guess = int(entry_human_guess.get())
            df.loc[current_index, 'human'] = human_guess
            save_data(df, csv_path)
        except ValueError:
            pass

    # Find the next image without a human guess
    while True:
        current_index += 1
        if current_index >= len(df) or pd.isna(df.loc[current_index, 'human']):
            break

    if current_index < len(df):
        # Update the image and prompt
        img_path = join(folder_path, df.loc[current_index, 'filename'])
        image = Image.open(img_path)
        #image = image.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        img_label.config(image=photo)
        img_label.image = photo
        prompt_label.config(text=f"Count the number of {df.loc[current_index, 'class']} in this image.")
        entry_human_guess.delete(0, tk.END)
    else:
        prompt_label.config(text="No more images to label.")
        img_label.config(image='')
        entry_human_guess.delete(0, tk.END)

# Paths
folder_path =  'FSC147_384_V2/selected_300_images'
csv_path = 'FSC147_384_V2/selected_300_image_annotation.csv'

df = load_data(csv_path)

# Setup GUI
root = tk.Tk()
root.title("Image Labeling Tool")
current_index = -1
img_label = tk.Label(root)
img_label.pack()
prompt_label = tk.Label(root, text="", font=('Helvetica', 14))
prompt_label.pack()
entry_human_guess = tk.Entry(root)
entry_human_guess.pack()
next_button = tk.Button(root, text="Next", command=next_image)
next_button.pack()

next_image()

root.mainloop()