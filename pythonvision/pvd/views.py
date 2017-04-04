from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from google.cloud import vision
import os
import io
import datetime
import six
from google.cloud import storage
from google.cloud.vision.feature import Feature
from google.cloud.vision.feature import FeatureTypes
# Create your views here.
def index(request):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(settings.CLOUD_STORAGE_BUCKET)
    blobs = bucket.list_blobs()
    my_dict={'annotations':blobs}
    return render(request,'pvd/index.html',context=my_dict)

def runvision(request):
    if request.method == "POST":
        images = request.POST.getlist('images')
        annotate =request.POST.getlist('annotate')
        # printing to check whether getting the selected values
        # print (images, annotate)
        html = "Hey"
        vision_client = vision.Client()
        batch = vision_client.batch()
        features = []
        for ann in annotate:
            if ann == "LANDMARK_DETECTION":
                land_feature = Feature(FeatureTypes.LANDMARK_DETECTION,20)
                features.append(land_feature)
            if ann == "FACE_DETECTION":
                face_feature = Feature(FeatureTypes.FACE_DETECTION,20)
                features.append(face_feature)
            if ann == "LOGO_DETECTION":
                logo_feature = Feature(FeatureTypes.LOGO_DETECTION,20)
                features.append(logo_feature)
            if ann == "LABEL_DETECTION":
                label_feature = Feature(FeatureTypes.LABEL_DETECTION,20)
                features.append(label_feature)
            if ann == "TEXT_DETECTION":
                text_feature = Feature(FeatureTypes.TEXT_DETECTION,20)
                features.append(text_feature)
            if ann == "SAFE_SEARCH_DETECTION":
                safe_search_feature = Feature(FeatureTypes.SAFE_SEARCH_DETECTION,20)
                features.append(safe_search_feature)
            if ann == "IMAGE_PROPERTIES":
                image_feature = Feature(FeatureTypes.IMAGE_PROPERTIES,20)
                features.append(image_feature)
        for img in images:
            image = vision_client.image(source_uri=img)
            batch.add_image(image, features)
        results = batch.detect()
        for image in results:
            anndict={"faces":image.faces,"labels":image.labels,"texts":image.texts,"properties":image.properties \
                    ,"landmarks":image.landmarks,"logos":image.logos,"safe_searches":image.safe_searches}
            """for face in image.faces:
                print('=' * 40)
                print(face.joy)
            for label in image.labels:
                print('=' * 40)
                print(label.description)
            for text in image.texts:
                print('=' * 40)
                print(text.description)"""
    return render(request,'pvd/annotations.html',context=anndict)

def index1(request):
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

def annotations(request):
    client = storage.Client()
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("pythonvisionapi")
    blobs = bucket.list_blobs()
    #for blob in blobs:
    #    print(blob.public_url)
    my_dict={'annotations':blobs}
    return render(request,'pvd/annotations.html',context=my_dict)

def uploadstorage(request):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(settings.CLOUD_STORAGE_BUCKET)
    blobs = bucket.list_blobs()
    my_dict={'annotations':blobs}
    return render(request,'pvd/storage.html',context=my_dict)

def uploadimage(request):
    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        image_url = upload_image_file(myfile)
        my_dict={'public_url':image_url}
    return render(request,'pvd/storage.html',context=my_dict)

def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = upload_file(
        file.read(),
        file.name,
        file.content_type
    )
    return public_url

def check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


def safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.
    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    filename = filename
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}.{1}".format(date, extension)


# [START upload_file]
def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    check_extension(filename, settings.ALLOWED_EXTENSIONS)
    filename = safe_filename(filename)

    client = storage.Client()
    bucket = client.bucket(settings.CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url
# [END upload_file]
