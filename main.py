import csv
import requests
import schedule
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Dictionary to store the URL statuses
url_statuses = {}
url_statuses_summary = {}


def load_urls_from_csv(file_path):
    urls = []
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            name = row['name']
            url = row['url']
            urls.append((name, url))
    return urls


def check_url_status(name, url):
    try:
        response = requests.get(url)
        status = response.status_code
    except requests.exceptions.RequestException:
        status = -1
    ## The process should also bind a local port, to provide a summary of monitoring status in the past hour in any suitable format.
    ## Adds the url status to the array to be considered
    url_statuses[name].append(status)
    ## Checks for the amount of 200 status, adjusts status accordingly
    if len(url_statuses[name])> 5:
        if url_statuses[name][-5:].count(200) > 2:
            url_statuses_summary[name]="UP"
    elif url_statuses[name].count(200) > 2:
            url_statuses_summary[name]="UP"
    else:
        url_statuses_summary[name]="DOWN"


def check_all_urls(urls):
    for name, url in urls:
        check_url_status(name, url)


def schedule_url_check(urls):
    check_all_urls(urls)
    ## The process should pull all these urls every 10 minutes to check their HTTP status.
    schedule.every(10).minutes.do(check_all_urls, urls)


@app.route('/')
def default():
    return "Nothing to see here"

@app.route('/summary')
def get_summary():
    summary = {
        'timestamp': time.time(),
        'urls': url_statuses_summary
    }
    return jsonify(summary)


if __name__ == '__main__':
    csv_file_path = 'urls.csv'  # Accepts a csv file containing a list of up to 1000 urls with names at startup.
    urls = load_urls_from_csv(csv_file_path)

    # Schedule URL checks
    schedule_url_check(urls)

    # Run the Flask app to provide monitoring status summary over a port
    app.run(host='0.0.0.0', port=5008)
