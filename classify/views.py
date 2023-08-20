from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
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
        label, col = klasifikasi(settings.LUNGMODEL, original, col)
        
        response = {
            "name":str(label),
            "col":col
        }
        return JsonResponse(response)
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
        col="warning"
        out=kelas[0]
    elif y_prediksi == 1:
        col="success"
        out=kelas[1]
    elif y_prediksi == 2:
        col="danger"
        out=kelas[2]
    return out,col
    