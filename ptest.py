
import cv2
import base64
import eel
import mediapipe as mp
import numpy as np

import threading
import sqlite3

def read_image():
  #conn = sqlite3.connect("stdb.db")
   # cursor = conn.cursor()
   # cursor.execute("SELECT data FROM frame_code WHERE id=1")
   # result = cursor.fetchone()
   # encoded = result[0]
    #decoded = base64.b64decode(encoded)

    #img = np.frombuffer(decoded, dtype=np.uint8)
    #cv2.imwrite("test.png", img)


   
    area9 = [185,186,92,165,167,164,393,391,322,410,409,270,269,267,0,37,39,40,185] # over_lip (Rectified)
    img=cv2.imread('test1.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (512, 512))


    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    print(results)
    landmarks = results.multi_face_landmarks[0]
   

    def find_landmarks(image, landmarks, area):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []
        coord = []
        for index, landmark in enumerate(landmarks.landmark):
            if landmark.visibility < 0 or landmark.presence < 0:
                continue
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point.append((landmark_x, landmark_y))
        for num in range(len(area)):
            coord.append(landmark_point[area[num]])
        return coord 

    points = find_landmarks(img, landmarks, area9)
    mask = np.zeros_like(img) 
    cv2.fillPoly(mask,[np.array(points)], (255,0,0))
    img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
    cv2.imwrite("test1.png", img1)
    return "test"

print(read_image())