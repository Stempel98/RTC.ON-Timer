from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'dhjhkdsa*hDAU_S&!hds'  # Change this to your own secret key

# Variables to store the remaining time, start time, and paused state
end_time = None
set_time = None
paused = True  # Initially, the timer is paused

# Password for time management
ADMIN_PASSWORD = "RTC.on!!2024"

# Route to display the remaining time
@app.route('/time')
def time_display():
    global end_time, set_time, paused
    if end_time and not paused:
        time_remaining = max(0, (end_time - datetime.now()).total_seconds())
    elif set_time and paused:
        time_remaining = set_time
    else:
        time_remaining = 0
    return render_template('time.html', time_remaining=int(time_remaining), paused=paused)

# Route for managing the time (with login)
@app.route('/manage', methods=['GET', 'POST'])
def manage():
    global end_time, set_time, paused

    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form.get('action')
        time_input = request.form.get('time')

        if action == 'Set':
            try:
                seconds = int(time_input)
                set_time = seconds
                end_time = None  # Reset end_time to prevent automatic start
                paused = True    # Keep the timer paused until "Start" is clicked
            except ValueError:
                return 'Invalid time value.'
        elif action == 'Start':
            if set_time:
                end_time = datetime.now() + timedelta(seconds=set_time)
                paused = False   # Unpause the timer
        elif action == 'Reset':
            end_time = None
            set_time = None
            paused = True  # Pause after reset

    return render_template('manage.html', set_time=set_time)

# Route for getting the current status of the timer
@app.route('/status')
def status():
    global end_time, set_time, paused
    if end_time and not paused:
        time_remaining = max(0, (end_time - datetime.now()).total_seconds())
    elif set_time and paused:
        time_remaining = set_time
    else:
        time_remaining = 0
    return jsonify({'time_remaining': int(time_remaining), 'paused': paused})

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('manage'))
        else:
            return 'Incorrect password.'

    return '''
        <form method="POST">
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
    '''

# Route for logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
