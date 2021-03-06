# Raspberry camera controller

Here you can find a Web Server developed to run in a [Raspberry Pi 3 B+]. The server has been made to manage the [Camera module v2].

# Index

* [Server features](#server-features)
    * [Live stream](#live-stream)
    * [Capturing mode](#capturing-mode)
* [System setup](#system-setup)
    * [Operative system](#operative-system)
    * [Activate camera](#activate-camera)
    * [VNC Remote access](#vnc-remote-access)
    * [Python environment](#python-environment)
        * [pip package manager](#pip-package-manager)
        * [pipenv environment manager](#pipenv-environment-manager)
* [Running server](#running-server)
    * [Environment variables](#environment-variables)
    * [Scripts to run the server](#scripts-to-run-the-server)
        * [System setup script](#1-system-setup-script)
        * [Python environment setup script](#2-python-environment-setup-script)
        * [Run server script](#3-run-server-script)
            * [Development mode](#development-mode)
            * [Development environment](#development-environment)
        * [Optional - cleanup virtualenv script](#4-optional---cleanup-virtualenv-script)
        * [Run tests with coverage script](#5-run-tests-with-coverage-script)
* [Users management](#users-management)
    * [Scripts for user management](#scripts-for-user-management)
        * [Create users script](#1-create-users-script)
        * [Change user password script](#2-change-user-password-script)
        * [Delete user script](#3-delete-user-script)

# Server features

**THE FRONTEND IS INTENDED TO BE USED WITH GOOGLE CHROME**

The server features are protected with [user log in](#users-management). When the user is not authenticated it will be redirected to the log in page.

`{SERVER_HOST}:{SERVER_PORT}/login`

The server have:

* [Live stream](#live-stream)
* [Capturing mode](#capturing-mode)

## Live stream

In the endpoint `{SERVER_HOST}:{SERVER_PORT}/camera/ui/stream` there will be a live stream of the PiCamera

## Capturing mode

The capturing mode will store captures from the camera every X seconds while it's activated. The capture interval will be configurable.

In the endpoint `{SERVER_HOST}:{SERVER_PORT}/camera/ui/captures/config` you will find the configuration and management section for the capturing mode

In the endpoint `{SERVER_HOST}:{SERVER_PORT}/camera/ui/captures/` you will find the captures, and you can apply datetime filters defining from date and until date.

# System setup

## Operative system

For the development of the Web Server I used the following operative system, **[Raspbian Buster with desktop and recommended software]**

To burn the image in the SD I used [Raspberry Pi Imager]

The latest version of this operative system already comes with Python 2.7 and Python 3.7, here we will use Python 3.7

When first start the OS, is good to update the packages running:

`sudo apt-get update`

## Activate camera

The server has been made to manage the [Camera module v2], here you can find the [instructions to enable it].

## VNC Remote access

To make the access and control of the Raspberry easier we can use a VNC Viewer from your PC. Follow the instructions here [VNC Viewer instructions].

## Python environment

This server is developed using Python 3.7 that comes with the Raspbian OS.

The script `./scripts/setup_system_env.sh` located at the [scripts](#running-server) folder will install the system requirements for the web server.

More about deploying scripts in the following section.


### pip package manager

To update the pip package manager we run

`python3 -m pip install -U pip`

To properly use pip3 in Raspbian is better to run it using

`python3 -m pip`

You can check the installed version running

`python3 -m pip -V`

### pipenv environment manager

To easily install the packages [pipenv] has been used.

To install it run

`python3 -m pip install pipenv`

To properly use [pipenv] in Raspbian we need to execute it as follow

`python3 -m pipenv`

# Running server

In this section you can find the instructions to run the server and configure it.

## Environment variables

* **FLASK_ENV** affect the running mode, if nothing is defined by default will be `production`, you can also define with the value of `development`.
* **SERVER_HOST** configure the host when running the server, default value is `0.0.0.0`
* **SERVER_PORT** configure the port when running the server, default value is `8080`
* **APP_ENV** if running tests the value must be `testing`, and the camera class will be forced to be `TestCamera`. When development should be `development`

## Server logging

When creating the Flask app in `./flask_server/picamera_server/picamera_server.py` in the `create_app` function the logging is configured using `logging.conf.dictConfig`.

The configuration will include logging to a file and will place the log files in the folder `./flask_server/picamera_server/logs`.

When running test environment the log to a file will be disabled.

## Scripts to run the server

The code comes with scripts to run that will help to setup the system for the server and run it.

**All the scripts must be run from the parent directory**

`./`

**When trying to run the scripts might be possible that they don't have execution rights, you can add them to all the scripts with the following command**

`chmod +x ./scripts/*`

### 1) System setup script

To setup the Raspbian OS to run the server you should update the OS packages and pip package manager.

For this step you can run the script

`./scripts/setup_system_env.sh`

The command lines to do this are:

```
# Update system packages
sudo apt-get update
# Upgrade pip
python3 -m pip install -U pip
# Install pipenv
python3 -m pip install pipenv
# Install lxml for testing
sudo apt-get install python3-lxml
```

### 2) Python environment setup script

To setup the python environment to run the server you can run the following script

`./scripts/install_server_requirements.sh`

The command lines to do this are:

```
# Move to the project folder
cd ./flask_server
# Install pipenv packages
python3 -m pipenv --site-packages --python=python3 install --dev
```

### 3) Run server script

#### Development mode

After installing all the requirements you can run the server with the following script

`./scripts/run_server_debug.sh`

This script will run the server in development mode with the following commands

```
# Move to the project folder
cd ./flask_server
# This script must be runned after install_server_requirements.sh
export FLASK_ENV=development
export SERVER_PORT=8080
python3 -m pipenv run python main.py -debug
```

The `run_server_debug.sh` script will run the server in debug mode.

#### Development environment

If you run the server in a development environment like a Windows machine, there will be a **`TestCamera class`** defined to simulate a camera and be able to test the server and validate its features.

### 4) Optional - cleanup virtualenv script

If we want to cleanup the created virtualenv we can do it with the script

`./scripts/clean_up_environment.sh`

The script will run the following commands:

```
# Move to the project folder
cd ./flask_server
# Remove pipenv
python3 -m pipenv --rm
```

### 5) Run tests with coverage script

The server have tests written with the framework [unittest] to get the coverage the framework [coverage] is used.

The tests will use the module [lxml] to validate the rendered HTML elements, the package is installed in the system interpreter using the script `./scripts/setup_system_env.sh`, and then included in the virtual env thanks to the `--site-packages` flag.

When running the tests the environment variable **APP_ENV** should be set to **`testing`**

The coverage module will have the following configuration file:

`./flask_server/.coveragerc`

In which we specify the paths to ignore in the coverage analysis.

To run the tests and get a coverage report you can run the following script:

`./scripts/run_tests_with_coverage.sh`

The coverage report will be shown in the terminal after the tests run. Also a HTML report will be created, to see the report you should open the following created file:

`./flask_server/htmlcov/index.html`

The script will run the following commands:

```
cd ./flask_server
export APP_ENV=testing
export FLASK_ENV=testing
# This script must be runned after install_server_requirements.sh
# Run tests and take coverage
python3 -m pipenv run python -m coverage run -m unittest --verbose
# Create HTML report of coverage
python3 -m pipenv run coverage report
python3 -m pipenv run coverage html
```

# Users management

The server features are protected by user log in. To create/update/delete users, you can do it using flask commands.

The flask commands are dependant on the environment variable **FLASK_APP**

You can find [scripts to execute the user commands](#scripts-for-user-management)

## Scripts for user management

In the scripts folder you can find scripts for user management

**All the scripts must be run from the parent directory**

`./`

**When trying to run the scripts might be possible that they don't have execution rights, you can add them to all the scripts with the following command**

`chmod +x ./scripts/users/*`

**The scripts must be run after running the scripts for [system setup script](#1-system-setup-script) and the [python environment setup script](#2-python-environment-setup-script)**

### 1) Create users script

The script to create users is located at

`./scripts/users/create_user.sh`

This script will receive 3 positional arguments:

* username
* password
* password_repeat

The script will execute the following commands:

```
cd ./flask_server
export FLASK_APP=picamera_server
python3 -m pipenv run flask user create $1 $2 $3
```

### 2) Change user password script

The script to update users passwords is located at:

`./scripts/users/change_password.sh`

This script will receive 3 positional arguments:

* username
* password
* password_repeat

The script will execute the following commands:

```
cd ./flask_server
export FLASK_APP=picamera_server
python3 -m pipenv run flask user change_password $1 $2 $3
```

### 3) Delete user script

The script to delete users is located at:

`./scripts/users/delete_user.sh`

This script will receive 1 positional arguments:

* username

The script will execute the following commands:

```
cd ./flask_server
export FLASK_APP=picamera_server
python3 -m pipenv run flask user delete $1
```

[Raspberry Pi 3 B+]: https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/
[Camera module v2]: https://www.raspberrypi.org/products/camera-module-v2/
[instructions to enable it]: https://www.raspberrypi.org/documentation/usage/camera/
[Raspbian Buster with desktop and recommended software]: https://www.raspberrypi.org/downloads/raspbian/
[Raspberry Pi Imager]: https://www.raspberrypi.org/downloads/
[VNC Viewer instructions]: https://www.raspberrypi.org/documentation/remote-access/vnc/
[pipenv]: https://pipenv-es.readthedocs.io/
[unittest]: https://docs.python.org/3/library/unittest.html
[coverage]: https://coverage.readthedocs.io/en/coverage-5.1/
[lxml]: https://lxml.de/index.html
