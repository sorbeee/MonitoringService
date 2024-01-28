from datetime import datetime
import json

global config_path
config_path = "config.json"


def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def convert_time_format(input_str):
    input_datetime = datetime.strptime(input_str, '%Y-%m-%dT%H:%M:%S.%f')
    output_str = input_datetime.strftime('%H:%M %d/%m/%Y')

    return output_str


def format_drive_info(drives):
    formatted_str = ""

    for drive in drives:
        formatted_str += \
            f"Drive: {drive['name']}   Total: {drive['total']}   Used: {drive['used']}   Free: {drive['free']}\n"

    return formatted_str
