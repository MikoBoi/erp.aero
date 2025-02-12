import pdfplumber
from pdf_parser import parse_pdf

def check_pdf_structure(etalon_pdf, test_pdf):
    etalon_data = parse_pdf(etalon_pdf)
    etalon_text = etalon_data["result"]

    test_data = parse_pdf(test_pdf)
    test_text = test_data["result"]

    missing_keys = set(etalon_text.keys()) - set(test_text.keys())
    extra_keys = set(test_text.keys()) - set(etalon_text.keys())

    # Проверяем расположение ключей (по координатам)
    with pdfplumber.open(etalon_pdf) as pdf:
        etalon_positions = {word["text"]: (word["x0"], word["top"]) for page in pdf.pages for word in page.extract_words()}

    with pdfplumber.open(test_pdf) as pdf:
        test_positions = {word["text"]: (word["x0"], word["top"]) for page in pdf.pages for word in page.extract_words()}

    position_match = etalon_positions == test_positions

    return {
        "missing_keys": list(missing_keys),
        "extra_keys": list(extra_keys),
        "position_match": position_match
    }
