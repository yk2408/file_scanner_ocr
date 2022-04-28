import json
import re

import pytesseract
from PIL import Image


class FileScanner:
    def __init__(self, image_path):
        self.image = Image.open(image_path)

        # download and install mcr and eng language
        #  https://github.com/BigPino67/Tesseract-MICR-OCR/blob/master/Tessdata/mcr.traineddata
        #  https://github.com/tesseract-ocr/tessdata_best/blob/main/eng.traineddata

    def image_to_string(self, lang):
        return pytesseract.image_to_string(self.image, lang=lang).split("\n")

    def fetch_result(self, regex, language):
        for text_data in self.image_to_string(language):
            if re.match(regex, text_data):
                return text_data


if __name__ == "__main__":
    file_name = 'inputs.json'
    print(f'Reading data from {file_name} file')
    with open(file_name, 'r') as file:
        # Reading image data from json file
        file_content = file.read()
        json_data = json.loads(file_content)
    print('Working on Extracting MICR code and Payer name from the image')
    for data in json_data:
        image_path = data.get('image_path')
        regex_micr = data.get('regex_for_micr')
        regex_payer = data.get('regex_for_payer')
        fs = FileScanner(image_path)
        micr_code = fs.fetch_result(regex_micr, 'mcr')
        payer_name = fs.fetch_result(regex_payer, 'eng')
        print(f"Micr Code: {micr_code}")
        print(f"Payer Name: {payer_name}")
