# q=input("what is capitalof india?").lower()
# if q=="delhi":
#     print("correct answer")
# else:
#     ("wrong answerd")

# q=input("what is capitalof karnataka?").lower()
# if q=="bengaluru":
#     print("correct answer")
# else:
#     ("wrong answerd")#pgm1


from flask import Flask, request, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Quiz Game</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #090d25, #162d52, #421e55);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 520px;
            background: rgba(255, 255, 255, 0.09);
            padding: 35px;
            border-radius: 22px;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 15px 50px rgba(0,0,0,0.4);
        }

        h1 {
            text-align: center;
            color: #70e1ff;
            margin-top: 0;
        }

        .subtitle {
            text-align: center;
            color: #d4d9ee;
            margin-bottom: 30px;
        }

        .question {
            margin: 22px 0;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }

        input {
            width: 100%;
            padding: 14px;
            border-radius: 10px;
            border: 1px solid #8a9bc5;
            background: #f5f7ff;
            color: #111;
            font-size: 16px;
            outline: none;
        }

        input:focus {
            border: 2px solid #70e1ff;
        }

        button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(90deg, #00c6ff, #7b61ff);
            color: white;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 12px;
        }

        button:hover {
            opacity: 0.85;
            transform: translateY(-2px);
        }

        .result {
            text-align: center;
            margin-top: 22px;
            padding: 15px;
            border-radius: 10px;
            background: rgba(0,0,0,0.25);
            line-height: 1.8;
        }

        .correct {
            color: #6dffad;
        }

        .wrong {
            color: #ff8585;
        }

        .score {
            color: #ffe27a;
            font-size: 20px;
            font-weight: bold;
        }

        .footer {
            text-align: center;
            margin-top: 22px;
            color: #bfc8e8;
            font-size: 12px;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>🧠 Quiz Challenge</h1>
        <p class="subtitle">Test your general knowledge!</p>

        <form method="POST">
            <div class="question">
                <label>1. What is the capital of India?</label>
                <input type="text" name="india"
                       placeholder="Enter your answer"
                       value="{{ india }}" required>
                {% if checked %}
                    <p class="{{ 'correct' if india_ok else 'wrong' }}">
                        {{ '✓ Correct answer!' if india_ok else '✗ Wrong! Answer: Delhi' }}
                    </p>
                {% endif %}
            </div>

            <div class="question">
                <label>2. What is the capital of Karnataka?</label>
                <input type="text" name="karnataka"
                       placeholder="Enter your answer"
                       value="{{ karnataka }}" required>
                {% if checked %}
                    <p class="{{ 'correct' if karnataka_ok else 'wrong' }}">
                        {{ '✓ Correct answer!' if karnataka_ok else '✗ Wrong! Answer: Bengaluru' }}
                    </p>
                {% endif %}
            </div>

            <button type="submit">Submit Answers →</button>
        </form>

        {% if checked %}
            <div class="result">
                <div class="score">Your Score: {{ score }} / 2</div>
                {% if score == 2 %}
                    Excellent! You got all answers correct! 🎉
                {% elif score == 1 %}
                    Good try! Keep learning. 👍
                {% else %}
                    Don't give up! Try again. 💪
                {% endif %}
                <form method="GET">
                    <button type="submit">Play Again ↻</button>
                </form>
            </div>
        {% endif %}

        <div class="footer">POWERED BY PYTHON + FLASK + HTML + CSS</div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def quiz():
    checked = request.method == "POST"

    india = ""
    karnataka = ""
    india_ok = False
    karnataka_ok = False
    score = 0

    if checked:
        india = request.form.get("india", "").strip()
        karnataka = request.form.get("karnataka", "").strip()

        india_ok = india.lower() == "delhi"
        karnataka_ok = karnataka.lower() == "bengaluru"

        score = int(india_ok) + int(karnataka_ok)

    return render_template_string(
        html,
        checked=checked,
        india=india,
        karnataka=karnataka,
        india_ok=india_ok,
        karnataka_ok=karnataka_ok,
        score=score
    )

if __name__ == "__main__":
    app.run(debug=True)
