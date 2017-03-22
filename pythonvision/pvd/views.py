from django.shortcuts import render
from google.cloud import vision
import os
import io
from google.cloud import storage
# Create your views here.

def index(request):
        # Instantiates a client
    vision_client = vision.Client()
    # The name of the image file to annotate
    file_name = os.path.join(os.path.abspath(os.curdir),'static\\images\\djangoguitar.jpg')
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(content=content)
    # Performs label detection on the image file

    labels = image.detect_labels()
    my_dict = {'lab':labels}
    return render(request,'pvd/index.html',context=my_dict)

def buckets(request):
    client = storage.Client()
    bucket = client.get_object('pythonvisionapi')
    print(bucket)
    my_dict={'buckets':bucket}
    return render(request,'pvd/test.html',context=my_dict)
