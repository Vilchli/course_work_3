import json
from datetime import datetime

filename = 'data/operation.json'


def load_json(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        raw_json_dict = json.load(f)

    json_dict = [item for item in raw_json_dict if item]

    return json_dict


def date_format(data_str: str):
    parsed = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S.%f")
    formatted_date = parsed.strftime("%d.%m.%Y")

    return formatted_date


def get_last_five_successful_operations(soft_list: list) -> list:
    successful_operations = [op for op in soft_list if op["state"] == "EXECUTED"]
    last_five_successful_operations = successful_operations[:5]

    return last_five_successful_operations


def sort_by_date(json_dict=None):
    sort_list = sorted(json_dict, key=lambda x: x.get("date"), reverse=True)
    return sort_list


def mask_card(operation_credentials: str) -> str:
    # Значение по ключу
    if operation_credentials:
        credentials_name = " ".join(operation_credentials.split(" ")[:-1])
        credentials_number = operation_credentials.split(" ")[-1]

        if len(credentials_number) == 16:
            # видны первые 6 цифр и последние 4
            number_hide = credentials_number[:6] + "*" * 6 + credentials_number[-4:]
            # разбито по блокам по 4 цифры
            number_sep = [number_hide[i:i + 4] for i in range(0, len(credentials_number), 4)]
            return f'{credentials_name} {" ".join(number_sep)}'

        elif len(credentials_number) == 20:
            return f'{credentials_name} {credentials_number.replace(credentials_number[:-4], "**")}'
    # Если по ключу не было получено значение, вернется строка N/A
    return "N/A"


def print_info(operations):

    for op in operations:
        operation_amount: dict = op['operationAmount']
        print(f"{date_format(op['date'])} {op['description']}\n"
              f"{mask_card(op.get('from'))} -> {mask_card(op.get('to'))}\n"
              f"{operation_amount.get('amount')} {operation_amount['currency'].get('name')}")
        print()
