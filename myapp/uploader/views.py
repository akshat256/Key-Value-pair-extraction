from django.shortcuts import render,redirect
from django.http import HttpResponse
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import csv
import os
import mimetypes
import tempfile
from django.core.files.uploadedfile import UploadedFile



def index(request):                 #index view which returns the upload and result page
    if request.method != 'POST':
        return render(request, "uploader/index.html")
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_mime, _ = mimetypes.guess_type(uploaded_file.name)
        if file_mime and (file_mime.startswith('image') or file_mime == 'application/pdf'): #to check if file is pdf or image
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:                    #temprory storing the file 
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
            if file_mime == 'application/pdf':                                              #if file is a pdf
                images = convert_from_path(temp_file.name)
                text = ''
                for image in images:                                            
                    text += pytesseract.image_to_string(image)
            else:
                image = Image.open(temp_file.name)                                          #if file is an image
                text = pytesseract.image_to_string(image)
            key_value_pairs = extract_key_value_pairs(text)
            return render(request, "uploader/result.html", {'key_value_pairs': key_value_pairs, 'file_path': temp_file.name})
        else:
            return render(request, "uploader/index.html")   
    else:
        return render(request, "uploader/index.html")
    


def delete_file(request):                                                                    #fucntion for deleting the temporary stored file
    if request.method == 'POST' and 'file_path' in request.POST:
        file_path = request.POST['file_path']
        if os.path.exists(file_path):
            os.remove(file_path)
    return redirect("index")



def extract_key_value_pairs(text):                                                           #function for extracting key value pairs
    
    key_value_pairs = {}

    lines = text.split('\n')

    for line in lines:      # cheks for key value pairs in the text
        if ':' in line:
            key, value = line.split(':', 1)
            key_value_pairs[key.strip()] = value.strip()
        
    return key_value_pairs