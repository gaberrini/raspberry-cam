# This script will setup the systen environment
# Update system packages
sudo apt-get update
# Upgrade pip
python3 -m pip install -U pip
# Install pipenv
python3 -m pip install pipenv
# Install lxml for testing
sudo apt-get install python3-lxml
