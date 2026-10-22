
from flask import Flask, request, render_template_string, session

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

correct_password = "admin123"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cinematic Login</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    font-family: Arial, sans-serif;
    color: white;
    background:
        radial-gradient(ellipse at 15% 20%, #25216b 0%, transparent 45%),
        radial-gradient(ellipse at 85% 80%, #5b164c 0%, transparent 40%),
        linear-gradient(135deg, #03040b, #0b1021 55%, #03040b);
}

/* Cinematic light beams */
body::before,
body::after {
    content: "";
    position: fixed;
    width: 60vw;
    height: 150vh;
    top: -25vh;
    left: -20vw;
    background: linear-gradient(
        90deg, transparent, #6d5df533, transparent
    );
    transform: rotate(30deg);
    filter: blur(35px);
    animation: beam 9s ease-in-out infinite alternate;
    pointer-events: none;
}

body::after {
    left: auto;
    right: -25vw;
    background: linear-gradient(
        90deg, transparent, #00d9ff22, transparent
    );
    animation-delay: -4s;
}

@keyframes beam {
    from { transform: translateX(-5%) rotate(30deg); }
    to { transform: translateX(30%) rotate(30deg); }
}

/* Floating cinematic particles */
.particles {
    position: fixed;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
}

.particles span {
    position: absolute;
    bottom: -20px;
    left: var(--x);
    width: var(--s);
    height: var(--s);
    background: #9eeaff;
    border-radius: 50%;
    box-shadow: 0 0 12px #00cfff;
    opacity: 0;
    animation: float var(--t) linear infinite;
    animation-delay: var(--d);
}

@keyframes float {
    0% {
        transform: translateY(0) translateX(0);
        opacity: 0;
    }
    15% { opacity: .8; }
    85% { opacity: .5; }
    100% {
        transform: translateY(-110vh) translateX(60px);
        opacity: 0;
    }
}

.login-card {
    position: relative;
    z-index: 2;
    width: min(390px, 90vw);
    padding: 42px 34px;
    text-align: center;
    border: 1px solid #ffffff26;
    border-radius: 22px;
    background: linear-gradient(
        145deg, #ffffff12, #ffffff04
    );
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    box-shadow:
        0 0 45px #5645ff18,
        0 25px 80px #000a,
        inset 0 1px #ffffff20;
    animation: appear 1.1s ease both;
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(30px) scale(.96);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.logo {
    width: 76px;
    height: 76px;
    margin: 0 auto 22px;
    display: grid;
    place-items: center;
    font-size: 35px;
    border-radius: 23px;
    border: 1px solid #7e8dff77;
    background: linear-gradient(135deg, #6754ff55, #00d9ff22);
    box-shadow: 0 0 35px #6255ff44;
    animation: glow 3s infinite alternate;
}

@keyframes glow {
    from { box-shadow: 0 0 15px #6255ff22; }
    to { box-shadow: 0 0 35px #6255ff77; }
}

.tag {
    color: #83eaff;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 4px;
    margin-bottom: 13px;
}

h1 {
    font-size: clamp(27px, 6vw, 34px);
    letter-spacing: 1px;
    margin-bottom: 12px;
    text-shadow: 0 0 25px #ffffff22;
}

.subtitle {
    color: #a5aec9;
    font-size: 13px;
    line-height: 1.7;
    margin-bottom: 30px;
}

label {
    display: block;
    text-align: left;
    margin-bottom: 10px;
    font-size: 12px;
    color: #d5ddf5;
    letter-spacing: 1px;
}

input {
    width: 100%;
    padding: 15px;
    border: 1px solid #ffffff25;
    border-radius: 10px;
    outline: none;
    background: #050814a8;
    color: white;
    font-size: 15px;
    transition: .3s;
}

input::placeholder {
    color: #717b99;
}

input:focus {
    border-color: #64dfff;
    box-shadow: 0 0 18px #00cfff20;
}

button {
    width: 100%;
    padding: 15px;
    margin-top: 20px;
    border: none;
    border-radius: 10px;
    color: #050817;
    background: linear-gradient(100deg, #75e8ff, #a9a0ff);
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
    cursor: pointer;
    transition: .3s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 28px #69dcff66;
    filter: brightness(1.1);
}

button:disabled,
input:disabled {
    opacity: .5;
    cursor: not-allowed;
}

.message {
    margin-top: 20px;
    padding: 13px;
    border-radius: 9px;
    font-size: 13px;
    line-height: 1.5;
    animation: appear .4s ease both;
}

.success {
    color: #8dffca;
    background: #00ff9512;
    border: 1px solid #00ff9540;
}

.error {
    color: #ff9eae;
    background: #ff234412;
    border: 1px solid #ff526344;
}

.attempts {
    color: #929db9;
    font-size: 11px;
    margin-top: 20px;
    letter-spacing: 1px;
}

.footer {
    margin-top: 28px;
    color: #626d8b;
    font-size: 9px;
    letter-spacing: 2px;
}

@media (max-width: 480px) {
    .login-card { padding: 35px 24px; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
</head>

<body>

<div class="particles">
    <span style="--x:8%;--s:3px;--t:12s;--d:0s"></span>
    <span style="--x:19%;--s:2px;--t:15s;--d:3s"></span>
    <span style="--x:31%;--s:4px;--t:11s;--d:1s"></span>
    <span style="--x:44%;--s:2px;--t:14s;--d:5s"></span>
    <span style="--x:57%;--s:3px;--t:13s;--d:2s"></span>
    <span style="--x:68%;--s:2px;--t:16s;--d:4s"></span>
    <span style="--x:79%;--s:4px;--t:12s;--d:1s"></span>
    <span style="--x:91%;--s:3px;--t:15s;--d:6s"></span>
</div>

<div class="login-card">
    <div class="logo">🔐</div>

    <div class="tag">SECURE ACCESS</div>

    <h1>Welcome Back</h1>

    <p class="subtitle">
        Enter the system.<br>
        Your next chapter begins here.
    </p>

    <form method="POST">
        <label for="password">PASSWORD</label>

        <input
            id="password"
            type="password"
            name="password"
            placeholder="Enter your password"
            autocomplete="current-password"
            required
            {% if locked or success %}disabled{% endif %}
        >

        <button type="submit"
            {% if locked or success %}disabled{% endif %}>
            {% if success %}
                ACCESS GRANTED
            {% elif locked %}
                ACCESS LOCKED
            {% else %}
                ENTER SYSTEM →
            {% endif %}
        </button>
    </form>

    {% if message %}
        <div class="message {{ status }}">{{ message }}</div>
    {% endif %}

    {% if not locked and not success %}
        <div class="attempts">
            SECURITY ATTEMPTS: {{ attempts }} / 3
        </div>
    {% endif %}

    <div class="footer">
        CINEMATIC INTERFACE · FLASK SECURITY DEMO
    </div>
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
            message = "ACCESS DENIED — ACCOUNT LOCKED"

        elif session["success"]:
            message = "ACCESS GRANTED — WELCOME BACK"
            status = "success"

        else:
            password = request.form.get("password", "")
            session["attempts"] += 1

            if password == correct_password:
                session["success"] = True
                message = "ACCESS GRANTED — WELCOME BACK"
                status = "success"

            elif session["attempts"] >= 3:
                session["locked"] = True
                message = "ACCESS DENIED — ACCOUNT LOCKED"

            else:
                remaining = 3 - session["attempts"]
                message = (
                    f"INCORRECT PASSWORD — "
                    f"{remaining} ATTEMPT(S) REMAINING"
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


