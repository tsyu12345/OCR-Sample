from __future__ import annotations
from typing import Final as const

import sys
from dataclasses import dataclass
import easyocr
from easyocr import Reader
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import matplotlib.patches as patches
import japanize_matplotlib
import cv2

@dataclass
class RecognitionTextData:
    """
    easyocr.readtext()の戻り値のデータクラス
    """
    point: list[list[int]]
    text: str
    confidence: float


def detect_checkbox(filename: str) -> None:
    """
    チェックボックスを検出する
    """

    # Load image
    image = cv2.imread(filename, 0)
    # Perform edge detection
    edges = cv2.Canny(image, 30, 100)
    # Perform a dilation and erosion to close gaps in between object edges
    dilated_edges = cv2.dilate(edges, None, iterations=2)
    edges = cv2.erode(dilated_edges, None, iterations=1)
    # Find contours in the edge image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # Approximate the contour
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        # If the contour has 2 vertices, it could be a checkmark
        if len(approx) == 2:
            # Draw the contour on the image
            cv2.drawContours(image, [contour], -1, (255, 0, 0), 3)
    # Display the image
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def show_recognition_image(result: list[tuple(RecognitionTextData)], filename: str) -> None:
    """
    認識結果を画像で表示する
    """
    image: Image = Image.open(filename)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image)
    for i in result:
        try:
            bbox = np.array(i[0])
            print("ax.text({},{},{})".format(type(bbox[0,0]), type(bbox[0,1]), type(i[1])))
            ax.text(bbox[0,0], bbox[0,1], i[1], size=10, color="blue")
            r = patches.Rectangle(
                xy=(bbox[0,0], bbox[0,1]), 
                width=(bbox[2,0] - bbox[0,0]), 
                height=(bbox[2,1] - bbox[0,1]), 
                ec='g', 
                fill=False,
                linewidth=2.0)
            ax.add_patch(r)
        except:
            continue
    plt.show()
    print("showed")


def recognition(filename: str, allow_list: list[str]=[]) -> list[tuple[RecognitionTextData]]:
    reader: Reader = easyocr.Reader(
        lang_list=['ja', 'en'], 
        gpu=False
    )
    result = reader.readtext(filename, allowlist=allow_list, decoder='wordbeamsearch', detail=True)
    return result

def main() -> None:
    filename: str = sys.argv[1]
    if filename is None:
        raise ValueError("ファイル名を指定してください")
    
    result = recognition(filename=filename)
    for i in result:
        print(i)
    
    #show_recognition_image(result=result, filename=filename)
    detect_checkbox(filename=filename)
    
    