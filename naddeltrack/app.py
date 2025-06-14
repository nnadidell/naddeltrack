from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "naddelsecret"

tracking_data = {
    "NAD123456": {
        "status": "In Transit",
        "current_location": "Paris, France",
        "last_update": "2025-06-13 16:00",
        "estimated_delivery": "2025-06-17",
        "history": [
            "Departed Lagos, Nigeria - 2025-06-12",
            "Arrived at Paris Distribution Center - 2025-06-13",
            "Customs Cleared - 2025-06-14"
        ]
    }
}

@app.route('/', methods=['GET', 'POST'])
def track():
    data = None
    error = None
    if request.method == 'POST':
        tracking_id = request.form['tracking_id'].strip().upper()
        data = tracking_data.get(tracking_id)
        if not data:
            error = "Tracking number not found."
    return render_template_string(open('templates/home.html').read(), data=data, error=error)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'track123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid credentials'
    return render_template_string(open('templates/login.html').read(), error=error)

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        tid = request.form['tracking_id'].upper()
        tracking_data[tid] = {
            "status": request.form['status'],
            "current_location": request.form['location'],
            "last_update": request.form['last_update'],
            "estimated_delivery": request.form['eta'],
            "history": request.form['history'].split("\n")
        }
        message = f"Order {tid} updated successfully."
        return render_template_string(open('templates/admin.html').read(), message=message)

    return render_template_string(open('templates/admin.html').read())

if __name__ == '__main__':
    app.run(debug=True)
