import json
from dataclasses import dataclass

from google.cloud import vision
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials as Credentials

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import japanize_matplotlib
from PIL import Image
import numpy as np


@dataclass
class ConfigJSON:
    type: str
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str
    universe_domain: str


def oauth(json_file_path: str) -> Credentials:
    return service_account.Credentials.from_service_account_file(json_file_path)


def get_image(img_path: str) -> bytes:
    with open(img_path, "rb") as file:
        return file.read()
    

def draw_texts(img_path: str, texts) -> None:
    # Open image file
    im = np.array(Image.open(img_path), dtype=np.uint8)

    # Create figure and axes
    fig, ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)

    # Create a Rectangle patch and text for each detected text
    for text in texts:
        vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        rect = patches.Polygon(vertices, linewidth=2, edgecolor='blue', facecolor='none')
        ax.add_patch(rect)
        ax.text(vertices[0][0], vertices[0][1], text.description, fontsize=8, color='blue')

    # Show the plot with detected texts
    plt.show()


def detect_text(img_path: str) -> None:

    credential = oauth("../baito-ocr-sample-ccb6bb9f060c.json")

    client = vision.ImageAnnotatorClient(credentials=credential)
    image = vision.Image(content=get_image(img_path))

    response = client.text_detection(image=image)

    texts = response.text_annotations
    print(type(texts))
    # <class 'proto.marshal.collections.repeated.RepeatedComposite'>
    draw_texts(img_path, texts)


    
    

if __name__ == "__main__":
    detect_text("../sheet1.jpg")
