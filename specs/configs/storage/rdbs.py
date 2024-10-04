import pydantic
import pydantic_settings
import settings


class DBPoolConfig(pydantic_settings.BaseSettings):
    host: str
    password: pydantic.SecretStr = pydantic.Field(..., env="rdbs_password")
    port: int = 5532
    user: str = 'postgres'
    database: str = settings.RDBS_DB_NAME
    pool_capacity: str = "5,20"

    @property
    def dsn(self):
        dsn = f'postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}'
        return dsn

    class Config:
        case_sensitive = False
        secrets_dir = '/run/secrets'
        env_prefix = "rdbs_"
