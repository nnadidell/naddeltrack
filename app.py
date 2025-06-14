from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'  # change this to something strong

ADMIN_PASSWORD = 'naddel123'  # change this too

def load_data():
    with open('data.json') as f:
        return json.load(f)

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/track', methods=['GET', 'POST'])
def track():
    result = None
    not_found = False
    if request.method == 'POST':
        tracking_id = request.form['tracking_id'].strip().upper()
        data = load_data()
        for item in data:
            if item['id'] == tracking_id:
                result = item
                break
        else:
            not_found = True
    return render_template('track.html', result=result, not_found=not_found)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_entry = {
            "id": request.form['id'].strip().upper(),
            "location": request.form['location'],
            "status": request.form['status'],
            "eta": request.form['eta']
        }
        data = load_data()

        for i, item in enumerate(data):
            if item['id'] == new_entry['id']:
                data[i] = new_entry  # update existing
                break
        else:
            data.append(new_entry)  # or add new

        save_data(data)
        return redirect(url_for('admin'))

    data = load_data()
    return render_template('admin.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('track'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
