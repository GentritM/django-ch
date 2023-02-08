import requests
import math

from django.conf import settings

from challenge_swapi.models import SwapiMetaData


class SwapiClient:
    """Swapi Client"""

    url = settings.SWAPI_URL

    #TODO Improvement: This could be asynchronus
    def fetch_data(self) -> list:
        """Fetches data from a Swapi"""

        number_of_pages, response_list = self._get_number_of_pages()

        for page in range(2, number_of_pages + 1):
            response = requests.request(url=self.url, method="GET", params={"page": page}).json()
            response_list.extend(response["results"])

        return response_list

    def _get_number_of_pages(self) -> tuple:
        """
        Checks and returns total number of pagination the Swapi API has
        For optimization purposes it returns number of total pages and the data of the first page
        """

        response = requests.get(self.url)
        assert response.status_code == 200, "Response is not okay"
        total_num_of_results, num_of_results_per_page = response.json()["count"], len(response.json()["results"])
        # For the sake of optimization purposes since 1 request has already been made we transmit this one and when
        # using the method again we start from page 2
        return math.ceil(total_num_of_results / num_of_results_per_page), response.json()["results"]


