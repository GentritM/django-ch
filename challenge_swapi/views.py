from django.shortcuts import render, redirect

from .service import SwapiClient, TransformSwapiData

from .service.utils import get_metadata, get_filedata, table_to_list, join_elements_of_lists, count_occurrence
import petl as etl


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


def details(request, pk, columns=None):
    # TODO: All of this could be restructured with a better practice, this gets the job done
    data = None
    column_headers = None
    rows = int(request.GET.get("rows", 10))

    file_info = get_filedata(pk)

    if file_info:
        try:
            table = etl.fromcsv(file_info.csv_location)
            column_headers = list(etl.header(table))
            if columns:
                columns = columns.split('-')
                table = etl.cut(table, columns)
                lcols = table_to_list(table)
                joined_lists = join_elements_of_lists(*lcols)
                # TODO: the count_occurrence func changed logic so it works with same lists for count methods
                occurrences = count_occurrence(joined_lists, joined_lists)
                table = etl.addcolumn(table, 'count', occurrences)

            table = etl.head(table, rows)
            # TODO: This could be handled with tempfile.TemporaryFile
            etl.tohtml(table, "temp_table.html")
            data = open("temp_table.html").read()
        except:
            # TODO: no generic exception is good, specific one without print, logging could be better
            print("Error while fetching data for this file")

    return render(request, "details.html", context={"data": data, "column_headers": column_headers})
