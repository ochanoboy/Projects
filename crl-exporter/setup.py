import sys
import requests
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Gauge
import schedule
import time
import datetime

# When connecting to hosts with a self-signed certificate (optional)
requests.packages.urllib3.disable_warnings()

# Metric template
certificates_info = Gauge('certificates_info', 'Certificate Information',
                         ['url', 'dn', 'from_date', 'to_date', 'oid', 'serial_number', 'crl', 'size'])
certificates_epoch = Gauge('certificates_epoch', 'Certificate Expiration Epoch Timestamp', ['dn'])

# Request to API func
def fetch_data_from_api(username, password, api_url):
    auth = (username, password)
    response = requests.get(api_url, auth=auth, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {api_url}. Status code: {response.status_code}")

# epoch func
def calculate_expiration(to_date):
    to_date_datetime = datetime.datetime.strptime(to_date, "%Y/%m/%d %H:%M:%S")
    to_date_timestamp = to_date_datetime.timestamp()
    return to_date_timestamp


# Parsing data func from API
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


# Parsing vars from file func 
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
        # Read username/password from file/env
        if os.path.isfile("secrets.txt"):
            secrets = read_variables_from_file("secrets.txt")
            username = secrets.get("USERNAME")
            password = secrets.get("PASSWORD")
        else:
            username = os.getenv("USERNAME")
            password = os.getenv("PASSWORD")


        # Read API_URL from file/env
        if os.path.isfile("api_urls.txt"):
            api_urls = read_variables_from_file("api_urls.txt").get("API_URLS")
            api_urls = api_urls.split(",")
        else:
            api_urls = os.getenv("API_URLS").split(",")

        for api_url in api_urls:
            data = fetch_data_from_api(username, password, api_url)
            parse_and_export(data, api_url)
    
    # Error handling
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
    # Port Prometheus
    start_http_server(8001)

    # Get data from URL every 3 min
    schedule.every(3).minutes.do(job)

   # Port HTTP server
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)

    # Sleep delay
    while True:
        schedule.run_pending()
        time.sleep(1)
