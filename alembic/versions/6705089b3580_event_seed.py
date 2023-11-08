"""event seed

Revision ID: 6705089b3580
Revises: 
Create Date: 2023-11-08 19:52:30.563528

"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy import DateTime, Boolean, String, Integer, text
import sqlalchemy as sa
from sqlalchemy.orm import Session
from database.models import Event
from datetime import timedelta, datetime

# revision identifiers, used by Alembic.
revision: str = '6705089b3580'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

current_time = datetime.now()
seed_data = [
    {
        "title": "Sample Event one",
        "description": "This is a sample event 1.",
        "start": current_time,
        "end": current_time + timedelta(hours=1),
        "note": "Sample note 1",
        "repeat": "NEVER",
        "is_full_day": False,
        "color": "#50b500",
        "is_repeated_child": False,
        "repeat_interval": 1,
    },
    {
        "title": "Sample Event two",
        "description": "This is a sample event 2.",
        "start": current_time + timedelta(hours=2),
        "end": current_time + timedelta(hours=3),
        "note": "Sample note 2",
        "repeat": "NEVER",
        "is_full_day": False,
        "color": "#50b500",
        "is_repeated_child": False,
        "repeat_interval": 1,
    },
    # Add more seed data as needed
]

# Add the seed data


def add_seed_data():
    bind = op.get_bind()
    session = Session(bind=bind)
    for data in seed_data:
        event = Event(**data)
        session.add(event)
    session.commit()


def upgrade() -> None:
    add_seed_data()


def downgrade() -> None:
    pass
