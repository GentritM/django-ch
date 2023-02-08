from django.shortcuts import render, redirect

from .service import SwapiClient, TransformSwapiData

from .service.utils import get_metadata


def index(request):
    return render(request, 'index.html', context={"data": get_metadata()})


def fetch(request):
    #TODO Improve: this could be gathered in another method and be run properly
    client = SwapiClient()
    transform = TransformSwapiData(client)
    transform.get_data()
    transform.date_transform()
    transform.drop_rows()
    transform.transform_homeworld_field()
    transform.create_and_save_file()
    return redirect("index")


def details(request, pk):
    # THe logic to display data filters and everything, unfortunately I did not have time to engineer that,
    # I had to take a day off to do this challenge after recent events that took place

    return render(request, "details.html")
