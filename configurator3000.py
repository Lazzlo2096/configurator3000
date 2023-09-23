import tkinter as tk
from tkinter import ttk
import json
import argparse
import os

parser = argparse.ArgumentParser(description="Генератор конфигурационного файла")
parser.add_argument("input_file", help="Имя файла для чтения JSON-схемы")
parser.add_argument("output_file", help="Имя файла для записи конфигурационного файла")
args = parser.parse_args()

with open(args.input_file, 'r') as schema_file:
    schema = json.load(schema_file)

def load_config(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as config_file:
            try:
                config_data = json.load(config_file)
                return config_data
            except json.JSONDecodeError:
                return None
    return None

config_data = load_config(args.output_file)

def validate_int(input_text):
    if input_text == "":
        return True
    try:
        int(input_text)
        return True
    except ValueError:
        return False

def generate_config():
    config = {}
    for section, fields in schema.items():
        config[section] = {}
        for field, field_type in fields.items():
            if field_type == "string":
                value = entry_values[section][field].get()
            elif field_type == "int":
                value = entry_values[section][field].get()
                if value == "":
                    value = None
                else:
                    value = int(value)
            elif field_type == "bool":
                value = combobox_values[section][field].get()
                if value == "True":
                    value = True
                else:
                    value = False
            else:
                value = combobox_values[section][field].get()
                if value == "":
                    value = None
            config[section][field] = value

    with open(args.output_file, 'w') as config_file:
        json.dump(config, config_file, indent=4)
    status_label.config(text="Конфигурационный файл сохранен")


root = tk.Tk()
root.title("Генератор конфигурационного файла")

entry_values = {}
combobox_values = {}
validation_int = root.register(validate_int)
row = 0
for section, fields in schema.items():
    tk.Label(root, text=section, font=('Helvetica', 14)).grid(row=row, column=0, columnspan=2)
    row += 1
    entry_values[section] = {}
    combobox_values[section] = {}
    for field, field_type in fields.items():
        label_text = f"{field} ({field_type})"
        tk.Label(root, text=label_text).grid(row=row, column=0, sticky='e')
        if field_type == "int":
            entry_values[section][field] = tk.StringVar()
            entry = tk.Entry(root, textvariable=entry_values[section][field], validate="all", validatecommand=(validation_int, '%P')) # validate="key"
            entry.grid(row=row, column=1)
            if config_data and section in config_data and field in config_data[section]:
                entry_values[section][field].set(config_data[section][field])
        elif field_type == "string":
            entry_values[section][field] = tk.StringVar()
            entry = tk.Entry(root, textvariable=entry_values[section][field])
            entry.grid(row=row, column=1)
            if config_data and section in config_data and field in config_data[section]:
                entry_values[section][field].set(config_data[section][field])
        elif field_type == "bool":
            combobox_values[section][field] = tk.StringVar()
            combobox = ttk.Combobox(root, textvariable=combobox_values[section][field], values=["True", "False"])
            combobox.grid(row=row, column=1)
            combobox.set("True")
            if config_data and section in config_data and field in config_data[section]:
                combobox.set(str(config_data[section][field]))
        else:
            combobox_values[section][field] = tk.StringVar()
            combobox = ttk.Combobox(root, textvariable=combobox_values[section][field], values=field_type)
            combobox.grid(row=row, column=1)
            combobox.set(field_type[0])
            if config_data and section in config_data and field in config_data[section]:
                combobox.set(str(config_data[section][field]))
        row += 1

generate_button = tk.Button(root, text="Создать конфиг", command=generate_config)
generate_button.grid(row=row, column=0, columnspan=2)

status_label = tk.Label(root, text="", font=('Helvetica', 12))
status_label.grid(row=row+1, column=0, columnspan=2)

root.mainloop()
