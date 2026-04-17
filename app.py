from flask import Flask, request, jsonify
import random
import string
import time

app = Flask(__name__)

guess_games = {}
quiz_sessions = {}
hangman_games = {}

HANGMAN_WORDS = ["python", "java", "kotlin", "javascript", "ruby", "swift"]

OPERATORS = ["+", "-", "*"]
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEMS = 10


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mind Arcade</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                margin: 0;
                padding: 24px;
            }
            .container {
                max-width: 950px;
                margin: auto;
                background: white;
                padding: 28px;
                border-radius: 16px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            }
            h1, h2 {
                margin-top: 0;
            }
            .game-box {
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 20px;
                margin-top: 20px;
            }
            input, button, select {
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                margin-bottom: 10px;
                font-size: 16px;
                border-radius: 8px;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            button {
                background: black;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                opacity: 0.92;
            }
            .output {
                margin-top: 15px;
                white-space: pre-line;
                font-size: 17px;
            }
            .hidden {
                display: none;
            }
            .menu-btn {
                margin-bottom: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 Welcome to the Mind Arcade! 🎮</h1>
            <p>Choose a game below.</p>

            <button class="menu-btn" onclick="showGame('guess')">1. 🔢 Guess the Number Game</button>
            <button class="menu-btn" onclick="showGame('password')">2. 🔐 Random Password Generator</button>
            <button class="menu-btn" onclick="showGame('rps')">3. ✊🖐✌ Rock, Paper, Scissors</button>
            <button class="menu-btn" onclick="showGame('math')">4. ⏳ Timed Math Quiz</button>
            <button class="menu-btn" onclick="showGame('hangman')">5. 🔤 Hangman Game</button>

            <div id="guess" class="game-box hidden">
                <h2>🔢 Guess the Number</h2>
                <button onclick="startGuessGame()">Start New Game</button>
                <input type="number" id="guessInput" placeholder="Enter your guess">
                <button onclick="submitGuess()">Submit Guess</button>
                <div class="output" id="guessOutput"></div>
            </div>

            <div id="password" class="game-box hidden">
                <h2>🔐 Random Password Generator</h2>
                <input type="number" id="passwordLength" value="12" min="4" max="50" placeholder="Password length">
                <button onclick="generatePassword()">Generate Password</button>
                <div class="output" id="passwordOutput"></div>
            </div>

            <div id="rps" class="game-box hidden">
                <h2>✊🖐✌ Rock, Paper, Scissors</h2>
                <select id="rpsChoice">
                    <option value="r">Rock</option>
                    <option value="p">Paper</option>
                    <option value="s">Scissors</option>
                </select>
                <button onclick="playRPS()">Play</button>
                <div class="output" id="rpsOutput"></div>
            </div>

            <div id="math" class="game-box hidden">
                <h2>⏳ Timed Math Quiz</h2>
                <button onclick="startMathQuiz()">Start Quiz</button>
                <div id="mathArea" class="hidden">
                    <div class="output" id="mathQuestion"></div>
                    <input type="number" id="mathAnswer" placeholder="Your answer">
                    <button onclick="submitMathAnswer()">Submit Answer</button>
                </div>
                <div class="output" id="mathOutput"></div>
            </div>

            <div id="hangman" class="game-box hidden">
                <h2>🔤 Hangman Game</h2>
                <button onclick="startHangman()">Start New Hangman</button>
                <input type="text" id="hangmanGuess" maxlength="1" placeholder="Guess a letter">
                <button onclick="submitHangmanGuess()">Submit Letter</button>
                <div class="output" id="hangmanOutput"></div>
            </div>
        </div>

        <script>
            let guessGameId = null;
            let mathSessionId = null;
            let hangmanGameId = null;

            function showGame(gameId) {
                const games = document.querySelectorAll('.game-box');
                games.forEach(game => game.classList.add('hidden'));
                document.getElementById(gameId).classList.remove('hidden');
            }

            async function startGuessGame() {
                const res = await fetch('/start-guess', { method: 'POST' });
                const data = await res.json();
                guessGameId = data.game_id;
                document.getElementById('guessOutput').innerText = 'Game started. Guess a number between 1 and 100.';
            }

            async function submitGuess() {
                const guess = parseInt(document.getElementById('guessInput').value);
                const res = await fetch('/guess', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ game_id: guessGameId, guess: guess })
                });
                const data = await res.json();
                document.getElementById('guessOutput').innerText = data.message || data.error;
            }

            async function generatePassword() {
                const length = parseInt(document.getElementById('passwordLength').value);
                const res = await fetch('/password', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ length: length })
                });
                const data = await res.json();
                document.getElementById('passwordOutput').innerText = data.password ? ('Your random password is: ' + data.password) : data.error;
            }

            async function playRPS() {
                const choice = document.getElementById('rpsChoice').value;
                const res = await fetch('/rps', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user: choice })
                });
                const data = await res.json();
                document.getElementById('rpsOutput').innerText =
                    'You chose: ' + data.user_choice + '\\n' +
                    'Computer chose: ' + data.computer_choice + '\\n' +
                    data.result;
            }

            async function startMathQuiz() {
                const res = await fetch('/math/start', { method: 'POST' });
                const data = await res.json();
                mathSessionId = data.session_id;
                document.getElementById('mathArea').classList.remove('hidden');
                document.getElementById('mathQuestion').innerText = 'Problem #1: ' + data.question;
                document.getElementById('mathOutput').innerText = '';
                document.getElementById('mathAnswer').value = '';
            }

            async function submitMathAnswer() {
                const answer = document.getElementById('mathAnswer').value;
                const res = await fetch('/math/answer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: mathSessionId, answer: answer })
                });
                const data = await res.json();

                if (data.finished) {
                    document.getElementById('mathQuestion').innerText = '';
                    document.getElementById('mathOutput').innerText =
                        'Quiz complete!\\n' +
                        'Wrong attempts: ' + data.wrong + '\\n' +
                        'Time taken: ' + data.total_time + ' seconds';
                    document.getElementById('mathArea').classList.add('hidden');
                } else {
                    document.getElementById('mathQuestion').innerText = 'Problem #' + data.problem_number + ': ' + data.question;
                    document.getElementById('mathOutput').innerText = data.message || data.error;
                    document.getElementById('mathAnswer').value = '';
                }
            }

            async function startHangman() {
                const res = await fetch('/hangman/start', { method: 'POST' });
                const data = await res.json();
                hangmanGameId = data.game_id;
                updateHangmanDisplay(data);
            }

            async function submitHangmanGuess() {
                const guess = document.getElementById('hangmanGuess').value.toLowerCase();
                const res = await fetch('/hangman/guess', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ game_id: hangmanGameId, guess: guess })
                });
                const data = await res.json();
                updateHangmanDisplay(data);
                document.getElementById('hangmanGuess').value = '';
            }

            function updateHangmanDisplay(data) {
                let text =
                    'Word: ' + data.word_display.join(' ') + '\\n' +
                    'Attempts left: ' + data.attempts + '\\n';

                if (data.message) {
                    text += data.message + '\\n';
                }

                if (data.finished) {
                    if (data.won) {
                        text += 'You guessed the word! You survived!';
                    } else {
                        text += 'You lost! The word was: ' + data.word;
                    }
                }

                document.getElementById('hangmanOutput').innerText = text;
            }
        </script>
    </body>
    </html>
    """


# Guess the Number
@app.route("/start-guess", methods=["POST"])
def start_guess():
    game_id = str(time.time()) + str(random.randint(1000, 9999))
    guess_games[game_id] = random.randint(1, 100)
    return jsonify({"game_id": game_id})


@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    game_id = data.get("game_id")
    guess_value = data.get("guess")

    if game_id not in guess_games:
        return jsonify({"message": "Start a new game first."}), 400

    try:
        guess_value = int(guess_value)
    except (TypeError, ValueError):
        return jsonify({"message": "Please enter a valid number."}), 400

    target = guess_games[game_id]

    if guess_value == target:
        del guess_games[game_id]
        return jsonify({"message": "Success: Correct Guess!!"})
    elif guess_value < target:
        return jsonify({"message": "The number was too small. Take a bigger guess...."})
    else:
        return jsonify({"message": "The number was too big. Take a smaller guess...."})


# Password Generator
@app.route("/password", methods=["POST"])
def password():
    data = request.get_json()
    length = data.get("length", 12)

    try:
        length = int(length)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid password length."}), 400

    if length < 4 or length > 50:
        return jsonify({"error": "Password length must be between 4 and 50."}), 400

    character_values = string.punctuation + string.digits + string.ascii_letters
    password_value = "".join(random.choice(character_values) for _ in range(length))

    return jsonify({"password": password_value})


# Rock Paper Scissors
def is_win(player, opponent):
    return (
        (player == "r" and opponent == "s") or
        (player == "s" and opponent == "p") or
        (player == "p" and opponent == "r")
    )


@app.route("/rps", methods=["POST"])
def rps():
    data = request.get_json()
    user = data.get("user")

    if user not in ["r", "p", "s"]:
        return jsonify({"error": "Invalid choice."}), 400

    computer = random.choice(["r", "p", "s"])
    names = {"r": "Rock", "p": "Paper", "s": "Scissors"}

    if user == computer:
        result = "It's a tie"
    elif is_win(user, computer):
        result = "You won!"
    else:
        result = "You lost!"

    return jsonify({
        "user_choice": names[user],
        "computer_choice": names[computer],
        "result": result
    })


# Timed Math Quiz
def generate_problem():
    left = random.randint(MIN_OPERAND, MAX_OPERAND)
    right = random.randint(MIN_OPERAND, MAX_OPERAND)
    operator = random.choice(OPERATORS)
    expr = f"{left} {operator} {right}"
    answer = eval(expr)
    return expr, answer


@app.route("/math/start", methods=["POST"])
def start_math():
    session_id = str(time.time()) + str(random.randint(1000, 9999))
    expr, answer = generate_problem()
    quiz_sessions[session_id] = {
        "start_time": time.time(),
        "wrong": 0,
        "current_problem": 1,
        "question": expr,
        "answer": answer
    }
    return jsonify({
        "session_id": session_id,
        "question": expr
    })


@app.route("/math/answer", methods=["POST"])
def math_answer():
    data = request.get_json()
    session_id = data.get("session_id")
    user_answer = data.get("answer")

    if session_id not in quiz_sessions:
        return jsonify({"error": "Invalid or expired session."}), 400

    session = quiz_sessions[session_id]

    try:
        user_answer = int(user_answer)
    except (TypeError, ValueError):
        return jsonify({"error": "Please enter a valid number."}), 400

    if user_answer == session["answer"]:
        if session["current_problem"] == TOTAL_PROBLEMS:
            total_time = round(time.time() - session["start_time"], 2)
            wrong = session["wrong"]
            del quiz_sessions[session_id]
            return jsonify({
                "finished": True,
                "wrong": wrong,
                "total_time": total_time
            })
        else:
            session["current_problem"] += 1
            expr, answer = generate_problem()
            session["question"] = expr
            session["answer"] = answer
            return jsonify({
                "finished": False,
                "problem_number": session["current_problem"],
                "question": expr,
                "message": "Correct!"
            })
    else:
        session["wrong"] += 1
        return jsonify({
            "finished": False,
            "problem_number": session["current_problem"],
            "question": session["question"],
            "message": "Wrong answer. Try again."
        })


# Hangman
@app.route("/hangman/start", methods=["POST"])
def start_hangman():
    game_id = str(time.time()) + str(random.randint(1000, 9999))
    chosen_word = random.choice(HANGMAN_WORDS)
    hangman_games[game_id] = {
        "word": chosen_word,
        "word_display": ["_" for _ in chosen_word],
        "attempts": 8,
        "guessed_letters": []
    }
    game = hangman_games[game_id]
    return jsonify({
        "game_id": game_id,
        "word_display": game["word_display"],
        "attempts": game["attempts"],
        "finished": False
    })


@app.route("/hangman/guess", methods=["POST"])
def hangman_guess():
    data = request.get_json()
    game_id = data.get("game_id")
    guess = data.get("guess", "").lower()

    if game_id not in hangman_games:
        return jsonify({"error": "Start a new hangman game first."}), 400

    game = hangman_games[game_id]

    if len(guess) != 1 or not guess.isalpha():
        return jsonify({
            "word_display": game["word_display"],
            "attempts": game["attempts"],
            "message": "Enter a single valid letter.",
            "finished": False
        })

    if guess in game["guessed_letters"]:
        return jsonify({
            "word_display": game["word_display"],
            "attempts": game["attempts"],
            "message": "You already guessed that letter.",
            "finished": False
        })

    game["guessed_letters"].append(guess)

    if guess in game["word"]:
        for index, letter in enumerate(game["word"]):
            if letter == guess:
                game["word_display"][index] = guess

        if "_" not in game["word_display"]:
            word = game["word"]
            finished_game = hangman_games.pop(game_id)
            return jsonify({
                "word_display": finished_game["word_display"],
                "attempts": finished_game["attempts"],
                "message": "Nice guess!",
                "finished": True,
                "won": True,
                "word": word
            })

        return jsonify({
            "word_display": game["word_display"],
            "attempts": game["attempts"],
            "message": "Nice guess!",
            "finished": False
        })
    else:
        game["attempts"] -= 1

        if game["attempts"] <= 0:
            word = game["word"]
            final_display = game["word_display"][:]
            del hangman_games[game_id]
            return jsonify({
                "word_display": final_display,
                "attempts": 0,
                "message": "That letter doesn't appear in the word.",
                "finished": True,
                "won": False,
                "word": word
            })

        return jsonify({
            "word_display": game["word_display"],
            "attempts": game["attempts"],
            "message": "That letter doesn't appear in the word.",
            "finished": False
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)