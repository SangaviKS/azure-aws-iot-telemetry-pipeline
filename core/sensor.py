import time
import random
import json

def get_sensor_reading(device_id="sensor-device-01"):
    return {
        "deviceId": device_id,
        "temperature": round(random.uniform(60, 120), 2),
        "pressure": round(random.uniform(14, 16), 2),
        "vibration": round(random.uniform(0, 5), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }