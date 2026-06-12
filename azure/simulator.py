import time
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient, Message
from core.sensor import get_sensor_reading

load_dotenv()
CONNECTION_STRING = os.getenv("AZURE_IOTHUB_CONNECTION_STRING")

def main():
    print("Connecting to Azure IoT Hub...")
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    print("Connected. Sending telemetry every 30 seconds.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            reading = get_sensor_reading()
            message = Message(json.dumps(reading))
            message.content_type = "application/json"
            message.content_encoding = "utf-8"
            client.send_message(message)
            print(f"Sent to Azure: {reading}")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()