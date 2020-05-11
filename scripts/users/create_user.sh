if [ $# -ne 3 ]
  then
    echo "Expected arguments create_user.sh [username] [password] [repeat_password]"
    exit 1
fi

# This script must be called from the root folder ./raspberry-cam
# Move to the project folder
cd ./flask_server
export FLASK_APP=picamera_server
# This script must be run after install_server_requirements.sh
python3 -m pipenv run flask user create $1 $2 $3
exit 0
