## Contributing

### Prerequisites
docker compose is required to run the application. To install docker compose follow these instructions: https://docs.docker.com/compose/install/

This repo using Taskfile to manage the tasks. To install Taskfile follow these instructions: https://taskfile.dev/installation/. Using the [install script](https://taskfile.dev/installation/#install-script) option is recommended as you can install the binary to a local directory if you don't want to install it globally.

If you don't want to install Taskfile, you can open the file and run the commands manually.

To see the available tasks run `task`.

### Start the api
```bash
task up
```

### Stop the api
```bash
task down
```

### Inspect the logs
```bash
task logs
```

### Run the tests
```bash
task test
```

### Format the code
```bash
task format
```

### Environment Variables
The following environment variables are used in the application (these are all set in the .env file):
- `API_PORT`: The port the server listens on. Default is 8080.
- `API_LOG_LEVEL`: The log level of the application. Default is debug.
- `TEST_SERVER_PROTOCOL`: The protocol of the test server. Default is http.
- `TEST_SERVER_HOST`: The host of the test server. Default is test-server.
- `TEST_SERVER_PORT`: The port of the test server. Default is 5001.
- `TEST_SERVER_COMM_MAX_RETRIES`: The maximum number of retries for communication with the test server. Default is 5.
- `TEST_SERVER_COMM_TIMEOUT_SECONDS`: The timeout in seconds for communication with the test server. Default is 10.

### Code Structure
Poetry is used to manage the dependencies of the application. The dependencies are listed in the pyproject.toml file.

In the src folder there are two main folders:
- `app`: This folder contains the code for the api.
- `tests`: This folder contains the unit tests.

The `app` folder is structured as follows:
- `main.py` contains the FastAPI application.
- `env.py` contains the environment variables used by the api.
- `logging.py` contains the logging configuration.
- `routes` contains the routes for the api.

Each `routes` folder is structured as follows:
- `models.py` contains the pydantic models used by the route.
- `routes.py` contains the route logic.
- `controllers.py` contains the controller logic.
