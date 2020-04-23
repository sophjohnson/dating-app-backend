# Dating App - Backend

## Database Setup

#### Requirements:
1. Oracle

#### Build Database

Create Oracle user:
``

Build database:
`$ ./database/build.sh`

## API Setup

#### Requirements:
1. Python >= 3.6
2. Pip3

#### Start API

Initialize virtual environment:
`$ source ./api/.venv/bin/activate`

Install requirements (inside virtual environment):
`$ (.venv) pip3 install -r ./api/requirements.txt

Run app:
`$ (.venv) gunicorn -b 0.0.0.0:8800 api.api.app --reload`
