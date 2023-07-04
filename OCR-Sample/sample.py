from __future__ import annotations
from typing import Final as const

import sys
from dataclasses import dataclass
import easyocr
from easyocr import Reader


@dataclass
class RecognitionTextData:
    """
    easyocr.readtext()の戻り値のデータクラス
    """
    point: list[list[int]]
    text: str
    confidence: float


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
    
    