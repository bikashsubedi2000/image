# imageresizer/views.py
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image
import os

def resize_image(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        
        # Get width and height from the form, with defaults
        try:
            width = int(request.POST.get('width'))
            height = int(request.POST.get('height'))
        except (ValueError, TypeError):
            # Handle cases where width/height are not provided or invalid
            # You can add an error message to the context here if you like
            return render(request, 'imageresizer/resize.html', {'error': 'Invalid width or height provided.'})

        fs = FileSystemStorage()
        input_filename = fs.save(uploaded_file.name, uploaded_file)
        input_filepath = fs.path(input_filename)
        input_file_url = fs.url(input_filename)

        # Define output path
        name, ext = os.path.splitext(input_filename)
        output_filename = f"{name}_resized{ext}"
        output_filepath = os.path.join(settings.MEDIA_ROOT, output_filename)

        # --- Image Resizing Logic ---
        with Image.open(input_filepath) as img:
            resized_img = img.resize((width, height))
            resized_img.save(output_filepath)
        # --------------------------

        output_file_url = os.path.join(settings.MEDIA_URL, output_filename)
        
        context['original_image_url'] = input_file_url
        context['processed_image_url'] = output_file_url

    return render(request, 'imageresizer/resize.html', context)