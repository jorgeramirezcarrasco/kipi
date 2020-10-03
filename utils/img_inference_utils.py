import cv2
import numpy as np
from math import sqrt

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