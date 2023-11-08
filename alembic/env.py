from app.database.models import Base  # Make sure to adjust the import path
from alembic import context
from sqlalchemy import create_engine
from logging.config import fileConfig
from dotenv import load_dotenv
import os
load_dotenv()

database_url = os.getenv("DATABASE_URL")

# Ensure your SQLAlchemy models are imported here

# Modify this to use the correct database URL
DATABASE_URL = database_url


# This is automatically generated by Alembic, and it is used to configure logging.
# You may need to adjust the path to your logging configuration file.
fileConfig(context.config.config_file_name)

# Your SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Target metadata should match the metadata of your SQLAlchemy models (Base.metadata)
target_metadata = Base.metadata

# Alembic will use this for introspection purposes.
config = context.config

# Ensure that the `target_metadata` is set correctly
config.set_main_option('sqlalchemy.url', DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and a connection.

    """
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
