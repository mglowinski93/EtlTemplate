# ExtractTransformLoadTemplate

Template for Extract-Transform-Load (
[ETL](https://aws.amazon.com/what-is/etl/)
).

## Prerequisites

Running of this project locally requires the following tools to be
present on the host system:

* `docker` (version 23.05.0+)
* `docker compose` (version 2.21.0+)

## Development environment

To run development environment
1. Go into `docker/development/` folder
2. Execute

  ```bash
  docker compose up
  ```

3. Open `http://localhost:8000` in browser

#### Running tests

1. Build development environment as described above
2. Execute

  ```bash
  docker exec -it etl-template-backend-development make
  ```

#### Admin Panel

Admin Panel is a tool for managing records in a database.
The panel is available at
[http://localhost:8000/admin-panel](http://localhost:8000/admin).

Username: `admin`  
Password: `admin`

#### API Documentation

API Documentation is available at
[http://localhost:8000/api/swagger/](http://localhost:8000/api/swagger/).

## Working with repository

1. `backend` folder must be marked as `Sources Root` in `IDE` to make imports work
