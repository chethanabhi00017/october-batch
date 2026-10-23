
from flask import Flask, request, render_template_string

app = Flask(__name__)
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>FitZone Gym</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial;
    background: #10151d;
    color: white;
}
header {
    text-align: center;
    padding: 30px;
    background: linear-gradient(120deg, #166534, #22c55e);
}
header h1 { margin: 0; font-size: 34px; }
.container {
    max-width: 650px;
    margin: 30px auto;
    padding: 20px;
}
.card {
    background: #1c2532;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
}
input, select, button {
    width: 100%;
    padding: 13px;
    margin: 8px 0;
    border-radius: 8px;
    border: none;
}
button {
    background: #22c55e;
    color: #07130a;
    font-weight: bold;
    cursor: pointer;
}
.result {
    padding: 15px;
    background: #163c2a;
    border-radius: 8px;
    overflow-wrap: anywhere;
}
</style>
</head>
<body>
<header>
    <h1>FITZONE GYM</h1>
    <p>Your Fitness Journey Starts Here</p>
</header>

<div class="container">
    <div class="card">
        <h2>Member Fitness Profile</h2>
        <form method="POST">
            <input name="name" placeholder="Member name" required>
            <input name="age" type="number" placeholder="Age"
                   min="1" max="120" required>
            <input name="weight" type="number" step="0.1"
                   placeholder="Weight in kg" min="1" required>
            <input name="height" type="number" step="0.1"
                   placeholder="Height in cm" min="30" required>

            <select name="goal">
                <option value="Muscle gain">Muscle gain</option>
                <option value="Fat loss">Fat loss</option>
                <option value="General fitness">General fitness</option>
            </select>
            <button type="submit">Generate Fitness Report</button>
        </form>
    </div>

    {% if result %}
    <div class="card">
        <h2>Fitness Report</h2>
        <div class="result">
            <p><b>Member:</b> {{ result.name }}</p>
            <p><b>Age:</b> {{ result.age }}</p>
            <p><b>BMI:</b> {{ result.bmi }}</p>
            <p><b>Goal:</b> {{ result.goal }}</p>
            <p><b>Suggested activity:</b> {{ result.workout }}</p>
            <p><b>Guidance:</b> {{ result.guidance }}</p>
        </div>
    </div>
    {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        try:
            name = request.form["name"].strip()
            age = int(request.form["age"])
            weight = float(request.form["weight"])
            height = float(request.form["height"])
            goal = request.form["goal"]

            if (not name or not 1 <= age <= 120
                    or not 1 <= weight <= 500
                    or not 30 <= height <= 260):
                raise ValueError("Enter valid profile details.")

            bmi = weight / ((height / 100) ** 2)

            if goal == "Muscle gain":
                workout = "Progressive strength training"
            elif goal == "Fat loss":
                workout = "Walking plus suitable strength training"
            else:
                workout = "Balanced cardio and strength training"

            if bmi < 18.5:
                guidance = "BMI is in the underweight range."
            elif bmi < 25:
                guidance = "BMI is in the usual healthy adult range."
            elif bmi < 30:
                guidance = "BMI is in the overweight range."
            else:
                guidance = "BMI is in the obesity range."

            result = {
                "name": name,
                "age": age,
                "bmi": round(bmi, 1),
                "goal": goal,
                "workout": workout,
                "guidance": guidance
            }

        except (ValueError, TypeError):
            return "Please enter valid age, weight and height.", 400

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(debug=False, port=8000)
