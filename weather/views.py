from .models import FavouriteCity
from django.http import JsonResponse
from .utils import format_api_response
from dotenv import load_dotenv
import requests
load_dotenv()



def home(request):
    city = request.GET.get("city", "indore")
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=a03a1b1193e5bff9dffc0e3297215f56'
    forcast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid=a03a1b1193e5bff9dffc0e3297215f56&cnt=5'
    try:
        weather_response = requests.get(weather_url)
        forcast_response = requests.get(forcast_url)
        weather_data = weather_response.json()
        forcast_data = forcast_response.json()
        print(weather_data, forcast_data)
        weather_details = {
                'id' : int(weather_data['id']),
                'temperature' : int(weather_data['main']['temp']),
                'min_temperature' : int(weather_data['main']['temp_min']),
                'max_temperature' : int(weather_data['main']['temp_max']),
                'city' : weather_data['name'],
                'humidity' : int(weather_data['main']["humidity"]),
                'wind_speed' : int(weather_data["wind"]["speed"]),
                'description': weather_data['weather'][0]['description'],
                'icon' : weather_data['weather'][0]['icon'],
                'five_days_forcast' : forcast_data['list']
            }
        return JsonResponse(weather_details)
    except Exception as e:
         response_data = format_api_response(success=False,message="error occur",error=str(e))
         return JsonResponse(response_data)
    


def add_to_favourite(request):

    cognito_id = request.cognito_id
    print('cognito_user_id->', cognito_id)
    city_name = request.headers.get('City')

    if not cognito_id:
        response_data = format_api_response(success=False, message='email is required')
        return JsonResponse(response_data)
    elif not city_name:
        response_data = format_api_response(success=False, message='city name is required')
        return JsonResponse(response_data)

    
    #count number of city
    
    if FavouriteCity.objects.filter(cognito_user=cognito_id).count() >= 5:
        count_cities = FavouriteCity.objects.filter(cognito_user=cognito_id).count()
        data={'city_count': count_cities}
        response_data = format_api_response(success=False,data=data, message="maximum number of cities reached")
        return JsonResponse(response_data)
    
    #check already exist
    if FavouriteCity.objects.filter(cognito_user=cognito_id, city_name=city_name).exists():
        response_data = format_api_response(success=False, message="city already exists in favorites")
        return JsonResponse(response_data)

    FavouriteCity.objects.create(cognito_user=cognito_id, city_name=city_name)

    response_data = format_api_response(success=True, message="city added successfully")
    return JsonResponse(response_data)



def get_weather(city_name):
    api_url = "https://api.openweathermap.org/data/2.5/weather?"

    params = {
        'q': city_name,
        'appid': 'a03a1b1193e5bff9dffc0e3297215f56',  
        'units': 'metric' 
    }
    response = requests.get(api_url, params=params)

   
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        return temperature
    else:
        return None


def get_favourite_cities_weather(request):
    cognito_id = request.cognito_id
    print('cognito_user_id->', cognito_id)
    if not cognito_id:
        return JsonResponse({'error': 'cognito_id is required'}, status=400)
    try:
        favorite_cities = FavouriteCity.objects.filter(cognito_user=cognito_id)
    except FavouriteCity.DoesNotExist:
        return JsonResponse({'error': 'Favorite cities not found for this user'}, status=404)

   
    city_list = [city.city_name for city in favorite_cities]
    weather_info = {}
    for city_name in city_list:
        temperature = get_weather(city_name)
        if temperature is not None:
            weather_info[city_name] = {'temperature': temperature}

    return JsonResponse({'weather_info': weather_info})


    



  






    





    

    
