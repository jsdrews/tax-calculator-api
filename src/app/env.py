from pydantic_settings import BaseSettings


class Env(BaseSettings):
    test_server_protocol: str
    test_server_host: str
    test_server_port: int
    test_server_comm_max_retries: int
    test_server_comm_timeout_seconds: int
