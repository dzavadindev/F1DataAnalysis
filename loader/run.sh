#!/bin/bash

# This retrieves the parent dir of the script (parent of 'loader' dir)
PROJECT_DIR=$(dirname "$(dirname "$(readlink -f "$0")")")

NODE_SERVER_PATH="$PROJECT_DIR/raw/api"
LOADER_PATH="$PROJECT_DIR/loader/load_data.py"
SERVER_IP="http://127.0.0.1:3000"
API_IMAGE_NAME="drivers-api-i"
API_CONTAINER_NAME="drivers-api-c"

kill_node_server () {
  docker rm --force "$(docker ps -qa --filter "name=drivers-api-c")"
}

# ---------  ⌄⌄⌄IN CASE YOU ARE HAVING TROUBLE RUNNING THIS SCRIPT UNCOMMENTING THIS MAY HELP⌄⌄⌄ -----------
  
# if ! (poetry env use "$(which python)"); then # assuming your python version is above 3.11, as that is required by poetry
#   echo "Failed to set Python 3.11 environment with Poetry"
#   exit 1
# fi

# echo "Installing Python dependencies..."
# poetry install

# ---------  ^^^IN CASE YOU ARE HAVING TROUBLE RUNNING THIS SCRIPT UNCOMMENTING THIS MAY HELP^^^ -----------

echo "Starting Node.js server for endpoints..."
docker build "$NODE_SERVER_PATH" -t "$API_IMAGE_NAME"
docker run -p 3000:3000 --name "$API_CONTAINER_NAME" -d "$API_IMAGE_NAME:latest" 

timeout_period=10
end_time=$(( $(date +%s) + timeout_period ))
until [ "$(curl -s -o /dev/null -w "%{http_code}" $SERVER_IP)" -eq 200 ] || [ "$(date +%s)" -ge $end_time ]; do
  sleep 2
done

trap kill_node_server EXIT # if script bye, server also bye

echo "Loading raw data into DuckDB..."
if ! (poetry run python "$LOADER_PATH"); then
  echo "Failed to load data into DuckDB"
  exit 1
fi
echo "Raw data loaded into DuckDB"

echo "Running dbt..."
if ! (poetry run dbt build --project-dir="$PROJECT_DIR"); then
  echo "dbt build failed"
  exit 1
fi
echo "dbt process completed"

echo "Updating sources in Evidence..."
npm i # assuming you are running the project for the first time 
if ! (npm --prefix "$PROJECT_DIR" run sources); then
  echo "Updating sources in Evidence failed"
  exit 1
fi
echo "Sources updated in Evidence!"
