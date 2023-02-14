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
    """
    Reads a csv file using petl and converts it to dictionary skipping the header
    :param: csv_path: path of csv_file saved in filesystem
    """

    table = etl.fromcsv(csv_path)
    mappings_dict = {key: value for key, value in table[1:]}
    return mappings_dict


def get_metadata():
    """Fetches the metadata of objects in databse filtered by date"""

    return SwapiMetaData.objects.order_by("-date").values("filename", "date", "id")


def get_filedata(pk):
    """
    Fetches the metadata of a particular file from database
    :param: pk: primary key of the file you want to retrieve
    """

    try:
        return SwapiMetaData.objects.get(pk=pk)
    except Exception as e:
        return None


def table_to_list(table):

    a = []
    for i in etl.header(table):
        a.append(list(etl.values(table, i)))
    return a


def join_elements_of_lists(*args):
    """
    Joins n element of list n with n element of list n in sequence
    if only one list is provided, it returns that list
    """

    if len(args) < 2:
        return args[0]
    return [''.join(map(str, i)) for i in zip(*args)]


def count_occurrence(produced_list, main_list):
    """
    Counts occurrences of elements of a produced list in main list
    """
    from collections import Counter

    counts = dict(Counter(main_list))
    return [counts[i] for i in produced_list]

