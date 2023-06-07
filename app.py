import requests
from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import time
import datetime

app = Flask(__name__)
# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK TEST', 200

@app.route('/dialogflow', methods=['GET', 'POST'])
def dialogflow():
    # Get the data from the request
    data = request.get_json()
    raw_city = data['sessionInfo']['parameters']['city']
    raw_date = data['sessionInfo']['parameters']['date']

    # Get the location data for the city, and transform the date
    date = datetime.date(int(raw_date['year']), int(raw_date['month']), int(raw_date['day']))
    city = raw_city.title()
    LOCATION = geolocator.geocode(city)
    LONGITUDE = str(LOCATION.longitude)
    LATITUDE = str(LOCATION.latitude)

    # Check if the date is historical or not. (NOTE: one is for historical data until 5d ago , one is for forecast including 5d ago)
    threshold_date = datetime.date.today() - datetime.timedelta(days=5) 
    historical = date < threshold_date
    if historical:
        BASE_URL = "https://archive-api.open-meteo.com/v1/archive?"
        URL = BASE_URL + "latitude=" + LATITUDE + "&longitude=" + LONGITUDE + "&start_date=" + str(date) + "&end_date=" + str(date) + "&daily=temperature_2m_max,temperature_2m_min,rain_sum&timezone=Europe%2FBerlin"
        index = 0
    else:
        # get amount of days between today and the date
        days = (date - threshold_date).days
        index = days
        # Request the weather data from the API
        BASE_URL = "https://api.open-meteo.com/v1/forecast?"
        URL = BASE_URL + "latitude=" + LATITUDE + "&longitude=" + LONGITUDE + "&daily=temperature_2m_max,temperature_2m_min,rain_sum&past_days=5&forecast_days=16&timezone=Europe%2FBerlin"

    try:
        response = requests.get(URL).json()
        if index > 15:
            final_response = "Sorry, I can only predict the weather for the next 16 days."
        else:
            max_temp = response["daily"]["temperature_2m_max"][index]
            min_temp = response["daily"]["temperature_2m_min"][index]
            rain_bool = response["daily"]["rain_sum"][index] > 0
            mean_temp = (max_temp + min_temp) / 2
            # Repsonse text
            final_response = "The weather in " + city + " on " + str(date) + " is between " + str(min_temp) + '-' + str(max_temp) + "°C."
            if historical:
                verb = "was"
            else:
                verb = "will be"
            if mean_temp < 10:
                final_response += f" It {verb} cold outside, make sure to wear a jacket!🥶"
            elif mean_temp > 20:
                final_response += f" It {verb} hot outside, make sure to put sun creme on in case you get burned!🥵"
            
            if rain_bool:
                final_response += f" Also, there {verb} a chance of rain that day, make sure to take an umbrella with you!🌧️"
    except:
        final_response = "Sorry, I couldn't find any data for that date."

    return jsonify(
        {
            'fulfillment_response': {
                'messages': [
                    {
                        'text': {
                            'text': [final_response]
                        }
                    }
                ]
            }
        }
    )


if __name__ == '__main__':
    app.run(debug=True)