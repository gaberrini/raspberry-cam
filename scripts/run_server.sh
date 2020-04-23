# This script must be called from the root folder ./raspberry-cam
# Move to the project folder
cd ./flask_server
# This script must be runned after install_server_requirements.sh
export FLASK_ENV=development
python3 -m pipenv run python main.py -debug
