import os
from os import walk
import pandas as pd
import utils

def get_filenames_in_path(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    return f


def extract_data(energy_file, weather_file, timezone):
    with open(weather_file, 'r') as f:
        line_1 = f.readline().lower().strip().rstrip('\n').replace('"','').split(',')
        tz = line_1[5]
        if tz != timezone:
            return []

    with open(energy_file, 'r') as f:
        data = list()

        # read header row
        headers = f.readline().lower().strip().rstrip('\n').replace('"','').split(',')
        datetime_col = headers.index('date & time')
        if not ('use [kw]' in headers or 'usage [kw]' in headers):
            return []

        try:
            use_col = headers.index('use [kw]')
        except ValueError:
            use_col = headers.index('usage [kw]')


        try:
            gen_col = headers.index('gen [kw]')
        except ValueError:
            gen_col = headers.index('generation [kw]')


        # read data
        while True:
            row = f.readline().strip().rstrip('\n').split(',')
            if not row[0]:
                break

            # get data from each row
            datetime = row[datetime_col]
            use = row[use_col]
            gen = row[gen_col]

            data_row = {'time': utils.timestr_to_timestamp(datetime, timezone),
                        'consumption': int(round(float(use) * 1000, 0)),
                        'generation': int(round(float(gen) * 1000, 0))}
            data.append(data_row)

        # data_df = pd.DataFrame(data)
        # data_df['time'] = pd.to_datetime(data_df['time'], format='%Y-%m-%d %H:%M:%S.%f')
        # df[(df['dt'] > '2014-07-23 07:30:00') & (df['dt'] < '2014-07-23 09:00:00')]
        return data
