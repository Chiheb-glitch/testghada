import cv2
import base64
import eel
import mediapipe as mp
import numpy as np
import pandas as pd
import threading
import sqlite3
eel.init('web')
camera = cv2.VideoCapture(0)


@eel.expose
def json_cloud_products():
  filename = "products.csv"
  df = pd.read_csv(filename)
  json_c={"Area 1": ["Wrinkles Depth Estimation on Average:", 0.04, ", Wrinkles detected: ", 6], 
    "Area 3": ["Wrinkles Depth Estimation on Average:", 0.05, ", Wrinkles detected: ", 15], 
    "Area 4": ["Wrinkles Depth Estimation on Average:", 0.05, ", Wrinkles detected: ", 22],
    }
  t=[]
  c=[]
  for i in json_c:

   for index, row in df.iterrows():
    print('Index:', index)
    print('Row data:', row['Area'])
    if row["Area"] == i:
        t.append(df.iloc[index,:])
        c.append(index)
  x=[]
  intt=0
  for i in t:
     y=[]
     y.append(i["Name"])
     y.append(i['Image URL'])
     y.append(i["Description"])
     y.append(i['Area'])
     y.append(c[intt])
     intt += 1 

     x.append(y)

  return x


@eel.expose
def add_product(id):
   t=()
   filename = "products.csv"
   df = pd.read_csv(filename)
   for index, row in df.iterrows():
     print('Index:', index)
     if id == index  :
        t=t+ (row["Name"],index,row['Image URL'] )
   conn = sqlite3.connect('stdb.db')

   cursor = conn.cursor()
   cursor.execute('INSERT INTO product (name, id, image) VALUES (?, ?, ?)', t)
   conn.commit()
   
   
@eel.expose
def send_email(name,email):
   
     

 import smtplib
 from email.mime.multipart import MIMEMultipart
 from email.mime.text import MIMEText
 from email.mime.image import MIMEImage

 sender = "camperdhaouadi@gmail.com"
 recipient = email

 msg = MIMEMultipart('alternative')
 msg['Subject'] = "Report"
 msg['From'] = sender
 msg['To'] = recipient
 conn = sqlite3.connect('stdb.db')
 cursor = conn.cursor()
 cursor.execute("SELECT name, image FROM product")
 html = "<html><body>"

 for product in cursor.fetchall():
    name, image = product
    product_html = f"""
        <div>
            <img src="{image}" alt="{name}">
            <h3>{name}</h3>
          
        </div>
    """
    html += product_html

 html += "</body></html>"

 part1 = MIMEText(html, 'html')
 cursor.execute('DELETE FROM product')
 conn.commit()
 msg.attach(part1)


 s = smtplib.SMTP('smtp.gmail.com', 587)
 s.starttls()
 s.login(sender, 'mnvlnpvwxoaqegzw') 
 s.sendmail(sender, recipient, msg.as_string())
 s.quit()


@eel.expose
def convert_to_grayscale(frame):
    frame = np.frombuffer(frame, np.uint8)
    img = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)

    if img is None:
        return "Error: Could not load image."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, jpeg = cv2.imencode('.jpg', gray)
    return jpeg.tobytes()

@eel.expose

def read_image_area():
  #conn = sqlite3.connect("stdb.db")
   # cursor = conn.cursor()
   # cursor.execute("SELECT data FROM frame_code WHERE id=1")
   # result = cursor.fetchone()
   # encoded = result[0]
    #decoded = base64.b64decode(encoded)

    #img = np.frombuffer(decoded, dtype=np.uint8)
    #cv2.imwrite("test.png", img)


   
    area1 =[70,71,21,54,103,67,109,10,338,297,332,284,251,301,300,293,334,296,336,9,107,66,105,63,70] # over_lip (Rectified)
    img=cv2.imread('test1.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (512, 512))


    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
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

    points = find_landmarks(img, landmarks, area1)
    mask = np.zeros_like(img) 
    cv2.fillPoly(mask,[np.array(points)], (255,0,0))
    img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
    _, encoded = cv2.imencode('.png', img1, [cv2.IMWRITE_JPEG_QUALITY, 80])
    
    return base64.b64encode(encoded).decode()


def read_image_of_group_detection():
    area1 =[70,71,21,54,103,67,109,10,338,297,332,284,251,301,300,293,334,296,336,9,107,66,105,63,70] # forehead (Checked)
    area2 = [113,124,156,143,116,117,228,25,130,113] # near_left_eye (Checked)
    area3 = [342,353,383,372,345,346,448,255,359,342] # near_right_eye (Rectified)
    area4 = [233,128,114,47,100,119,118,117,31,228,229,230,231,232,233] # under_left_eye (Checked)
    area5 = [453,357,343,277,329,348,347,346,361,448,449,450,451,452,453] # under_right_eye (Rectified)
    area6 = [55,8,285,417,351,6,122,193,55] # between_eyes (Rectified)
    area7 = [185,186,216,207,192,135,169,170,211,204,106,43,146,61,185] # left_cheek (Rectified)
    area8 = [409,410,436,427,416,364,394,395,431,424,335,273,375,291,409]  # right_cheek (Rectified)
    area9 = [185,186,92,165,167,164,393,391,322,410,409,270,269,267,0,37,39,40,185] # over_lip (Rectified)
    area10 = [57,43,106,182,83,18,313,406,335,273,287,375,321,405,314,17,84,181,91,146,57]  # under_lip (Changed)
    area11 = [194,201,200,421,418,262,369,396,175,171,140,32,194] # chin (Rectified)
    json_c={"Area1": ["Wrinkles Depth Estimation on Average:", 0.04, ", Wrinkles detected: ", 6], 
"Area3": ["Wrinkles Depth Estimation on Average:", 0.05, ", Wrinkles detected: ", 15], 
"Area3": ["Wrinkles Depth Estimation on Average:", 0.05, ", Wrinkles detected: ", 22],
}
    img=cv2.imread('68971.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (512, 512))
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
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
    for i in json_c:
     if i == "Area1":
      points = find_landmarks(img, landmarks, area1)
      mask = np.zeros_like(img)
      cv2.fillPoly(mask,[np.array(points)], (255,0,0))
      img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
      cv2.imwrite("68971.png", img1)
     if i == "Area2":
        points = find_landmarks(img, landmarks, area2)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)
     if i == "Area3":
        points = find_landmarks(img, landmarks, area3)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)
     if i == "Area4":
        points = find_landmarks(img, landmarks, area4)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)

     if i == "Area5":
        points = find_landmarks(img, landmarks, area5)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)
     if i == "Area6":
        points = find_landmarks(img, landmarks, area6)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)
     if i == "Area7":
        points = find_landmarks(img, landmarks, area7)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)
     if i == "Area8":
        points = find_landmarks(img, landmarks, area9)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)
     if i == "Area9":
        points = find_landmarks(img, landmarks, area9)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)

     if i == "Area10":
        points = find_landmarks(img, landmarks, area10)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)

     if i == "Area11":
        points = find_landmarks(img, landmarks, area11)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask,[np.array(points)], (25,190,60))
        img1 = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
        cv2.imwrite("68971.png", img1)
    
    
    _, encoded = cv2.imencode('.png', img1, [cv2.IMWRITE_JPEG_QUALITY, 80])
    
    return base64.b64encode(encoded).decode()


@eel.expose
def send_image(b64_string):
    global camera
    camera.release()
    cv2.destroyAllWindows()
   
    img_data = base64.b64decode(b64_string.split(",")[1])
    numpy_array = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(numpy_array, cv2.IMREAD_UNCHANGED)
    image = cv2.resize(image, (250, 512))

    cv2.imwrite("image.png", image)

@eel.expose
def read_image():
    conn = sqlite3.connect("stdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM frame_code WHERE id=1")
    binary_data = cursor.fetchone()[0]
    return binary_data 
    

@eel.expose
def set_frame(b64_string):
    print('test')
    eel.set_frame(b64_string)()

def capture_thread():
    #camera = cv2.VideoCapture(0)
    
    global camera
    print(camera.isOpened())
    if camera.isOpened() == False:
        camera = cv2.VideoCapture(0)


    camera.set(cv2.CAP_PROP_FPS, 30)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    i=0
    

    while True:
        if camera.isOpened() == False:
            break
        ret, frame = camera.read()
        x_frame = cv2.resize(frame, (500, 900))
        conn = sqlite3.connect("stdb.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM frame_code")
        conn.commit()

        _, encoded = cv2.imencode('.png', x_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if i == 0 :
                x = cv2.resize(frame, (512, 512))

                cv2.imwrite("test1.png", x)
                i=i+1

        cursor.execute("INSERT INTO frame_code (data) VALUES (?)", (base64.b64encode(encoded).decode(),))
        conn.commit()

      
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
         for i in range(20):
            cv2.circle(frame, (x, y+i), 2, (250, 235, 215), -1)
            cv2.circle(frame, (x+i, y), 2, (250, 235, 215), -1)
            cv2.circle(frame, (x + w-i, y), 2, (250, 235, 215), -1)
            cv2.circle(frame, (x + w, y+i), 2, (250, 235, 215), -1)
            cv2.circle(frame, (x+i, y + h), 2, (250, 235, 215), -1)
            cv2.circle(frame, (x, y + h-i), 2, (250, 235, 215), -1)
            cv2.circle(frame, (i+x + w, y + h), 2, (250, 235, 215), -1)
            cv2.circle(frame, (x + w+20, y-i+h), 2, (250, 235, 215), -1)
 


        _, encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80]) 
        b64_string = base64.b64encode(encoded).decode()
        eel.set_frame(b64_string)()
    camera.release()
    cv2.destroyAllWindows()

capture_thread = threading.Thread(target=capture_thread)
capture_thread.start()

eel.start('index.html', size=(500, 900))
