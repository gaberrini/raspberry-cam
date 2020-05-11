# This script must be called from the root folder ./raspberry-cam
# Move to the project folder
cd ./flask_server
# This script must be runned after install_server_requirements.sh
export FLASK_ENV=development
export SERVER_PORT=8080

python3 -m pipenv run python main.py -debug
