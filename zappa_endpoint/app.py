from flask import Flask, Response, request
import json
from flask_cors import CORS
import cv2
import numpy as np
from math import sqrt
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from datetime import datetime
from datetime import timedelta
import os
import boto3



app = Flask(__name__)
cors = CORS(app)

def check_status():
    dynamodb = boto3.resource('dynamodb',region_name='eu-central-1')
    table = dynamodb.Table('shop_status')
    response = table.get_item(Key={'shop': "GrMlgElPalmeral"})
    status = response['Item']['status_shop']
    return status

def update_status(status):
    
    dynamodb = boto3.resource('dynamodb',region_name='eu-central-1')
    table = dynamodb.Table('shop_status')
    table.update_item(
        Key={'shop': "GrMlgElPalmeral"},
        UpdateExpression='SET status_shop = :val1',
        ExpressionAttributeValues={
            ':val1': status
        }
    )

    return 1

def send_email(status,shop="GrMlgElPalmeral"):
    # set up a server
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(os.environ['EMAIL_SENDER'], os.environ['PASSWORD_SENDER'])

    # create and specify parts of the email
    msg = MIMEMultipart()
    msg['From'] = os.environ['EMAIL_SENDER']
    msg['To'] = os.environ['EMAIL_RECEIVER']
    msg['Subject'] = f"Apertura de la tienda {date.today()+ timedelta(hours=1)}"

    msg.attach(MIMEText(f"La tienda {shop} está {status} a las {datetime.now()}", 'plain'))

    mail.send_message(msg)
    mail.quit()

def extract_shopfront_imgs(img,
                           vitr_pts = {'top-left': (630, 750),
            'top-right': (270, 1380),
            'bottom-left': (750, 890),
            'bottom-right': (350, 1510)},
                           div_lines_x = [240, 500, 770]):
    """Extract shopfront elements to improve inference

    Args:
        img ([Img]): Frame of the video
        vitr_pts (dict, optional): Coordinates of the shopfront. Defaults to {'top-left': (630, 750), 'top-right': (270, 1380), 'bottom-left': (750, 890), 'bottom-right': (350, 1510)}.
        div_lines_x (list, optional): Divisors of the shopfront. Defaults to [240, 500, 770].

    Returns:
        [Img, list]: ShopFront Image and a list of the crops
    """

    # Calculate width - height
    a = vitr_pts['top-right'][1] - vitr_pts['top-left'][1]
    b = vitr_pts['top-left'][0] - vitr_pts['top-right'][0]
    width = round(sqrt(a**2 + b**2))
    
    a = vitr_pts['top-left'][1] - vitr_pts['bottom-left'][1]
    b = vitr_pts['bottom-left'][0] - vitr_pts['top-left'][0]
    height = round(sqrt(a**2 + b**2))
    
    # Crop image with warp perspective
    raw_pts = np.float32([[x, y] for y, x in vitr_pts.values()])
    dst_pts = np.float32([[0, 0], [width, 0],
                          [0, height], [width, height]])
    M = cv2.getPerspectiveTransform(raw_pts, dst_pts)
    img_crop = cv2.warpPerspective(img, M, (width, height))
    
    vitr_crops = list()
    for idx, x in enumerate(div_lines_x):
        if idx == 0:
            crop = img_crop[: , :x, :]
        else:
            crop = img_crop[: , div_lines_x[idx-1]:x]
        vitr_crops.append(crop)
    return img_crop, vitr_crops

@app.route("/check_is_open",methods=['POST']) 
def check_is_open():
    list_status = []
    send_email_flag = False
    label = "closed"
    time.sleep(1)
    cap = cv2.VideoCapture(os.environ['URL_VIDEO'])
    for ii in range(10):
        ret, frame = cap.read()
        frame_saturation, _ = extract_shopfront_imgs(frame,{'top-left': (800, 1100),
            'top-right': (500, 1400),
            'bottom-left': (1000, 1300),
            'bottom-right': (700, 1700)})
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_hsv = cv2.cvtColor(frame_saturation, cv2.COLOR_BGR2HSV)
        saturation = img_hsv[:, 1, :].mean()
        if saturation > 50:
            list_status.append(1)
        else:
            list_status.append(0)

    label_count = np.array(list_status).sum()
    if label_count > 4:
        label = "open"
    if check_status() != label:
        update_status(label)
        send_email_flag = True
    if send_email_flag:
        send_email(label)
    return Response(json.dumps({"status":label}),  mimetype='application/json')

if __name__ == "__main__":
    app.run()
    

