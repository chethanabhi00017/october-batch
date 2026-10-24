# user_name=input("enter your name : ")
# user_password=input("enter your password : ")
# inbuilt_user_name="admin"
# inbuilt_user_password="admin123"

# if user_name==inbuilt_user_name and user_password==inbuilt_user_password:
#     print("login successfull!")
# else:
#     print("invalid username or password")#pgm1


from flask import Flask, request, render_template_string

app = Flask(__name__)

# Original Python login credentials
inbuilt_user_name = "admin"
inbuilt_user_password = "admin123"

# HTML + CSS + Flask in one file
page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Login</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            font-family: Arial, sans-serif;
            background: #050713;
            color: white;
        }

        /* Animated background from your reference */
        .background {
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(
                    120deg,
                    rgba(2, 4, 18, 0.70),
                    rgba(4, 8, 25, 0.45)
                ),
                url("https://cdn.dribbble.com/userupload/25118139/file/original-df88ebfba6ec6256604d5173bcdafe5b.gif");
            background-size: cover;
            background-position: center;
            transform: scale(1.04);
            animation: backgroundZoom 18s ease-in-out infinite alternate;
            z-index: -2;
        }

        .background::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(
                circle at center,
                transparent 5%,
                rgba(0, 0, 0, 0.55) 100%
            );
        }

        .login-card {
            width: min(400px, 90%);
            padding: 42px 35px;
            position: relative;
            border-radius: 22px;
            text-align: center;
            background: rgba(8, 13, 32, 0.70);
            border: 1px solid rgba(0, 229, 255, 0.65);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            box-shadow:
                0 0 25px rgba(0, 229, 255, 0.18),
                0 0 70px rgba(0, 100, 255, 0.13);
            animation: cardEnter 1s ease-out;
        }

        .logo {
            width: 66px;
            height: 66px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            border-radius: 50%;
            border: 1px solid #00e5ff;
            color: #00e5ff;
            font-size: 30px;
            box-shadow: 0 0 22px rgba(0, 229, 255, 0.35);
            animation: pulse 2.5s infinite;
        }

        h1 {
            font-size: 30px;
            letter-spacing: 4px;
            color: #ffffff;
            text-shadow: 0 0 15px rgba(0, 229, 255, 0.65);
        }

        .subtitle {
            margin-top: 12px;
            margin-bottom: 30px;
            color: #aab9d0;
            font-size: 11px;
            letter-spacing: 3px;
        }

        .field {
            text-align: left;
            margin-bottom: 19px;
        }

        label {
            display: block;
            margin-bottom: 9px;
            color: #b8c9e3;
            font-size: 12px;
            letter-spacing: 1.5px;
        }

        input {
            width: 100%;
            padding: 15px;
            color: white;
            font-size: 14px;
            background: rgba(255, 255, 255, 0.055);
            border: 1px solid rgba(150, 180, 220, 0.28);
            border-radius: 9px;
            outline: none;
            transition: 0.3s;
        }

        input::placeholder {
            color: #7e8ba5;
        }

        input:focus {
            border-color: #00e5ff;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.18);
            background: rgba(0, 229, 255, 0.045);
        }

        button {
            width: 100%;
            margin-top: 8px;
            padding: 15px;
            border: none;
            border-radius: 9px;
            color: #03101c;
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 3px;
            cursor: pointer;
            background: linear-gradient(100deg, #00e5ff, #3c8dff);
            box-shadow: 0 0 22px rgba(0, 190, 255, 0.20);
            transition: 0.3s;
        }

        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 30px rgba(0, 229, 255, 0.55);
        }

        button:active {
            transform: scale(0.98);
        }

        .message {
            margin-top: 22px;
            font-size: 14px;
            line-height: 1.5;
            overflow-wrap: anywhere;
        }

        .success {
            color: #48ffc0;
            text-shadow: 0 0 12px rgba(72, 255, 192, 0.35);
        }

        .error {
            color: #ff6b88;
            text-shadow: 0 0 12px rgba(255, 70, 120, 0.3);
        }

        .footer {
            margin-top: 28px;
            color: #8290a8;
            font-size: 10px;
            letter-spacing: 2px;
        }

        .status-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            margin-right: 7px;
            background: #43ffb0;
            border-radius: 50%;
            box-shadow: 0 0 9px #43ffb0;
        }

        @keyframes cardEnter {
            from {
                opacity: 0;
                transform: translateY(35px) scale(0.96);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        @keyframes pulse {
            0%, 100% {
                box-shadow: 0 0 15px rgba(0, 229, 255, 0.25);
            }
            50% {
                box-shadow: 0 0 30px rgba(0, 229, 255, 0.65);
            }
        }

        @keyframes backgroundZoom {
            from {
                transform: scale(1.04);
            }
            to {
                transform: scale(1.13);
            }
        }

        @media (max-width: 480px) {
            .login-card {
                padding: 32px 24px;
            }

            h1 {
                font-size: 25px;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation: none !important;
                transition: none !important;
            }
        }
    </style>
</head>

<body>
    <div class="background"></div>

    <main class="login-card">
        <div class="logo">&#9678;</div>

        <h1>WELCOME</h1>
        <p class="subtitle">IDENTITY VERIFICATION SYSTEM</p>

        <form method="POST" autocomplete="off">
            <div class="field">
                <label for="username">USERNAME</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    placeholder="Enter your username"
                    required
                >
            </div>

            <div class="field">
                <label for="password">PASSWORD</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Enter your password"
                    required
                >
            </div>

            <button type="submit">ACCESS SYSTEM</button>
        </form>

        {% if message %}
            <p class="message {{ status }}" role="status">
                {{ message }}
            </p>
        {% endif %}

        <div class="footer">
            <span class="status-dot"></span>
            SYSTEM ONLINE &nbsp; | &nbsp; SECURE ACCESS
        </div>
    </main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if request.method == "POST":
        user_name = request.form.get("username", "")
        user_password = request.form.get("password", "")

        # Your original if/else logic
        if (user_name == inbuilt_user_name
                and user_password == inbuilt_user_password):
            message = "LOGIN SUCCESSFUL! Welcome, admin."
            status = "success"
        else:
            message = "INVALID USERNAME OR PASSWORD"
            status = "error"

    return render_template_string(
        page,
        message=message,
        status=status
    )


if __name__ == "__main__":
    app.run(debug=True)
