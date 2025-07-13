# backgroundremover/views.py

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rembg import remove
import os

def upload_image(request):
    # This context will be passed to the template
    context = {}

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        
        # Use FileSystemStorage to handle file saving
        fs = FileSystemStorage()
        
        # Save the uploaded file and get its name
        # We save it to have a persistent original file to display
        input_filename = fs.save(uploaded_file.name, uploaded_file)
        
        # Construct the full path and URL for the input file
        input_filepath = fs.path(input_filename)
        input_file_url = fs.url(input_filename)

        # Define a name and path for the output file
        # Add a _bg_removed suffix to the original name
        output_filename = f"{os.path.splitext(input_filename)[0]}_bg_removed.png"
        output_filepath = os.path.join(settings.MEDIA_ROOT, output_filename)
        
        # Read the input file
        with open(input_filepath, 'rb') as f_in:
            input_data = f_in.read()
            # Process the image with rembg
            output_data = remove(input_data)

        # Write the output file
        with open(output_filepath, 'wb') as f_out:
            f_out.write(output_data)

        # Construct the URL for the output file
        output_file_url = os.path.join(settings.MEDIA_URL, output_filename)
        
        # Add the URLs to the context to be used in the template
        context['original_image_url'] = input_file_url
        context['processed_image_url'] = output_file_url

    return render(request, 'backgroundremover/index.html', context)

def homepage(request):
    """
    Renders the main homepage where users can choose a tool.
    """
    return render(request, 'homepage.html')