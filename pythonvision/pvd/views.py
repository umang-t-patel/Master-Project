"""
Constructs the Views for Pythonvisionapi Application
Author: Umang Patel
Last Tested: 4/06/2017 by Umang Patel
Verified with:
Python 3.5,
Django 1.10.6, for creating web application
google-cloud-storage==0.23.1 for Storage related libraries
google-cloud-vision==0.23.1 for Vision related libraries
gunicorn==19.7.0 for running it on cloud enviornment
"""
import os,datetime,six
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from google.cloud import vision, storage
from google.cloud.vision.feature import Feature, FeatureTypes
from pvd import upload

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
        annlist = []
        index = 0
        for image in results:
            anndict={"img":images[index],"faces":image.faces,"labels":image.labels,"texts":image.texts,"properties":image.properties \
                    ,"landmarks":image.landmarks,"logos":image.logos,"safe_searches":image.safe_searches}
            #print(anndict)
            anndict = {index:anndict}
            annlist.append(anndict)
            index += 1
        #print(annlist)
    return render(request,'pvd/annotations.html',context={'annlist': annlist})

def annotations(request):
    client = storage.Client()
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("pythonvisionapi")
    blobs = bucket.list_blobs()
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
        image_url = upload.upload_image_file(myfile)
        my_dict={'public_url':image_url}
    return render(request,'pvd/storage.html',context=my_dict)
