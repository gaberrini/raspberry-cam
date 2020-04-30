# This script must be called from the root folder ./raspberry-cam
# Move to the project folder
cd ./flask_server
export APP_ENV=testing
export FLASK_ENV=testing
# This script must be runned after install_server_requirements.sh
# Run tests and take coverage
python3 -m pipenv run python -m coverage run -m unittest --verbose
# Create HTML report of coverage
python3 -m pipenv run coverage report
python3 -m pipenv run coverage html
