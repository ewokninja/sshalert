#!/usr/bin/env python3

import json
import logging
import requests
import os, time
import subprocess, select

# Initialization
log = logging.getLogger('sshalert')
log.setLevel(logging.INFO)

with open('.env') as f:
    for line in f:
        if line.startswith('#'):
            continue
        key, value = line.replace('export ', '', 1).strip().split('=', 1)
        os.environ[key] = value

try:
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
except:
    logging.critical("ERROR: Have you exported all required environment variables? (TARGET_PHONE_NUMBER, NEXMO_KEY, NEXMO_SECRET)")
    exit(1)


def poll_logfile(filename):
    """
    Polls a logfile for sudo commands or ssh logins.
    """
    f = subprocess.Popen(["tail", "-f", "-n", "0", filename], encoding="utf8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    while True:
        if p.poll(1):
            process_log_entry(f.stdout.readline())
        time.sleep(1)


def process_log_entry(logline):
    """
    Check a logline and see if it matches the content we care about.
    """
    # If it's a local sudo exec
    if "sudo" and "COMMAND" in logline:
        send_message(logline)
    
    # If it's an SSH login
    elif "ssh" and "Accepted" in logline:
        send_message(logline)
    return


def send_message(msg):
    """
    Sends a text message to the target slack channel, via slack webhook.
    Returns 0 if everything worked; otherwise 1
    """
    # Set the webhook_url to the one from your secrets.env file
    webhook_url = slack_webhook
    slack_data = {'text': msg}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )

    # Error Handling
    if response.status_code != 200:
        logging.error("ERROR: failed to send message: {} CODE: {}".format(response.text, response.status_code))
    else:
        logging.info("Successfully sent slack message")

# If this program was called directly (as opposed to imported)
if __name__ == "__main__":
    # poll the auth.log file
    poll_logfile("/var/log/auth.log")
