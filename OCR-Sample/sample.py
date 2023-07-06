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


@dataclass
class RecognitionTextData:
    """
    easyocr.readtext()の戻り値のデータクラス
    """
    point: list[list[int]]
    text: str
    confidence: float


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
            print(i[1])
            ax.text(bbox[0,0], bbox[0,1], i[1], size=30, fontname="MS Gothic",color="black")
            r = patches.Rectangle(xy=(bbox[0,0], bbox[0,1]), width=(bbox[2,0] - bbox[0,0]), height=(bbox[2,1] - bbox[0,1]), ec='g', fill=False,linewidth='10.0')
            ax.add_patch(r)
        except:
            continue
    plt.show()


def recognition(filename: str) -> list[tuple[RecognitionTextData]]:
    reader: Reader = easyocr.Reader(
        lang_list=['ja'], 
        gpu=False
    )
    result = reader.readtext(filename)
    return result

def main() -> None:
    filename: str = sys.argv[1]
    if filename is None:
        raise ValueError("ファイル名を指定してください")
    
    result = recognition(filename=filename)
    for i in result:
        print(i)
    
    show_recognition_image(result=result, filename=filename)
    
    