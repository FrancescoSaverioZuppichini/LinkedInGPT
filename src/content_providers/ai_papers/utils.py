import os
import tempfile

import cv2
import numpy as np
import requests
from pdf2image import convert_from_path
from PIL import Image


def download_and_convert_pdf(url: str):
    # Download the PDF
    response = requests.get(url)
    pdf_data = response.content

    # Save the PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(pdf_data)
        temp_pdf_path = f.name

    # Convert the first two pages of the PDF to images
    images = convert_from_path(temp_pdf_path, first_page=1, last_page=2)

    # Clean up the temporary PDF file
    os.unlink(temp_pdf_path)

    return images


def combine_images_horizontally(images):
    # Calculate the dimensions of the combined image
    width = sum(img.width for img in images)
    height = max(img.height for img in images)

    # Create a new blank image with the combined dimensions
    combined_image = Image.new("RGB", (width, height))

    # Paste the images one after the other vertically
    x_offset = 0
    for img in images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.width

    return combined_image


def create_image(pdf_url: str, image_file_path: str) -> str:
    # Download the PDF and convert the first two pages to images
    first_two_pages = download_and_convert_pdf(pdf_url)
    # Combine the images vertically
    combined_image = combine_images_horizontally(first_two_pages)
    # resize to full HD
    combined_image = combined_image.resize((1920, 1280))
    # Save the combined image to a file
    combined_image.save(image_file_path)
    return image_file_path
