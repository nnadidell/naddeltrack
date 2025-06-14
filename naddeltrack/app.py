from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple in-memory order storage
orders = {
    "NDL123456": {
        "status": "In Transit",
        "location": "Istanbul Hub",
        "delivery": "2025-06-17"
    }
}

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Tracking form page
@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        tracking_id = request.form['tracking_id']
        order = orders.get(tracking_id)
        return render_template('result.html', tracking_id=tracking_id, order=order)
    return render_template('track.html')

# Admin login and update
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        tracking_id = request.form['tracking_id']
        status = request.form['status']
        location = request.form['location']
        delivery = request.form['delivery']
        
        orders[tracking_id] = {
            "status": status,
            "location": location,
            "delivery": delivery
        }
        return redirect(url_for('admin'))
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    app.run()
