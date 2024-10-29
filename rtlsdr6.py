import time
import json
from rtlsdr import *
import numpy as np
from datetime import datetime, timedelta



sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.048e6  # Hz
sdr.center_freq = 70e6     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

# print(sdr.read_samples(512))

data_list = []

for i in range(12260):
    samples = sdr.read_samples(256*1024)
    real_part = samples[128*1024].real
    imag_part = samples[128*1024].imag
    magnitude = np.sqrt(real_part**2 + imag_part**2)
    power_db = 10 * np.log10(magnitude**2 + 1e-10)

    current_time = datetime.now()
    shifted_time = current_time - timedelta(hours=7)

    data_entry = {
            'timestamp': shifted_time.strftime('%Y/%m/%d %H:%M:%S'),
            'power_db' : power_db
            }
    data_list.append(data_entry)

    with open('data2.json', mode='w') as file:
        json.dump(data_list, file, indent=4)
    print(data_entry)

    time.sleep(5)
    
sdr.close()
            