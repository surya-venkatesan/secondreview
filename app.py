#import sys
import os
import cv2
#import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from flask import Flask, request, render_template
import statistics as st


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index1.html")
    
    
@app.route('/camera', methods = ['GET', 'POST'])
def camera():
    i=0

 
    classifier = tf.keras.models.load_model('Model.h5')
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    output=[]
    cap = cv2.VideoCapture(1)
    class_labels = ['Angry','Happy','Neutral','Sad','Surprise']
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(238,130,238),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
    ##    
            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)


                predictions = classifier.predict(roi)[0]
                max_index = predictions.argmax()
                predicted_emotion = class_labels[max_index]
                
                print(predicted_emotion)
                label_position = (x,y)
                cv2.putText(frame,predicted_emotion,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(144, 154, 255),3)
                    
            else:
                cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(144, 154, 255),3)
                

        cv2.imshow('LIVE', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # print(output)
    cap.release()
    cv2.destroyAllWindows()
    # final_output1 = st.mode(output)
    return render_template("buttons.html",final_output=predicted_emotion.lower())


@app.route('/templates/buttons', methods = ['GET','POST'])
def buttons():
    return render_template("buttons.html")

@app.route('/songs/surprise', methods = ['GET', 'POST'])
def songsSurprise():
    return render_template("songsSurprise.html")

@app.route('/songs/angry', methods = ['GET', 'POST'])
def songsAngry():
    return render_template("songsAngry.html")

@app.route('/songs/sad', methods = ['GET', 'POST'])
def songsSad():
    return render_template("songsSad.html")

@app.route('/songs/happy', methods = ['GET', 'POST'])
def songsHappy():
    return render_template("songsHappy.html")

@app.route('/songs/neutral', methods = ['GET', 'POST'])
def songsNeutral():
    return render_template("songsNeutral.html")

@app.route('/templates/test', methods = ['GET', 'POST'])
def join():
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)
