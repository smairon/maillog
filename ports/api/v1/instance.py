from envparse import env

import specs

from . import bootstrap

env.read_envfile()

db_pool_config = specs.configs.storage.rdbs.DBPoolConfig()

app = bootstrap.api(
    rdbs_dsn=db_pool_config.dsn,
)
