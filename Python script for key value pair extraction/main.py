import pytesseract
from pdf2image import convert_from_path
import csv
import os
import mimetypes
import csv

def text_extractor(input):    # To extract text from given pdf file/image
    text = ''
    if is_pdf(input):   
        images = convert_from_path(input)
        for i, image in enumerate(images):          
            text += extract_text_from_image(image)
    else:
        text = extract_text_from_image(input)
    return text

def is_pdf(file_path):   # Finds if given file is a pdf or not
    return mimetypes.guess_type(file_path)[0] == 'application/pdf'

def extract_text_from_image(image): #to extract text from images
    text = ''
    text += pytesseract.image_to_string(image)  # Perform OCR on page
    return text

def extract_key_value_pairs_from_invoice(text): #
    
    key_value_pairs = {}
    table_data = []

    lines = text.split('\n')

    for line in lines:      # cheks for key value pairs in the text
        if ':' in line:
            key, value = line.split(':', 1)
            key_value_pairs[key.strip()] = value.strip()
        
        

    return key_value_pairs


def write_dict_to_csv(data_dict, file_path):            #function to add key value pairs to csv file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(data_dict.keys())
        # Write data
        writer.writerow(data_dict.values())

input = 'sample2.jpg'
text = text_extractor(input)
key_value_pairs = extract_key_value_pairs_from_invoice(text)


file_path = 'data.csv'
write_dict_to_csv(key_value_pairs, file_path)       