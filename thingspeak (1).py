import requests
import csv
import datetime
import time
import os

# URL của Thingspeak để lấy dữ liệu sensor
thingspeak_url = "https://api.thingspeak.com/channels/2315582/feeds.json?api_key=L4UP07991VIZ8ZUW&results=1"

# Đường dẫn và tên file CSV để lưu dữ liệu
csv_file_path = "data6.csv"

# Hàm ghi dữ liệu sensor vào tệp CSV
def write_sensor_data_to_csv(csv_file_path, sensor_data):
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, mode='a', newline='') as csv_file:
        sensor_fields = list(sensor_data.keys())
        writer = csv.DictWriter(csv_file, fieldnames=sensor_fields)

        # Ghi tiêu đề các trường dữ liệu (chỉ ghi một lần khi file chưa tồn tại)
        if not file_exists:
            writer.writeheader()

        # Ghi dữ liệu từ sensor vào file CSV
        writer.writerow(sensor_data)

# Hàm lấy dữ liệu từ Thingspeak
def get_sensor_data():
    response = requests.get(thingspeak_url)
    data = response.json()

    # Kiểm tra xem dữ liệu có tồn tại không
    if "feeds" in data and len(data["feeds"]) > 0:
        sensor_data = data["feeds"][0]
        return sensor_data

    return None

# Hàm chạy chương trình ghi dữ liệu
def run_program():
    while True:
        # Lấy dữ liệu từ Thingspeak
        sensor_data = get_sensor_data()

        if sensor_data is not None:
            # Lấy thời gian hiện tại
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sensor_data["timestamp"] = current_time

            # Ghi dữ liệu từ sensor vào tệp CSV
            write_sensor_data_to_csv(csv_file_path, sensor_data)

        # Ngừng thực hiện trong một khoảng thời gian cố định trước khi cập nhật lại dữ liệu
        time.sleep(10)

# Chạy chương trình
run_program()