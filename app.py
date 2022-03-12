from flask import Flask, render_template, request, url_for,  redirect
from gpio import startPumping, stopPumping
from flask_apscheduler import APScheduler

app = Flask(__name__)

# watering configs
app.config['PUMP_RELAY_PIN'] = 23
app.config['IS_PUMPING'] = False
app.config['PUMP_SCHEDULE'] = [{ 'id': 'initID', 'time': '12:00', 'durationSek':10 }]

scheduler = APScheduler()

#
# external routes
#
@app.route('/')
def index():
    return render_template('index.html', isPumping=app.config['IS_PUMPING'])

@app.route('/settings', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        if request.form['relay_pin']:
            pin = int(request.form['relay_pin'])
            app.config['PUMP_RELAY_PIN'] = pin
        return redirect(url_for('index'))
    return render_template('settings.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html', data=app.config['PUMP_SCHEDULE'])

#
# internal routes
#
@app.route('/switchPumping')
def switchPumping():
    setPumping(not app.config['IS_PUMPING'])
    return 'Sucesss', 200

@app.route('/addJob', methods=['POST'])
def addJob():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        matches = [d for d in app.config['PUMP_SCHEDULE'] if d['id'] == json['id']];
        if (len(matches) == 0):
            # TODO add job to scheduler
            app.config['PUMP_SCHEDULE'].append({ 'id':json['id'], 'time':json['time'], 'durationSek':json['duration'] })
        elif (len(matches) == 1):
            matches[0]['time'] = json['time']
            matches[0]['durationSek'] = json['duration']
            # TODO change job at scheduler
        elif (len(matches) > 1):
            return 'Something went wrong', 500
        return 'Sucesss', 200
    return 'Wrong http header', 400

@app.route('/removeJobs', methods=['POST'])
def removeJobs():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        requestID = json['id']
        d_list = [d for d in app.config['PUMP_SCHEDULE'] if d.get('id') != requestID]
        if (len(d_list) == len(app.config['PUMP_SCHEDULE'])-1):
            app.config['PUMP_SCHEDULE'] = d_list
            # TODO remove job from scheduler
            return 'Sucesss', 200
        elif (len(d_list) == len(app.config['PUMP_SCHEDULE'])):
            return 'Id not found', 400
    return 'Wrong http header', 400

def setPumping(value):
    app.config['IS_PUMPING'] = value
    if app.config['IS_PUMPING'] == False:
        stopPumping(app.config['PUMP_RELAY_PIN'])
    else:
        startPumping(app.config['PUMP_RELAY_PIN'])


def testSchedule(durationSek):
    print("pump for", str(durationSek), "seconds")


if __name__ == '__main__':
    # scheduler.add_job(id='scheduleTest', func=testSchedule, args=[10], trigger='cron', hour=12, minute=0)
    scheduler.start()
    app.run(host="0.0.0.0", port=8080)
