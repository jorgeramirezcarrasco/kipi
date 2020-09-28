import cv2
import glob
import os
import numpy as np
import sys

vidcap = cv2.VideoCapture('../data/artifacts/videos/tienda.mp4')
success,image = vidcap.read()
count = 0
classes=2
while success:
        for class_id in range(classes):
                cv2.imwrite(f"../data/artifacts/images/{class_id}_frame{count}.jpg", image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1
        if count>100:
                break

current_dir = "../data/artifacts/images"
split_pct = 10;
file_train = open("../data/artifacts/train.txt", "w")  
file_val = open("../data/artifacts/val.txt", "w")  
counter = 1  
index_test = round(100 / split_pct)  
for pathAndFilename in glob.iglob(os.path.join(current_dir, "*.jpg")):  
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if counter == index_test:
                counter = 1
                file_val.write(current_dir + "/" + title + '.jpg' + "\n")
        else:
                file_train.write(current_dir + "/" + title + '.jpg' + "\n")
                counter = counter + 1
file_train.close()
file_val.close()