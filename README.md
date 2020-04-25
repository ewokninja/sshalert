# SSHAlert script

A simple script that sends a slack message when someone logs in or becomes root. This is forked from Dave at Tutorial Linux, he's great, go follow him and check out the original.

## To run
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
NOTE: I don't use a virtual environment for this particular use but I'm leaving these instructions here because generally I think it's a good idea.

## To install

Use rsync to copy this project directory to your target server. Adjust file paths as necessary in sshalert.service.

Pass your secrets in as env vars, or use the secrets.env file in this repo (and referenced in the sshalert.service systemd unit file):

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY
```


## Naked Ubuntu 18.04 Server Setup
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install virtualenv python3-virtualenv

# copy this repo over, adjust paths in sshalert.service
# copy sshalert.service to /etc/systemd/system/ into whichever target directory you want (probably multi-user)
systemctl daemon-reload
systemctl start sshalert
systemctl enable sshalert
```

TODO: add more instructions ;-)

