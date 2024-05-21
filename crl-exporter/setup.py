import sys
import requests
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Gauge
import schedule
import time
import datetime

# Отключаем предупреждения о небезопасных запросах (при подключении к хостам с самоподписанным сертификатом)
requests.packages.urllib3.disable_warnings()

# Cтруктура метрик
certificates_info = Gauge('certificates_info', 'Certificate Information',
                         ['url', 'dn', 'from_date', 'to_date', 'oid', 'serial_number', 'crl', 'size'])
certificates_epoch = Gauge('certificates_epoch', 'Certificate Expiration Epoch Timestamp', ['dn'])

# Функция запроса к API
def fetch_data_from_api(username, password, api_url):
    auth = (username, password)
    response = requests.get(api_url, auth=auth, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {api_url}. Status code: {response.status_code}")

# Функция расчета epoch
def calculate_expiration(to_date):
    to_date_datetime = datetime.datetime.strptime(to_date, "%Y/%m/%d %H:%M:%S")
    to_date_timestamp = to_date_datetime.timestamp()
    return to_date_timestamp


# Функция парсинга ответа от API
def parse_and_export(data, api_url):
    table = data.get("table", [])

    if not table:
        print(f"No data to export from {api_url}.")
        return

    for item in table:
        dn = item.get("dn", "")
        from_date = item.get("from", "")
        to_date = item.get("to", "")
        oid = item.get("oid", "")
        serial_number = item.get("serialNumber", "")
        crl = item.get("crl", "")
        size = float(item.get("size", 0.0))

        certificates_info.labels(url=api_url, dn=dn, from_date=from_date, to_date=to_date,
                                 oid=oid, serial_number=serial_number, crl=crl, size=size).set(size)

        to_date_epoch = calculate_expiration(to_date)
        certificates_epoch.labels(dn=dn).set(to_date_epoch)


# Парс переменных из файла
def read_variables_from_file(filename):
    variables = {}
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split("=")
                variables[key.strip()] = value.strip()
    return variables

def job():
    try:
        # Чтение username/password из file/env
        if os.path.isfile("secrets.txt"):
            secrets = read_variables_from_file("secrets.txt")
            username = secrets.get("USERNAME")
            password = secrets.get("PASSWORD")
        else:
            username = os.getenv("USERNAME")
            password = os.getenv("PASSWORD")


        # Чтение API_URL из file/env
        if os.path.isfile("api_urls.txt"):
            api_urls = read_variables_from_file("api_urls.txt").get("API_URLS")
            api_urls = api_urls.split(",")
        else:
            api_urls = os.getenv("API_URLS").split(",")

        for api_url in api_urls:
            data = fetch_data_from_api(username, password, api_url)
            parse_and_export(data, api_url)
    
    # работа с ошибками
    except Exception as e:
        print(f"Error: {e}")
        error_message = f"Error: {e}\n"
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message_with_time = f"[{current_time}] {error_message}"
        print(error_message_with_time)
        with open("error.txt", "a") as file:
            file.write(error_message_with_time)
        sys.stdout.flush()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'certificates_info ' + certificates_info._collect() + b'\n')
            self.wfile.write(b'certificates_epoch ' + certificates_epoch._collect() + b'\n')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')


if __name__ == '__main__':
    # Порт для Prometheus
    start_http_server(8001)

    # Наш джоб будет дергать API каждые 3 минуты
    schedule.every(3).minutes.do(job)

   # Порт HTTP server для API запросов
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)

    # Sleep если не используется
    while True:
        schedule.run_pending()
        time.sleep(1)