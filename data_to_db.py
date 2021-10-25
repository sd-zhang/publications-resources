import profile_extractor
import dataset
from datetime import datetime
import pytz
from dateutil.parser import parse as timeparse

energy_data_dir = "D:/Smart star data/SunDance_data_release/energy/"
weather_data_dir = "D:/Smart star data/SunDance_data_release/weather/"

files = profile_extractor.get_filenames_in_path(energy_data_dir)
# files = random.sample(files, 10)

# print(files)
profiles = dict()
db = dataset.connect("postgresql://postgres:postgres@localhost/SunDance")
for file in files:
    profile_name = 'SunDance_' + file.split('_')[1].split('.')[0]
    print(profile_name)

    energy_data = energy_data_dir + file
    weather_data = weather_data_dir + profile_name + '.csv'
    profile = profile_extractor.extract_data(energy_data, weather_data, 'america/denver')

    if profile_name not in db.tables:
        table = db.create_table(profile_name, primary_id='time')
    else:
        table = db[profile_name]
    table.upsert_many(profile, ['time'])
