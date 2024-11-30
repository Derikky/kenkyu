from django.urls import path
#from .views import get_solar_data
from . import views

urlpatterns = [
    #path('solar-data/', get_solar_data, name='solar_data'),
    path('', views.get_solar_data, name='get_solar_data'),
    # 他のURLパターンをここに追加
] 
