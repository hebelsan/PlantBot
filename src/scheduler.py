def addJobToScheduler(scheduler: object, timeEntry: dict):
    hours, minutes = getHourMinute(timeEntry['time'])
    jobID = timeEntry['id']
    scheduler.add_job(
        id=jobID, 
        func=testSchedule,
        args=[timeEntry['duration']],
        trigger='cron',
        hour=hours,
        minute=minutes
    )

def changeJobInScheduler(scheduler: object, timeEntry: dict):
    jobID = timeEntry['id']
    removeJobFromSchedule(scheduler, jobID)
    addJobToScheduler(scheduler, timeEntry)

def removeJobFromSchedule(scheduler: object, jobID: str):
    scheduler.remove_job(id=jobID)

# transforms '12:15' to 12, 15
def getHourMinute(time: str):
    arr = time.split(':', 1)
    return arr[0], arr[1]

def testSchedule(durationSek):
    print("pump for", str(durationSek), "seconds")