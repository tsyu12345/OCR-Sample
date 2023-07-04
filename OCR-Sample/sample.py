from __future__ import annotations
from typing import Final as const

import easyocr
from easyocr import Reader


def recognition() -> list:
    reader: Reader = easyocr.Reader(
        lang_list=['ja'], 
        gpu=False
    )
    result = reader.readtext('sheet1.jpg')
    return result

def main() -> None:
    result = recognition()
    for i in result:
        print(i)
    
    