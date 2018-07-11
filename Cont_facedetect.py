#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 18:52:16 2018

@author: arpitansh
"""

import cv2
import requests
from os.path import join, dirname
from dotenv import load_dotenv
import os
import facedata_insert



def PhotoCapture():
    #cap = cv2.VideoCapture(0) 
    while True:
  
        ret, frame = cap.read()
        #if ret == True:
            #cv2.imshow('image',frame)

            
       
        #k = cv2.waitKey(1)
        # save frame as JPEG file if s is hit
        #if k%256 == 115:
        #while(1):
        cv2.imwrite("test_image.jpg", frame) 
            #cap.release() 
        cv2.destroyAllWindows()
        break
            #return 1
            
        
        # exit if Escape is hit
        #if k%256 == 27:
        #while(1):
            #cap.release()
            #cv2.destroyAllWindows()                  
            #return 0

    
 
def Collect_Face_Info():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    subscription_key = os.getenv('key')
    

    face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

    image_path = "test_image.jpg"  # Set the image path  

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()

    headers = {
         'Ocp-Apim-Subscription-Key':subscription_key,
         'Content-Type': 'application/octet-stream'
         }

    params = {
        'returnFaceId': 'True',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile,' + 
        'emotion,hair,makeup,accessories'
        }
    try:
        

        response = requests.post(
                face_api_url, headers=headers, params=params, data=image_data
                )

        analysis = response.json()
        return analysis
    
    except requests.exceptions.RequestException as err:
        print('Connection Error',err)
    except requests.exceptions.ConnectionError as errc:
        print('Connection Error',errc)
    except requests.exceptions.ConnectTimeout as errt:
        print('Time out',errt)
    except requests.exceptions.HTTPError as errh:
        print('HTTP err',errh)
    return None
    
    
def PrintData(analysis):
    count = 0
    for face in analysis:
        count += 1
    
        face_id = face['faceId']
        gender = face['faceAttributes']['gender']
        age = face['faceAttributes']['age']
        
        print('face id:',face_id) 
        print('Gender:',gender)
        print('Age:',age) 
    
        check_emo =0
        rslt_emotion = " "
        for emotion in face['faceAttributes']['emotion']:
            if face['faceAttributes']['emotion'][emotion] > check_emo:
                check_emo = face['faceAttributes']['emotion'][emotion]
                rslt_emotion = emotion
        emotion = rslt_emotion
        emotion_percentage = check_emo*100 
        
        print('Emotion:',emotion)
        print('Emotion Percentage: ',emotion_percentage)
        
        # Transferring face Details into Database
        facedata_insert.insert_Face_Details(face_id, gender,age,emotion,emotion_percentage)
        
        
        

def main():
    while(1):
        PhotoCapture()
        analysis = Collect_Face_Info()
        if analysis:
            PrintData(analysis)
        else:
            print("No Face deteced")
    
    print('No photo Captured')
    cap.release() 
       
cap = cv2.VideoCapture(0)            
main()
 
