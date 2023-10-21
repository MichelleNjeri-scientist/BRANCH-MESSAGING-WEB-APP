
from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name=""),


    # IMPORT

    path('import-csv', views.import_csv_view, name="import-csv"),

    

]