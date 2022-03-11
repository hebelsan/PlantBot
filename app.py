from flask import Flask, render_template, request, url_for,  redirect
from gpio import startPumping, stopPumping
from flask_apscheduler import APScheduler

app = Flask(__name__)

# watering configs
app.config['PUMP_RELAY_PIN'] = 23
app.config['IS_PUMPING'] = False
app.config['PUMP_SCHEDULE'] = [{ 'time': '12:00', 'durationSek':10 }]

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

def setPumping(value):
    app.config['IS_PUMPING'] = value
    if app.config['IS_PUMPING'] == False:
        stopPumping(app.config['PUMP_RELAY_PIN'])
    else:
        startPumping(app.config['PUMP_RELAY_PIN'])


def testSchedule(durationSek):
    print("pump for", str(durationSek), "seconds")

@app.route('/removeJobs')
def removeJobs():
    scheduler.remove_all_jobs()
    return 'Sucesss', 200

@app.route('/addJob')
def addJob():
    # jobId, time, durationSeconds
    scheduler.add_job(id='scheduleTest', func=testSchedule, trigger='interval', seconds=3)
    return 'Sucesss', 200


if __name__ == '__main__':
    # scheduler.add_job(id='scheduleTest', func=testSchedule, args=[10], trigger='cron', hour=12, minute=0)
    scheduler.start()
    app.run(host="0.0.0.0", port=8080)
