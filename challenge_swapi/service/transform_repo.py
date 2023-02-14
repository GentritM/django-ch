import requests
from requests import Response
from functools import wraps
import petl as etl

from .client import SwapiClient
from django.conf import settings
from .utils import generate_filename, get_current_date, csv_to_dict
from challenge_swapi.models import SwapiMetaData


class TransformSwapiData:

    def __init__(self, client: SwapiClient):
        self.client = client
        self.response_list: Response = None

    def _check_response_list(func):
        """Decorator that checks that the response_list attribute of the repo is not None"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.response_list:
                raise ValueError(f"Cannot call {func.__name__} before calling fetch method")
            return func(self, *args, **kwargs)

        return wrapper

    def get_data(self):
        self.response_list = etl.fromdicts(self.client.fetch_data())

    @_check_response_list
    def date_transform(self):
        """Creates a date field by capturing date from 'edited' field and removed the 'edited' column"""

        self.response_list = etl.capture(self.response_list, 'edited', "(\d{1,4}-\d{1,2}-\d{1,2})", ['date'])

    @_check_response_list
    def drop_rows(self):
        """Removes unwanted rows from the table"""

        swapi_columns = settings.SWAPI_DF_COLUMNS
        self.response_list = etl.cut(self.response_list, swapi_columns)

    @_check_response_list
    def transform_homeworld_field(self):
        """
        Handles the logic of homeworld field transformation through a csv file creating it if it doesn't exists containing mappings
        so that whenever a name is not there it sends a request and updates the csv with the api link and name, if it is there it just reads it and does the
        transformation
        """

        homeworld_field = set(etl.values(self.response_list, 'homeworld'))
        homeworld_csv_mapping_path = f"{settings.MAPPINGS_DIR}/homeworld_mapping.csv"
        homeworld_mappings_dict = csv_to_dict(homeworld_csv_mapping_path)

        with open(homeworld_csv_mapping_path, 'a') as csv_mapping:
            for value in homeworld_field:
                try:
                    homeworld_name = homeworld_mappings_dict[value]
                    # TODO Improvement: these could be parametrized
                    self.response_list = etl.convert(self.response_list, 'homeworld', 'replace', value, homeworld_name)
                except KeyError:
                    name = requests.get(value).json()['name']
                    self.response_list = etl.convert(self.response_list, 'homeworld', 'replace', value, name)
                    homeworld_mappings_dict[value] = name
                    csv_mapping.write(f"{value},{name}" + '\n')


    @_check_response_list
    def create_and_save_file(self):
        """Saves the csv file to datasets/ directory and creates instance in the database with the metadata"""

        filename = generate_filename()
        current_date = get_current_date()
        file_location = f"{settings.FILE_LOCATION}/{filename}"
        etl.tocsv(self.response_list, file_location)
        SwapiMetaData.objects.create(filename=filename, csv_location=file_location, date=current_date)

    @_check_response_list
    def table_to_html(self):

        return etl.tohtml(self.response_list)
