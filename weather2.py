
from flask import Flask, request, render_template_string
from urllib.parse import urlencode
from urllib.request import urlopen
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #60a5fa, #a5f3fc);
            color: #172554;
        }

        .container {
            width: 100%;
            max-width: 480px;
            padding: 30px;
            border-radius: 22px;
            background: white;
            box-shadow: 0 12px 35px #1e3a8a30;
        }

        h1 {
            margin-top: 0;
            text-align: center;
            color: #1d4ed8;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 25px;
        }

        form {
            display: flex;
            gap: 10px;
        }

        input {
            width: 100%;
            min-width: 0;
            padding: 13px;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            font-size: 16px;
        }

        button {
            padding: 13px 16px;
            border: none;
            border-radius: 10px;
            background: #2563eb;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #1d4ed8;
        }

        .weather {
            margin-top: 25px;
            padding: 22px;
            border-radius: 16px;
            color: white;
            background: linear-gradient(135deg, #2563eb, #0891b2);
        }

        .city {
            margin: 0;
            font-size: 23px;
        }

        .temperature {
            margin: 15px 0 5px;
            font-size: 55px;
            font-weight: bold;
        }

        .condition {
            margin-bottom: 20px;
            font-size: 17px;
        }

        .details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .detail {
            padding: 12px;
            border-radius: 10px;
            background: #ffffff25;
        }

        .label {
            display: block;
            margin-bottom: 8px;
            font-size: 12px;
            color: #dbeafe;
        }

        .value {
            font-size: 17px;
            font-weight: bold;
        }

        .error {
            margin-top: 20px;
            padding: 12px;
            border-radius: 10px;
            background: #fee2e2;
            color: #b91c1c;
        }

        .footer {
            margin-bottom: 0;
            text-align: center;
            font-size: 12px;
            color: #94a3b8;
        }

        @media (max-width: 400px) {
            .container {
                padding: 20px;
            }

            form {
                flex-direction: column;
            }

            button {
                width: 100%;
            }
        }
    </style>
</head>

<body>
    <main class="container">
        <h1>🌤 Weather App</h1>
        <p class="subtitle">Check the weather of any city</p>

        <form method="POST">
            <input
                type="text"
                name="city"
                placeholder="Enter city name"
                value="{{ city }}"
                required
            >
            <button type="submit">Search</button>
        </form>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if weather %}
            <section class="weather">
                <h2 class="city">{{ weather.city }}</h2>
                <p>{{ weather.time }}</p>

                <div class="temperature">
                    {{ weather.temperature }}°C
                </div>

                <div class="condition">
                    {{ weather.icon }} {{ weather.description }}
                </div>

                <div class="details">
                    <div class="detail">
                        <span class="label">Feels like</span>
                        <span class="value">
                            {{ weather.feels_like }}°C
                        </span>
                    </div>

                    <div class="detail">
                        <span class="label">Humidity</span>
                        <span class="value">
                            {{ weather.humidity }}%
                        </span>
                    </div>

                    <div class="detail">
                        <span class="label">Wind speed</span>
                        <span class="value">
                            {{ weather.wind }} km/h
                        </span>
                    </div>

                    <div class="detail">
                        <span class="label">Today's high / low</span>
                        <span class="value">
                            {{ weather.high }}° / {{ weather.low }}°C
                        </span>
                    </div>
                </div>
            </section>
        {% endif %}

        <p class="footer">
            Weather data by Open-Meteo · Free API
        </p>
    </main>
</body>
</html>
"""


def fetch_json(url, params):
    query = urlencode(params)
    with urlopen(url + "?" + query, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def get_weather_description(code):
    conditions = {
        0: ("Clear sky", "☀️"),
        1: ("Mainly clear", "🌤️"),
        2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Foggy", "🌫️"),
        48: ("Foggy", "🌫️"),
        51: ("Light drizzle", "🌦️"),
        53: ("Drizzle", "🌦️"),
        55: ("Heavy drizzle", "🌧️"),
        61: ("Light rain", "🌦️"),
        63: ("Moderate rain", "🌧️"),
        65: ("Heavy rain", "🌧️"),
        71: ("Light snow", "🌨️"),
        73: ("Snow", "🌨️"),
        75: ("Heavy snow", "❄️"),
        80: ("Rain showers", "🌦️"),
        81: ("Rain showers", "🌧️"),
        82: ("Heavy rain showers", "⛈️"),
        95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with hail", "⛈️"),
        99: ("Heavy thunderstorm", "⛈️")
    }

    return conditions.get(
        code, ("Weather information unavailable", "🌡️")
    )


def get_weather(city):
    # Find the city using the free geocoding API
    location_data = fetch_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
    )

    locations = location_data.get("results", [])

    if not locations:
        return None

    location = locations[0]

    # Get current weather and today's forecast
    forecast = fetch_json(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,weather_code,wind_speed_10m"
            ),
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto",
            "forecast_days": 1
        }
    )

    current = forecast["current"]
    daily = forecast["daily"]

    description, icon = get_weather_description(
        current["weather_code"]
    )

    city_parts = [
        location.get("name"),
        location.get("admin1"),
        location.get("country")
    ]

    city_name = ", ".join(
        dict.fromkeys(part for part in city_parts if part)
    )

    return {
        "city": city_name,
        "time": current.get("time", "").replace("T", " "),
        "temperature": round(current["temperature_2m"]),
        "feels_like": round(current["apparent_temperature"]),
        "humidity": current["relative_humidity_2m"],
        "wind": round(current["wind_speed_10m"]),
        "high": round(daily["temperature_2m_max"][0]),
        "low": round(daily["temperature_2m_min"][0]),
        "description": description,
        "icon": icon
    }


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        try:
            if city:
                weather = get_weather(city)

                if weather is None:
                    error = "City not found. Please check the spelling."
            else:
                error = "Please enter a city name."

        except Exception:
            error = (
                "Unable to get weather. Check your internet "
                "connection and try again."
            )

    return render_template_string(
        HTML,
        city=city,
        weather=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
