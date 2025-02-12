import re
import numpy as np
import pdfplumber
import cv2

from pdf2image import convert_from_path
from pyzbar.pyzbar import decode



def extract_barcodes(image):
    barcodes = []
    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    decoded_objects = decode(gray)  # Используется функция decode() модуля pyzbar
    for obj in decoded_objects:
        barcodes.append(obj.data.decode("utf-8"))
    return barcodes

def extract_pdf_data(pdf_path):
    # pdf_converted = convert_from_path(pdf_path, poppler_path=r"C:\Program Files\poppler-24.08.0\Library\bin")
    pdf_converted = convert_from_path(pdf_path)
    barcodes = []
    for barcode in pdf_converted:
        barcodes.extend(extract_barcodes(barcode))
    barcodes.reverse()

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    lines = text.split("\n")
    return lines, barcodes

def parse_lines(lines, barcodes):
    data = {}

    data['GRIFFON AVIATION SERVICES LLC'] = barcodes[0]

    pattern = r"([\w#\.\s]+):\s*([^:\n]*)\s+([\w#\.\s]+):\s*([\w#\-/\.]*)?"     # Регулярное выражение для нахождения соответствий

    for index, line in enumerate(lines):
        if line.count(":") > 1:
            # Если в строке два `:`, разбираем с регуляркой
            matches = re.findall(pattern, line)
            for match in matches:
                data[match[0].strip()] = match[1].strip()
                data[match[2].strip()] = match[3].strip()
        elif ":" in line:
            # Если `:` только один, разбираем стандартно
            key, value = map(str.strip, line.split(":", 1))
            data[key] = value

        if 'NOTES:' in line:
            if index + 1 < len(lines) and ":" not in lines[index + 1]:
                data["NOTES"] = lines[index + 1].strip()

    if "TAGGED BY" in data and len(barcodes) > 1:
        data["TAGGED BY"] = barcodes[1]

    return data

def parse_pdf(pdf_path):
    lines, barcodes = extract_pdf_data(pdf_path)
    parsed_data = parse_lines(lines, barcodes)

    return {
        "result": parsed_data
    }