from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
from assignment import *
import datetime

db = TinyDB('planr.json')

app = Flask(__name__, template_folder="web/", static_folder="web/static/")


def getAssignmentByDate(date):
    assignment = Query()
    return db.search(assignment.date==date)
    

def calcRings(totalTime,activityTime,workTime):
    if activityTime+workTime>totalTime:
        return [1], ["Time Used"]
    else:
        return [workTime,activityTime,totalTime-activityTime-workTime], ["Work Time", "Activity Time", "Free Time"]


def htmlString(tags):
    htmlString = ""
    for tag in tags:
        if tag == "Work Time":
            htmlString += '<div class="chart-note mr-0 d-block"><span class="dot dot--blue"></span><span>Work Time</span></div>'
        if tag == "Activity Time":
            htmlString+= '<div class="chart-note mr-0 d-block"><span class="dot dot--red"></span><span>Activity Time</span></div>'
        if tag == "Free Time":
            htmlString+= '<div class="chart-note mr-0 d-block"><span class="dot dot--green"></span><span>Free Time</span></div>'
    return htmlString


@app.route('/')
def index():

    tags = {
        "time_today": "25-30",
        "today_due": 4,
        "tmrw_due": 33,
        "nxt_due": 4,
        "pie_data": calcRings(90, 30, 100)[0],
        "pie_tags": calcRings(90, 30, 100)[1],
        "pie_dots": ["r", "f", "f"]
    }

    return render_template("index.html", **tags)

@app.route('/add_assignment', methods=['GET', 'POST'])
def newAssignment():
    if request.method == 'POST':
        assignmentName = request.form.get("name")
        className = request.form.get("class")
        typeName = request.form.get("type")
        dueDate = request.form.get("date")
        notes = request.form.get("notes")
        duration = request.form.get("duration")
        attachments = request.form.get("attachments")

        assignment = Assignment(assignmentName,className,typeName,dueDate,notes,duration,attachments)

        print(assignment.dictionary())

        db.insert(assignment.dictionary())

        return redirect(url_for("index"))
    else:
        return render_template("add_assignment.html")



def widgetData():
    date_time_str = DateTime.Now.toString(MM/dd/yyyy)
    assignment = Query()
    dueToday = []
    dueTomorrow = []
    dueLater = []
    dueToday.append(db.search(assignment.date==))
    return 

if __name__ == "__main__":
    app.run()