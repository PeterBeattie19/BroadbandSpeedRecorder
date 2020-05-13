import pandas as pd
from datetime import datetime
import time
import speedtest as st


def test_speeds():
    speed_test = st.Speedtest()
    speed_test.get_best_server()
    ping = speed_test.results.ping
    down = speed_test.download()
    up = speed_test.upload()
    download_mbs = round(down / (10**6), 2)
    upload_mbs = round(up / (10**6), 2)
    return ping, download_mbs, upload_mbs


def update_csv(internet_speeds, csv_file_name="internet_speeds_dataset.csv"):
    # Get today's date in the form Month/Day/Year
    date_today = datetime.today().strftime("%m/%d/%Y_%H:%M:%S")

    # Load the CSV to update
    try:
        csv_dataset = pd.read_csv(csv_file_name, index_col="Date")
    # If there's an error, assume the file does not exist and create\
    # the dataset from scratch
    except FileNotFoundError:
        csv_dataset = pd.DataFrame(
            list(),
            columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)"]
        )

    # Create a one-row DataFrame for the new test results
    results_df = pd.DataFrame(
        [[internet_speeds[0], internet_speeds[1], internet_speeds[2]]],
        columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)"],
        index=[date_today]
    )

    updated_df = csv_dataset.append(results_df, sort=False)
    updated_df.to_csv(csv_file_name, index_label="Date")


def start_recording(delay, csv_file_name="internet_speeds_dataset.csv"):
    while True:
        try:
            _results = test_speeds()
            update_csv(_results, csv_file_name=csv_file_name)
            print(_results)
            time.sleep(delay)
            print("AWAKE")
        except KeyboardInterrupt:
            print("SHUTDOWN")
            return


interval_minutes = 10
start_recording(interval_minutes*60)
