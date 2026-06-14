import time
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
from awscrt import mqtt
from awsiot import mqtt_connection_builder
from core.sensor import get_sensor_reading

load_dotenv()

ENDPOINT = os.getenv("AWS_IOT_ENDPOINT")
CERT_PATH = os.getenv("AWS_IOT_CERT_PATH")
KEY_PATH = os.getenv("AWS_IOT_KEY_PATH")
CA_PATH = os.getenv("AWS_IOT_CA_PATH")
CLIENT_ID = os.getenv("AWS_IOT_CLIENT_ID")
TOPIC = "iot/telemetry"

def on_connection_interrupted(connection, error, **kwargs):
    print(f"Connection interrupted: {error}")

def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"Connection resumed: return_code={return_code}")

def main():
    print("Connecting to AWS IoT Core...")

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=CERT_PATH,
        pri_key_filepath=KEY_PATH,
        ca_filepath=CA_PATH,
        client_id=CLIENT_ID,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        clean_session=False,
        keep_alive_secs=30
    )

    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("Connected to AWS IoT Core!")
    print(f"Publishing to topic: {TOPIC}")
    print("Sending telemetry every 30 seconds.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            reading = get_sensor_reading()
            mqtt_connection.publish(
                topic=TOPIC,
                payload=json.dumps(reading),
                qos=mqtt.QoS.AT_LEAST_ONCE
            )
            print(f"Sent to AWS: {reading}")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        print("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected.")

if __name__ == "__main__":
    main()