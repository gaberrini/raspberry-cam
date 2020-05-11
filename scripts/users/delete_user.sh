if [ $# -ne 1 ]
  then
    echo "Expected arguments delete_user.sh [username]"
    exit 1
fi

# This script must be called from the root folder ./raspberry-cam
# Move to the project folder
cd ./flask_server
export FLASK_APP=picamera_server
# This script must be run after install_server_requirements.sh
python3 -m pipenv run flask user delete $1
exit 0
