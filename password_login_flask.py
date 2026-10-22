
from flask import Flask, request, render_template_string, session

app = Flask(__name__)
app.secret_key = "my-secret-key"

correct_password = "admin123"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login System</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #141e30, #35577d);
        }

        .login-box {
            width: 350px;
            padding: 35px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px #0005;
            text-align: center;
        }

        .login-box h1 {
            margin-bottom: 10px;
            color: #23395d;
        }

        .login-box p {
            color: #777;
            font-size: 14px;
        }

        input {
            width: 100%;
            padding: 13px;
            margin-top: 15px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 15px;
        }

        button {
            width: 100%;
            padding: 13px;
            margin-top: 20px;
            background: #315bd6;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #203f9e;
        }

        .message {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
        }

        .success {
            background: #d4edda;
            color: #155724;
        }

        .error {
            background: #f8d7da;
            color: #721c24;
        }

        button:disabled, input:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
    </style>
</head>

<body>
    <div class="login-box">
        <h1>🔐 Welcome Back</h1>
        <p>Enter your password to continue</p>

        <form method="POST">
            <input
                type="password"
                name="password"
                placeholder="Enter password"
                required
                {% if locked or success %}disabled{% endif %}
            >

            <button type="submit"
                {% if locked or success %}disabled{% endif %}>
                Login
            </button>
        </form>

        {% if message %}
            <div class="message {{ status }}">
                {{ message }}
            </div>
        {% endif %}

        {% if not locked and not success %}
            <p>Attempts: {{ attempts }}/3</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    session.setdefault("attempts", 0)
    session.setdefault("locked", False)
    session.setdefault("success", False)

    message = ""
    status = "error"

    if request.method == "POST":
        if session["locked"]:
            message = "Account locked!"
        elif session["success"]:
            message = "Login successful!"
            status = "success"
        else:
            password = request.form.get("password", "")
            session["attempts"] += 1

            if password == correct_password:
                session["success"] = True
                message = "Login successful!"
                status = "success"

            elif session["attempts"] >= 3:
                session["locked"] = True
                message = "Account locked! Too many attempts."

            else:
                remaining = 3 - session["attempts"]
                message = (
                    f"Wrong password! {remaining} attempts left."
                )

    return render_template_string(
        HTML,
        message=message,
        status=status,
        attempts=session["attempts"],
        locked=session["locked"],
        success=session["success"]
    )

if __name__ == "__main__":
    app.run(debug=True)
