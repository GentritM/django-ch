import random
import string
from datetime import datetime
import petl as etl

from challenge_swapi.models import SwapiMetaData


def generate_filename() -> str:
    """Static method that generates random name for a file"""

    letters = string.ascii_letters
    filename = "".join([random.choice(letters) for _ in range(16)])
    return f"{filename}.csv"


def get_current_date() -> str:
    """Generates current datetime in the particular format mm.dd.hh.mm. am/pm"""

    return datetime.today().strftime("%b. %d. %Y %I:%M %p")


def csv_to_dict(csv_path: str) -> dict:
    """Reads a csv file using petl and converts it to dictionary skipping the header"""

    table = etl.fromcsv(csv_path)
    mappings_dict = {key: value for key, value in table[1:]}
    return mappings_dict

def get_metadata():
    """Returns objects ordered by date"""
    return SwapiMetaData.objects.order_by("-date").values("filename", "date", "id")
