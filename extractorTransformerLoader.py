import uuid

import pandas as pd

from objects.Leg import Leg
from objects.Schedule import Schedule

import csv
import json
import os
from datetime import datetime


def extract_sailing_schedules(carrier_id):
    # params = {'page': page, 'page_size': 100}
    # url = f"https://api.linescape.io/v1/sailings?carrier_id={carrier_id}"
    # response = requests.get(url, params=params)
    with open('externalApiResponse/data.json', 'r') as openfile:
        json_object = json.load(openfile)
    return json_object


def transform_schedules(data, page, page_size):
    begin = int((int(page) - 1) * int(page_size))
    end = int(int(page) * int(page_size))
    transformed_data = []
    for schedule in data['items'][begin:end]:
        new_schedule = Schedule(schedule['carrier']['id'])
        for leg_data in schedule['legs']:
            leg = Leg(schedule['carrier']['id'], leg_data['start']['port']['code'], leg_data['end']['port']['code'],
                      leg_data['start']['date'], leg_data['end']['date'], leg_data['voyage'])
            new_schedule.add_leg(leg)
        transformed_data.append(new_schedule)
    return transformed_data


def load_to_csv(carrier_id, data):
    file_path = os.path.join("schedulesCache/", f"{carrier_id}_SchedulesCache.csv")
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'carrier', 'origin', 'destination', 'departureDateTime', 'arrivalDateTime', 'duration',
                      'creationTime', 'lastModifiedTime']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for schedule in data:
            for leg in schedule.legs:
                writer.writerow({
                    'id': str(uuid.UUID(int=int(leg.voyage))),
                    'carrier': str(schedule.carrier_id),
                    'origin': str(leg.origin),
                    'destination': str(leg.destination),
                    'departureDateTime': str(leg.departure_date),
                    'arrivalDateTime': str(leg.arrival_date),
                    'duration': str(leg.duration.days),
                    'creationTime': str(datetime.now().isoformat()),
                    'lastModifiedTime': str(datetime.now().isoformat())
                })


def load_to_csv_exist(carrier_id, data):
    file_path = os.path.join("schedulesCache/", f"{carrier_id}_SchedulesCache.csv")
    existing_data = pd.read_csv(file_path)

    for schedule in data:
            for leg in schedule.legs:
                # Convert ID to string
                leg_id = str(uuid.UUID(int=int(leg.voyage)))

                # Check if ID exists in existing data
                if leg_id in existing_data['id'].values:
                    # Update the existing record
                    existing_data.loc[existing_data['id'] == leg_id, 'carrier'] = str(schedule.carrier_id)
                    existing_data.loc[existing_data['id'] == leg_id, 'origin'] = str(leg.origin)
                    existing_data.loc[existing_data['id'] == leg_id, 'destination'] = str(leg.destination)
                    existing_data.loc[existing_data['id'] == leg_id, 'departureDateTime'] = str(leg.departure_date)
                    existing_data.loc[existing_data['id'] == leg_id, 'arrivalDateTime'] = str(leg.arrival_date)
                    existing_data.loc[existing_data['id'] == leg_id, 'duration'] = str(leg.duration.days)
                    existing_data.loc[existing_data['id'] == leg_id, 'lastModifiedTime'] = str(
                        datetime.now().isoformat())
                else:
                    # Add new record
                    new_row = {
                        'id': leg_id,
                        'carrier': str(schedule.carrier_id),
                        'origin': str(leg.origin),
                        'destination': str(leg.destination),
                        'departureDateTime': str(leg.departure_date),
                        'arrivalDateTime': str(leg.arrival_date),
                        'duration': str(leg.duration.days),
                        'creationTime': str(datetime.now().isoformat()),
                        'lastModifiedTime': str(datetime.now().isoformat())
                    }
                    existing_data = existing_data.append(new_row, ignore_index=True)

    existing_data.to_csv(file_path, index=True, encoding='utf-8')
