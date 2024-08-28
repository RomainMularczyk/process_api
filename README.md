# Process Usage API

The following web application is designed to store and monitor processes usage on Linux systems.

## Collected metadata

The Process Usage API collects the following pieces of metadata :
* `id`: the process ID
* `user`: the user running the process
* `cpu`: CPU load used by the process
* `memory`: RAM memory used by the process
* `command`: name of the command used to run the process
* `time`: time elapsed since the beginning of the process

To make it easier for you to collect those pieces of data, you can use the `top` Linux command and filter out the metadata described above.

## Configuration

In order to configure the Process Usage API, you shoud first install a Python version superior or equal to `3.11`.

### Project dependencies

To install the project dependencies, you can refer to the `requirements.txt`and run :
```
pip install requirements.txt
```

### Serve the API

The Process Usage API was built using `FastAPI`. Please refer to its official documentation (https://fastapi.tiangolo.com/) to find additional informations on how to deploy such applications.

In order to serve the API, you can use a Python webserver such as `Uvicorn`. You'll find its official documentation here : https://www.uvicorn.org/.

If you want to serve the API with `Uvicorn`, you can run the following command :
```
uvicorn main:app --host 0.0.0.0 --port <port_number>
```

### Database

The Process Usage API requires an access to Postgres database (version 16.4) to run properly.

### Environment variables

In order to allow the Process Usage API to connect to a Postgres database, you should provide the following environment variables :
* `POSTGRES_USER`: the database user
* `POSTGRES_PASSWORD`: the database user's password
* `POSTGRES_HOST`: the host name of the database machine
* `POSTGRES_DB`: the name of the database
