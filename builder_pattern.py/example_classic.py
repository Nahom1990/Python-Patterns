class DatabaseConfig:
    def __init__(self,host,port,database,username,password,ssl,pool_size,timeout,) -> None:
        self.host=host
        self.port=port
        self.database=database
        self.username=username
        self.password=password
        self.ssl=ssl
        self.pool_size=pool_size
        self.timeout=timeout

"""can also use dataclasses for the above like """
from dataclasses import dataclass
@dataclass
class DatabaseConfig2:
    host:str
    port:int
    database:str
    username:str
    password:str
    ssl:str
    pool_size:int
    timeout:int

    

class DatabaseConfigBuilder:
    def __init__(self) -> None:
        self.host=None
        self.port=None
        self.database=None
        self.username=None
        self.password=None
        self.ssl=False
        self.pool_size=5
        self.timeout=30

    def set_host(self,host):
        self.host=host
        return self
    def set_port(self,port):
        self.port=port
        return self
    def set_database(self,database):
        self.database=database
        return self
    def set_username(self,username):
        self.username=username
        return self
    def set_password(self,password):
        self.password=password
        return self
    def set_ssl(self,ssl):
        self.ssl=ssl
        return self

    def set_pool_size(self,pool_size):
        self.pool_size=pool_size
        return self

    def set_timeout(self,timeout):
        self.timeout=timeout
        return self
    def build(self):
        if self.host is None:
            raise ValueError("host is required")

        if self.port is None:
            raise ValueError("port is required")

        if self.database is None:
            raise ValueError("database is required")
        if not 1 <= self.port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        if self.pool_size<=0:
            raise ValueError("pooolsize must be greater than 0")
        return(DatabaseConfig(self.host,
                              self.port,
                              self.database,
                              self.username,
                              self.password,
                              self.ssl,
                              self.pool_size,
                              self.timeout))

config = (
    DatabaseConfigBuilder()
    .set_host("localhost")
    .set_port(5432)
    .set_database("mydb")
    .set_username("admin")
    .set_password("secret")
    .set_ssl(True)
    .set_pool_size(10)
    .set_timeout(60)
    .build()
)

"""The Builder isn't the product.

The Builder is a temporary object whose responsibility is:

"Help me construct the product correctly."
"""