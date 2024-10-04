import functools

import fire
from envparse import env

import specs
import internals
import ports
import settings

if __name__ == "__main__":
    env.read_envfile()

    db_pool_config = specs.configs.storage.rdbs.DBPoolConfig()
    migrator = ports.rdbs.migrator.Migrator(
        rdbs_dsn=db_pool_config.dsn,
        migrations_dir=settings.MIGRATION_DIR
    )

    fire.Fire({
        "api:run": internals.scripts.api_run,
        "rdbs:upgrade": migrator.upgrade,
        "rdbs:downgrade": migrator.downgrade,
        "parse:log": functools.partial(
            internals.scripts.logs_parser,
            rdbs_dsn=db_pool_config.dsn,
            file_path=settings.LOGFILE_PATH
        )
    })
