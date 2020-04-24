# This script must be called from the root folder ./raspberry-cam
# Move to the project folder
cd ./flask_server
# This script must be runned after install_server_requirements.sh
export FLASK_ENV=production
export SERVER_PORT=8080
python3 -m pipenv run gunicorn --threads 5 --workers 1 --bind 0.0.0.0:$SERVER_PORT main:main
