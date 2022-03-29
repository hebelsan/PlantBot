from flask import Flask, render_template, request, url_for,  redirect
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
from src.gpio import switchPumping
from src.scheduler import addJobToScheduler, removeJobFromSchedule, changeJobInScheduler
from src.weather import getWeather

#
# initial setup
#
class Config:
    """App configuration."""
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Europe/Berlin"

def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app)

    # watering configs
    app.config['PUMP_RELAY_PIN'] = 23
    app.config['IS_PUMPING'] = False
    app.config['PUMP_SCHEDULE'] = [{ 'id': 'initID', 'time': '08:24', 'duration':10 }]


    #
    # external routes
    #
    @app.route('/')
    def index():
        w_data = getWeather()
        return render_template(
            'index.html', 
            isPumping=app.config['IS_PUMPING'], 
            weather=w_data
        )

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
    def routeSwitchPumping():
        switchPumping(app)
        return 'Sucesss', 200
    
    @app.route('/weather')
    def weather():
        w_data = getWeather()
        return w_data

    @app.route('/addJob', methods=['POST'])
    def addJob():
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.json
            matches = [d for d in app.config['PUMP_SCHEDULE'] if d['id'] == json['id']];
            if (len(matches) == 0):
                app.config['PUMP_SCHEDULE'].append({ 'id':json['id'], 'time':json['time'], 'duration':json['duration'] })
                addJobToScheduler(scheduler, json)
            elif (len(matches) == 1):
                matches[0]['time'] = json['time']
                matches[0]['duration'] = json['duration']
                changeJobInScheduler(scheduler, json)
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
                removeJobFromSchedule(scheduler, requestID)
                return 'Sucesss', 200
            elif (len(d_list) == len(app.config['PUMP_SCHEDULE'])):
                return 'Job ID not found', 400
        return 'Wrong http header', 400
    
    # init existing pump jobs
    for entry in app.config['PUMP_SCHEDULE']:
        addJobToScheduler(scheduler, entry)
    scheduler.start()
    
    return app


if __name__ == '__main__':
    create_app()
