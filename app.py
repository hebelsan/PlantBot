from flask import Flask, render_template, request, url_for,  redirect
from gpio import startPumping, stopPumping

app = Flask(__name__)

app.config['PUMP_RELAY_PIN'] = 23
app.config['IS_PUMPING'] = False


@app.route('/')
def index():
    return render_template('index.html', isPumping=app.config['IS_PUMPING'])

@app.route('/settings', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        if request.form['relay_pin']:
            pin = int(request.form['relay_pin'])
            if pin != 0:
                app.config['PUMP_RELAY_PIN'] = pin
        if request.form.get('pumping'):
            setPumping(True)
            app.config['IS_PUMPING'] = True
        else:
            setPumping(False)
            app.config['IS_PUMPING'] = False
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/switchPumping')
def your_flask_route():
    setPumping(not app.config['IS_PUMPING'])
    return 'Sucesss', 200

def setPumping(value):
    app.config['IS_PUMPING'] = value
    if app.config['IS_PUMPING'] == False:
        stopPumping(app.config['PUMP_RELAY_PIN'])
    else:
        startPumping(app.config['PUMP_RELAY_PIN'])
