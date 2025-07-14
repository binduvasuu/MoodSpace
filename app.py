from flask import Flask, render_template, request, redirect, session, url_for
import json, os 
from datetime import datetime
import uuid 

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

# Save users
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

@app.route('/')
def home():
    if 'username' in session:
        users = load_users()
        moods = users[session['username']].get('moods', [])
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return render_template('index.html', username=session['username'], moods=moods, now=now)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect('/')
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists!"
        users[username] = {'password': password, 'moods': []}
        save_users(users)
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/save_mood', methods=['POST'])
def save_mood():
    if 'username' not in session:
        return redirect('/login')

    mood = request.form['mood']
    note = request.form['note']
    date = request.form['date']

    suggestion = ""
    if mood == "😢":
        suggestion = "It's okay to feel down sometimes. Try listening to your favorite song or talking to a friend 💬"
    elif mood == "😡":
        suggestion = "Take a deep breath. Maybe try a short walk or write down what made you upset. 🧘‍♀️"
    elif mood == "😐":
        suggestion = "Maybe a small distraction would help. Try drawing, journaling, or a funny video! 🎨📒"
    elif mood == "😴":
        suggestion = "You might just need some rest. Take a nap or stretch for 5 minutes 😴💤"
    elif mood == "😊":
        suggestion = "Yay! Keep smiling and spread those good vibes today! ☀️"
    elif mood == "❤️":
        suggestion = "Love is beautiful. Maybe tell someone how much they mean to you 💌"

    users = load_users()
    user_data = users.get(session['username'], {})
    new_entry = {
        'id': str(uuid.uuid4()),
        'mood': mood,
        'note': note,
        'date': date,
        'suggestion': suggestion
    }
    user_data.setdefault('moods', []).append(new_entry)
    users[session['username']] = user_data
    save_users(users)

    return redirect('/')
    
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
