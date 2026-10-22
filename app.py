
from flask import Flask, request, jsonify, render_template_string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>My Alexa Assistant</title>
<style>
*{box-sizing:border-box}
body{
    margin:0;min-height:100vh;display:grid;place-items:center;
    padding:20px;font-family:Arial,sans-serif;color:white;
    background:radial-gradient(circle at top,#273b75,#080d1a 70%)
}
.card{
    width:100%;max-width:600px;padding:28px;border-radius:24px;
    background:#131d35;border:1px solid #34466d;text-align:center;
    box-shadow:0 20px 60px #0006
}
h1{font-size:27px}
p{color:#b5c4df}
.orb{
    width:130px;height:130px;border-radius:50%;margin:28px auto;
    display:grid;place-items:center;font-size:52px;
    background:radial-gradient(circle at 30% 25%,#c4fbff,#7581ff 45%,#252365);
    box-shadow:0 0 45px #777cff77
}
button{
    padding:12px 18px;border:0;border-radius:12px;
    color:white;background:#686ff1;cursor:pointer
}
input{
    flex:1;min-width:0;padding:13px;border-radius:12px;
    border:1px solid #39476a;background:#080e1d;color:white
}
form{display:flex;gap:8px;margin-top:16px}
#chat{
    max-height:230px;overflow-y:auto;text-align:left;
    background:#090f20;border-radius:12px;padding:12px;margin-top:25px
}
#chat div{padding:10px;line-height:1.5;overflow-wrap:anywhere}
.user{color:#d1caff;text-align:right}
.bot{color:#a9eaff}
.small{font-size:12px}
</style>
</head>
<body>
<div class="card">
    <h1>✦ My Alexa Assistant</h1>
    <p>Your personal Python voice assistant</p>
    <div class="orb">✦</div>
    <h3 id="status">Hello! How can I help?</h3>
    <button onclick="listen()">🎙 Speak</button>
    <div id="chat">
        <div class="bot">Assistant: Hello! Ask me about the weather or a topic.</div>
    </div>
    <form id="form">
        <input id="message" placeholder="Type your command..." required>
        <button type="submit">Send</button>
    </form>
    <p class="small">Try: weather in Bengaluru · who is Einstein · help</p>
</div>

<script>
const form = document.getElementById("form");
const input = document.getElementById("message");
const chat = document.getElementById("chat");
const statusText = document.getElementById("status");

function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = type;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function askAssistant(text) {
    if (!text.trim()) return;
    addMessage("You: " + text, "user");
    statusText.textContent = "Thinking...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: text})
        });
        const data = await response.json();
        addMessage("Assistant: " + data.reply, "bot");
        statusText.textContent = "Ready to help";

        if ("speechSynthesis" in window) {
            speechSynthesis.cancel();
            speechSynthesis.speak(
                new SpeechSynthesisUtterance(data.reply)
            );
        }
    } catch (error) {
        addMessage("Assistant: Connection error. Try again.", "bot");
        statusText.textContent = "Error";
    }
}

form.addEventListener("submit", function(event) {
    event.preventDefault();
    const text = input.value.trim();
    input.value = "";
    askAssistant(text);
});

function listen() {
    const SR = window.SpeechRecognition ||
               window.webkitSpeechRecognition;

    if (!SR) {
        statusText.textContent =
            "Voice recognition unavailable. Please type instead.";
        return;
    }

    const recognition = new SR();
    recognition.lang = "en-IN";
    recognition.onstart = () => statusText.textContent = "Listening...";
    recognition.onresult = event => {
        const text = event.results[0][0].transcript;
        input.value = text;
        askAssistant(text);
    };
    recognition.onerror = () =>
        statusText.textContent = "Microphone error. Check permissions.";
    recognition.start();
}
</script>
</body>
</html>
"""


def get_json(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "MyPythonAssistant/1.0"}
    )
    with urllib.request.urlopen(req, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def get_weather(city):
    city_url = urllib.parse.quote(city)
    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city_url}&count=1&language=en&format=json"
    )

    places = get_json(url).get("results", [])
    if not places:
        return f"Sorry, I could not find the city {city}."

    place = places[0]
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={place['latitude']}"
        f"&longitude={place['longitude']}"
        "&current=temperature_2m,relative_humidity_2m,"
        "apparent_temperature,wind_speed_10m,weather_code"
    )
    current = get_json(url)["current"]

    conditions = {
        0: "clear sky", 1: "mainly clear", 2: "partly cloudy",
        3: "overcast", 45: "fog", 48: "fog",
        51: "light drizzle", 53: "moderate drizzle",
        55: "heavy drizzle", 61: "slight rain",
        63: "moderate rain", 65: "heavy rain",
        71: "slight snow", 73: "moderate snow",
        75: "heavy snow", 80: "rain showers",
        81: "moderate rain showers", 82: "heavy rain showers",
        95: "thunderstorm", 96: "thunderstorm with hail",
        99: "thunderstorm with heavy hail"
    }

    condition = conditions.get(current.get("weather_code"), "unknown conditions")

    return (
        f"Weather in {place['name']}, {place.get('country', '')}: "
        f"{condition}. Temperature: {current['temperature_2m']}°C. "
        f"Feels like: {current['apparent_temperature']}°C. "
        f"Humidity: {current['relative_humidity_2m']}%. "
        f"Wind: {current['wind_speed_10m']} km/h."
    )


def get_wikipedia(topic):
    title = urllib.parse.quote(topic.replace(" ", "_"), safe="_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    data = get_json(url)
    return data.get("extract", f"No information found about {topic}.")


def assistant(message):
    text = message.strip()
    lower = text.lower()

    if not text:
        return "Please enter a command."

    if lower in ("hi", "hello", "hey", "hello alexa"):
        return "Hello! I am your Python assistant. How can I help?"

    if lower in ("help", "what can you do"):
        return (
            "I can tell you the weather and explain topics. "
            "Try weather in Bengaluru, who is Einstein, "
            "or tell me about Python."
        )

    if lower.startswith("weather in "):
        city = text[len("weather in "):].strip()
        return get_weather(city) if city else "Please provide a city name."

    if lower.startswith("who is "):
        return get_wikipedia(text[len("who is "):].strip())

    if lower.startswith("what is "):
        return get_wikipedia(text[len("what is "):].strip())

    if lower.startswith("tell me about "):
        return get_wikipedia(text[len("tell me about "):].strip())

    return (
        "I don't know that command yet. Try asking about the weather "
        "or say 'tell me about Python'."
    )


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", ""))

    try:
        reply = assistant(message)
    except Exception:
        reply = (
            "Sorry, I could not connect to the free API. "
            "Check your internet connection and try again."
        )

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
