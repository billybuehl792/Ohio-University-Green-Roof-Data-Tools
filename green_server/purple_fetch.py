# purple_fetch.py - retrieve current purpleAir data

import requests
import json


class PurpleFetch:

    desired_data = {
        'ID': 'PurpleAir sensor ID',
        'Lat': 'Latitude position info',
        'Lon': 'Longitude position info',
        'PM2_5Value': 'Current PM2.5 value',
        'LastSeen': 'Last seen data time stamp in UTC',
        'timeSinceModified': 'Time between last two readings in milliseconds',
        'Uptime': 'Sensor uptime in seconds',
        'RSSI': 'Sensor WiFi signal strength in dBm',
        'Adc': 'The voltage reading on the analog input of the control board.',
        'p_0_3_um': 'Channel A 0.3 micrometer particle counts per deciliter of air',
        'p_0_5_um': 'Channel A 0.5 micrometer particle counts per deciliter of air',
        'p_1_0_um': 'Channel A 1.0 micrometer particle counts per deciliter of air',
        'p_2_5_um': 'Channel A 2.5 micrometer particle counts per deciliter of air',
        'p_5_0_um': 'Channel A 5.0 micrometer particle counts per deciliter of air',
        'p_10_0_um': 'Channel A 10.0 micrometer particle counts per deciliter of air',
        'pm1_0_cf_1': 'CF=1 PM1.0 particulate mass in ug/m3 (is actually CF=ATM)',
        'pm2_5_cf_1': 'CF=1 PM2.5 particulate mass in ug/m3 (is actually CF=ATM)',
        'pm10_0_cf_1': 'CF=1 PM10.0 particulate mass in ug/m3 (is actually CF=ATM)',
        'pm1_0_atm': 'ATM PM1.0 particulate mass in ug/m3 (is actually CF=1)',
        'pm2_5_atm': 'ATM PM2.5 particulate mass in ug/m3 (is actually CF=1)',
        'v': 'Real time or current PM2.5 Value',
        'v1': 'PM2.5 10 minute average',
        'v2': 'PM2.5 30 minute average',
        'v3': 'PM2.5 1 hour average',
        'v4': 'PM2.5 6 hour average',
        'v5': 'PM2.5 24 hour average',
        'v6': 'PM2.5 1 week average'
    }

    # retrieve purple air data
    @staticmethod
    def get_data(purple_id):
        purpleResponse = requests.get(f'https://www.purpleair.com/json?&show={purple_id}')
        data = json.loads(purpleResponse.content)['results'][0]
        stats = json.loads(data['Stats'])

        for item in stats:
            data[item] = stats[item]

        del data['Stats']

        return data
