import csv
import json
from pathlib import Path


def read_file(path: str):
    ext = Path(path).suffix
    with open(path) as file_contents:
        if ext == '.csv':
            reader = csv.DictReader(file_contents)
            for line in reader:
                print(line)
        elif ext == '.json':
            data = json.load(file_contents)
            data_keys = list(dict.keys(data))
            key_array = 'IO_MASTER/POST_JOB_REPORT_DB.TOTALS_JOB_1.FLUID_EVENT_TOTAL.ARRAY'
            data_array = data[key_array]
            # print('Headers: ', data_keys)
            print('Data Array: ', data_array)
        else:
            for line in file_contents:
                print(line)


