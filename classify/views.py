from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
import os
from keras.preprocessing.image import load_img

# Create your views here.
def index(request):

    if  request.method == "POST":
        f=request.FILES['sentFile']
        original = readimg(f)
        col=""
        label, col = klasifikasi(settings.MYMODEL, original, col)

        response = {}
        response['name'] = str(label)
        response['img'] = f.read
        response['color'] = col
        return render(request,'index.html', response)
    else:
        return render(request,'index.html')


# function
import cv2
import numpy as np

def readimg(fn):
    # img = cv2.imread(filename=fn)
    im = fn.read()
    img = np.asarray(bytearray(im), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    rgb=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rez=cv2.resize(rgb,(270,270))
    resc=rez/255
    return resc

def klasifikasi(model, image, col):
    img=cv2.resize(image,(128,128))
    img=np.expand_dims(img,axis=0)
    prediksi=model.predict(img)
    y_prediksi=np.argmax(prediksi, axis=1)[0]
    kelas=["Adenocarsinoma","Normal","Squamous Cell Carcinoma"]
    if y_prediksi == 0:
        col="orange"
        out=kelas[0]
    elif y_prediksi == 1:
        col="green"
        out=kelas[1]
    elif y_prediksi == 2:
        col="red"
        out=kelas[2]
    return out,col
    