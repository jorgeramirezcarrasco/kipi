from PIL import Image
import time
from .img_inference_utils import extract_shopfront_imgs
import cv2
from tqdm import tqdm

def create_ds_from_video_feed(feed,num_images=1000,sleep_time=100,dataset_path='../data/shopfront/'):
    """Dataset generator from video feed.

    Args:
        feed (str): video feed
        num_images (int, optional): Number of images to generate. Defaults to 1000.
        sleep_time (int, optional): Waiting time between captures. Defaults to 100.
        dataset_path (str, optional): Path to save the images. Defaults to '../data/shopfront/'.
    """
    for i in tqdm(range(num_images)):
            cap = cv2.VideoCapture(feed)
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame, _ = extract_shopfront_imgs(frame)
            im = Image.fromarray(frame)
            t = time.localtime()
            current_time = time.strftime("%y-%m-%d_%H-%M-%S", t)
            im.save(f"{dataset_path}{current_time}.jpeg")
            time.sleep(sleep_time)