
from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name=""),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('user-logout', views.user_logout, name="user-logout"),

    # LOGIC

    path('dashboard', views.dashboard, name="dashboard"),

    path('create-message', views.create_message, name="create-message"),
    
    path('agent-response/<int:pk>', views.agent_response, name="agent-response"),

    path('singular-user/<int:client_user_id>', views.singular_user, name="singular-user"),

    # IMPORT

    path('import-excel', views.import_excel_view, name="import-excel"),

    

]