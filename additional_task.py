import json
import re


def transform_table(table, websocket_response, base_ws):
    result = {
        "columns": [],
        "order_by": {},
        "conditions_data": {},
        "page_size": "",
        "row_height": "",
        "color_conditions": {},
        "module": "SO"
    }

    condition_pattern = re.compile(r'(\w+)=([\w\d]+)(?:=(rgba\(\d+,\d+,\d+,\d+(?:\.\d+)?\)))?')

    for i, row in enumerate(table):
        col_name = row.get("Columns View")
        ws_data = websocket_response.get(col_name)

        if ws_data:
            result["columns"].append({"index": ws_data["index"], "sort": i})

        for key, result_key in base_ws.items():
            value = row.get(key, "")
            if not value:
                continue

            if result_key in ["page_size", "row_height"]:
                result[result_key] = value
            elif result_key == "order_by":
                result[result_key] = {"direction": value, "index": ws_data["index"]}
            elif result_key in ["conditions_data", "color_conditions"]:
                filter_key = ws_data["filter"]
                parsed_conditions = []

                matches = condition_pattern.findall(value)
                for match in matches:
                    condition_type, condition_value, color = match
                    condition_data = {"type": condition_type, "value": condition_value}
                    if result_key == "color_conditions":
                        condition_data["color"] = color if color else ""
                    parsed_conditions.append(condition_data)

                result[result_key].setdefault(filter_key, []).extend(parsed_conditions)

    return json.dumps(result, indent=4)



# result = {'columns': [{'index': 'so_list_so_number', 'sort': 0},
#                       {'index': 'so_list_client_po', 'sort': 1},
#                       {'index': 'so_list_terms_of_sale', 'sort': 2}],
#           'order_by': {'direction': 'asc', 'index': 'so_list_terms_of_sale'},
#           'conditions_data': {'so_no': [{'type': 'equals', 'value': 'S110'},
#                                         {'type': 'equals', 'value': 'S111'}],
#                               'client_po': [{'type': 'equals', 'value': 'P110'}]},
#           'page_size': '25',
#           'row_height': '60',
#           'color_conditions': {'so_no': [{'type': 'equals', 'value': 'S110', 'color': 'rgba(172,86,86,1)'}],
#                                'client_po': [{'type': 'equals', 'value': 'S110', 'color': ''}, {'type': 'equals', 'value': 'S111', 'color': ''}],
#                                'term_sale': []},
#           'module': 'SO'}
