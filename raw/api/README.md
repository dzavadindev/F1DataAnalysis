# Drivers and Constructors API Server

This folder contains a simple REST API server. Build and run the Docker image using:

```sh
docker build -t f1-api .
docker run -p 3000:3000 f1-api
```

Example usage:

```
http://localhost:3000/drivers           # Get list of drivers
http://localhost:3000/drivers/de_vries  # Get driver information for Nyck de Vries

http://localhost:3000/teams             # Get list of teams
http://localhost:3000/teams/spyker      # Get team information for Spyker F1
```