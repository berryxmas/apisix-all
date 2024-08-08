# APISIX Demo Project

This project demonstrates the use of APISIX, PostgreSQL, and other tools in a Dockerized environment.

## Tools Used
- **APISIX**: A dynamic, real-time, high-performance API gateway.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Docker**: A platform for developing, shipping, and running applications in containers.
- **Grafana**: An open-source platform for monitoring and observability.
- **Prometheus**: A monitoring and alerting toolkit.
- **Nginx**: A high-performance web server.

## Project Structure
- `apisix_conf/`: Configuration files for APISIX.
- `dashboard_conf/`: Configuration files for the dashboard.
- `docker-compose.yml`: Docker Compose file to set up the environment.
- `etcd_conf/`: Configuration files for etcd.
- `grafana_conf/`: Configuration files for Grafana.
- `mkcert/`: Certificates for local development.
- `myapi/`: Source code for the custom API.
- `postgres_conf/`: Configuration files for PostgreSQL.
- `postgres_data/`: Data directory for PostgreSQL.
- `prometheus_conf/`: Configuration files for Prometheus.
- `upstream/`: Configuration files for upstream services.

## Running the Project

### Prerequisites
- Docker
- Docker Compose

### Setting Up FastAPI Environment

#### Navigating to the `myapi` Folder
```sh
cd myapi
```
#### Creating a Virtual Environment
##### Mac
```sh
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```
##### Windows
```sh
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```
##### Installing Requirements
```sh
# Make sure the virtual environment is activated, then install the requirements
pip install -r requirements.txt
```

### Setting Up Environment Variables
This project uses a `.env` file to manage environment variables. An example file `.env.example` is provided. To get started, copy this file to `.env` and update the values as needed.
```sh
cp .env.example .env
```
Edit the `.env` file to set your own values for the environment variables.

### Starting the Project


#### Mac
```sh
# Pull the latest images
docker compose pull

# Build and start the containers
docker-compose up --build
```

#### Windows
```sh
# Pull the latest images
docker-compose pull

# Build and start the containers
docker-compose up --build
```
#### Stopping the Project
```sh
# Stop and remove containers, networks, volumes, and images created by up
docker-compose down -v

# Remove all unused volumes
docker volume prune -f
```
#### Resetting PostgreSQL Data
```sh
# Remove PostgreSQL data to start from scratch
rm -rf ./postgres_data
```
#### Accessing PostgreSQL
```sh
# Access PostgreSQL container
docker exec -it CONTAINER_ID psql -U USER -d DATABASE
```
#### Basic PostgreSQL Commands
```sql
-- List all databases
\l

-- Connect to a specific database
\c DATABASE_NAME

-- List all tables in the current database
\dt

-- Show table schema
\d TABLE_NAME

-- Add tables from init.sql
\i /path/to/init.sql
```
#### Managing Users and Privileges
```sql
-- Create a new user
CREATE USER newuser WITH PASSWORD 'password';

-- Grant all privileges on a database to a user
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO newuser;

-- Grant specific privileges on a table to a user
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE mytable TO newuser;

-- Revoke specific privileges on a table from a user
REVOKE INSERT ON TABLE mytable FROM newuser;

-- Show current user
SELECT current_user;

-- Show all users
\du
```
### Setting Up Basic Routes in APISIX
#### Create a Test Route
```sh
curl -i http://localhost:9080/apisix/admin/routes/1 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-d '{
  "uri": "/test",
  "plugins": {
    "response-rewrite": {
      "body": "{\"message\": \"Hello from APISIX\"}"
    }
  },
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "127.0.0.1:80": 1
    }
  }
}'
```
Now you can see the route has been created in the apisix dashboard.
#### Check the Route
```sh
curl -X GET "http://localhost:9080/test"
```
#### Create an API Route
```sh
curl -i http://localhost:9080/apisix/admin/routes/1 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-d '{
  "uri": "/api/v1/incidents",
  "methods": ["GET"],
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "myapi:8000": 1
    }
  }
}'
```
### Additional Docker Commands
```sh
# SSH into a container
docker-compose exec apisix sh

# Check etcd container health
docker exec -it CONTAINER_ID etcdctl --endpoints=http://127.0.0.1:2379 endpoint health

# Check APISIX container connection
docker exec -it CONTAINER_ID apk add curl
docker exec -it CONTAINER_ID curl -L http://etcd:2379/health
```
### Understanding Ports
- Port 9180: Admin API port for configuring routes, services, and other settings in APISIX.
- Port 9080: Default port where APISIX listens for incoming HTTP requests and routes them based on the configurations set via the Admin API.

