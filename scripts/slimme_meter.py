
import csv
from datetime import datetime
import time
import re
import os
from pprint import pprint


# deze codes gaan naar de csv, in deze volgorde. Als het bestand nieuw is worden
# ze bovenaan gezet
csv_codes = [
    'timestamp',
    '1-0:1.7.0',
    '1-0:1.8.1',
    '1-0:1.8.2',
    '1-0:2.7.0',
    '1-0:2.8.1',
    '1-0:2.8.2',
    '0-1:24.2.1',
]


class SlimmeMeterData:
    def __init__(self):
        self.data = {}

    def add_raw_line(self, line_string):
        m = re.search('(.-[^()]+)(\(.*\))', line_string)
        if m:
            key = m.group(1)
            if key in self.data:
                # als een
                print('dubbele sleutel in readout: %s' % res[key])
            else:
                self.data[key] = m.group(2)

    def save_to_csv(self):
        # als we moeten gaan saven moeten we de waarden extracten
        csv_values = []
        t = time.time()

        for c in csv_codes:
            if c == 'timestamp':
                csv_values.append(t)

            elif c in obis_codes:
                if obis_codes[c]['extract'] == 'el':
                    v = self._extract_el_val(self.data[c])
                    csv_values.append(v['value'])

                elif obis_codes[c]['extract'] == 'gas':
                    v = self._extract_gas_val(self.data[c])
                    csv_values.append(v['value'])

                else:
                    print('geen idee hoe %s te parsen' % c)
                    csv_values.append('?')

            else:
                print('geen idee wat je wilt met %s' % c)

        # determine file name

        datestring = datetime.utcfromtimestamp(t).date().isoformat()

        filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "../../meterstanden/data/daily/",
            datestring + '.csv'
        ))

        newfile = not os.path.isfile(filepath)

        try:
            with open(filepath, "a+") as f:
                writer = csv.writer(f)
                if newfile:
                    writer.writerow(csv_codes)
                writer.writerow(csv_values)

        except:
            print('file error')

    def _extract_el_val(self, data):
        res = re.search('^\(([\d.]+)\*(.+)\)$', data)

        retval = {
            'value': res.group(1),
            'unit': res.group(2),
        }

        return retval

    def _extract_gas_val(self, data):
        res = re.search('^\([\d]+[^)]*\)\(([\d.]+)\*(.+)\)$', data)

        retval = {
            'value': res.group(1),
            'unit': res.group(2),
        }

        return retval


# lijstje met obis codes
obis_codes = {
    '0-0:1.0.0': {
        'desc': 'Date-time stamp of the P1 message',
        'extract': '',
    },
    '0-0:96.1.1': {
        'desc': 'Equipment identifier',
        'extract': '',
    },
    '0-0:96.13.0': {
        'desc': 'Text message max 1024 characters.',
        'extract': '',
    },
    '0-0:96.13.1': {
        'desc': '???',
        'extract': '',
    },
    '0-0:96.14.0': {
        'desc': 'Tariff indicator electricity. The tariff indicator can also be used to switch tariff dependent loads e.g boilers. This is the responsibility of the P1 user',
        'extract': '',
    },
    '0-0:96.7.21': {
        'desc': 'Number of power failures in any phase',
        'extract': '',
    },
    '0-0:96.7.9': {
        'desc': 'Number of long power failures in any phase',
        'extract': '',
    },
    '0-1:24.1.0': {
        'desc': 'Device-Type',
        'extract': '',
    },
    '0-1:24.2.1': {
        'desc': 'Last 5-minute value (temperature converted), gas delivered to client in m3, including decimal values and capture time',
        'extract': 'gas',
    },
    '0-1:96.1.0': {
        'desc': 'Equipment identifier (Gas)',
        'extract': '',
    },
    '1-0:1.7.0': {
        'desc': 'Actual electricity power delivered (+P) in 1 Watt resolution',
        'extract': 'el',
    },
    '1-0:1.8.1': {
        'desc': 'Meter Reading elctricity delivered to client (Tariff 1) in 0,001 kWh',
        'extract': 'el',
    },
    '1-0:1.8.2': {
        'desc': 'Meter Reading electricity delivered to client (Tariff 2) in 0,001 kWh',
        'extract': 'el',
    },
    '1-0:2.7.0': {
        'desc': 'Actual electricity power received (-P) in 1 Watt resolution',
        'extract': 'el',
    },
    '1-0:2.8.1': {
        'desc': 'Meter Reading electricity delivered by client (Tariff 1) in 0,001 kWh',
        'extract': 'el',
    },
    '1-0:2.8.2': {
        'desc': 'Meter Reading electricity delivered by client (Tariff 2) in 0,001 kWh',
        'extract': 'el',
    },
    '1-0:21.7.0': {
        'desc': 'Instantaneous active power L1 (+P) in W resolution',
        'extract': '',
    },
    '1-0:22.7.0': {
        'desc': 'Instantaneous active power L1 (-P) in W resolution',
        'extract': '',
    },
    '1-0:31.7.0': {
        'desc': 'Instantaneous current L1 in A resolution.',
        'extract': '',
    },
    '1-0:32.32.0': {
        'desc': 'Number of voltage sags in phase L1',
        'extract': '',
    },
    '1-0:32.36.0': {
        'desc': 'Number of voltage swells in phase L1',
        'extract': '',
    },
    '1-0:41.7.0': {
        'desc': 'Instantaneous active power L2 (+P) in W resolution',
        'extract': '',
    },
    '1-0:42.7.0': {
        'desc': 'Instantaneous active power L2 (-P) in W resolution',
        'extract': '',
    },
    '1-0:51.7.0': {
        'desc': 'Instantaneous current L2 in A resolution.',
        'extract': '',
    },
    '1-0:52.32.0': {
        'desc': 'Number of voltage sags in phase L2',
        'extract': '',
    },
    '1-0:52.36.0': {
        'desc': 'Number of voltage swells in phase L2',
        'extract': '',
    },
    '1-0:61.7.0': {
        'desc': 'Instantaneous active power L3 (+P) in W resolution',
        'extract': '',
    },
    '1-0:62.7.0': {
        'desc': 'Instantaneous active power L3 (-P) in W resolution',
        'extract': '',
    },
    '1-0:71.7.0': {
        'desc': 'Instantaneous current L3 in A resolution.',
        'extract': '',
    },
    '1-0:72.32.0': {
        'desc': 'Number of voltage sags in phase L3 ',
        'extract': '',
    },
    '1-0:72.36.0': {
        'desc': 'Number of voltage swells in phase L3',
        'extract': '',
    },
    '1-0:99.97.0': {
        'desc': 'Power Failure Event Log (long power failures)',
        'extract': '',
    },
    '1-3:0.2.8': {
        'desc': 'Version information for P1 output',
        'extract': '',
    },
}
