from pdf_parser import parse_pdf
from pdf_checker import check_pdf_structure
from additional_task import transform_table

import sys

def main():
    task = sys.argv[1] if len(sys.argv) > 1 else "1"

    if task == "1":
        pdf_to_read = "test_task.pdf"
        test_samples = ["test_task.pdf", "test_file_1.pdf", "test_file_2.pdf", "test_file_3.pdf"]

        Task1 = parse_pdf(pdf_to_read)
        print("Задание 1. Читаем всю возможную информацию")
        print(Task1)

        print("\n")

        print("Задание 2. Проверяем с эталонным файлом. Проверка на расположение и на наличие ключей в файле")
        # Есть три разных сэмпла помимо оригинала,
        # сравниваем с оригиналом чтобы убедиться корректность работы проверки расположения
        for sample in test_samples:
            Task2 = check_pdf_structure(sample, pdf_to_read)
            print(Task2)

        print("\n")

    elif task == "3":
        print("Задание 3. Дополнительное задание")
        print("\n")

        table = [
            {'Columns View': 'SO Number', 'Sort By': '', 'Highlight By': 'equals=S110=rgba(172,86,86,1),equals=S111',
             'Condition': 'equals=S110,equals=S111', 'Row Height': '60', 'Lines per page': '25'},
            {'Columns View': 'Client PO', 'Sort By': '', 'Highlight By': 'equals=P110,equals=P111',
             'Condition': 'equals=P110', 'Row Height': '', 'Lines per page': ''},
            {'Columns View': 'Terms of Sale', 'Sort By': 'asc', 'Highlight By': 'equals=S110=rgba(172,86,86,1)',
             'Condition': '', 'Row Height': '', 'Lines per page': ''}]

        websocket_response = {'Client PO': {'index': 'so_list_client_po', 'filter': 'client_po'},
                              'SO Number': {'index': 'so_list_so_number', 'filter': 'so_no'},
                              'Terms of Sale': {'index': 'so_list_terms_of_sale', 'filter': 'term_sale'}}

        base_ws = {'Columns View': 'columns',
                   'Sort By': 'order_by',
                   'Condition': 'conditions_data',
                   'Lines per page': 'page_size',
                   'Row Height': 'row_height',
                   'Highlight By': 'color_conditions'}

        result = transform_table(table, websocket_response, base_ws)
        print(result)

    else:
        print("❌ Ошибка: неизвестное задание.")



if __name__ == "__main__":
    main()