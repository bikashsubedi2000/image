# imageconverter/views.py
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image
import os

def convert_image(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        output_format = request.POST.get('format', 'png').lower()

        fs = FileSystemStorage()
        input_filename = fs.save(uploaded_file.name, uploaded_file)
        input_filepath = fs.path(input_filename)
        input_file_url = fs.url(input_filename)

        # Define output path with the new extension
        name, _ = os.path.splitext(input_filename)
        output_filename = f"{name}_converted.{output_format}"
        output_filepath = os.path.join(settings.MEDIA_ROOT, output_filename)

        # --- Image Conversion Logic ---
        with Image.open(input_filepath) as img:
            # If original is RGBA (has transparency) and converting to JPG, convert to RGB first
            if img.mode == 'RGBA' and output_format == 'jpeg':
                img = img.convert('RGB')
            img.save(output_filepath, format=output_format.upper())
        # ---------------------------

        output_file_url = os.path.join(settings.MEDIA_URL, output_filename)
        
        context['original_image_url'] = input_file_url
        context['processed_image_url'] = output_file_url

    return render(request, 'imageconverter/convert.html', context)