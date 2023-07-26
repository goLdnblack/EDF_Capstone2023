# SQL code
import sqlite3

import os,sys, random

from datetime import datetime
from datetime import timedelta

# Handle HTML swithing
from flask import Flask, flash
from flask import url_for, session
from flask import render_template, request, redirect


# Log application
import AppLogger

# Hash user passwords
from HashGenerator import HashGenerator

# AppLogger functions: (increasing severity)

# msg is string containing description

# log(msg)
# log_debug(msg)
# log_warning(msg)
# log_error(msg)
# log_critical(msg)


# Executable
base_dir = '.'

# Logger
logDir = (AppLogger.os.getcwd() + '\\log')
logger = AppLogger.logging.setLoggerClass(AppLogger.LogApp)
logger = AppLogger.setupLogger('edf_logger', logDir)

# Password Hash generator
hw = HashGenerator()

# Initialize app and connect to database
app = Flask(__name__)
database = sqlite3.connect("Database_EDF.db", check_same_thread=False)

# Start a SQL connection
def connectDB():
    try:
        sql = database.cursor()
    except:
        logger.critical(f'Unable to connect to DB.')
    else:
        logger.info(f'Successfully connected to DB.')

    return sql

# Generate a new unique ID for current EDF
def edfIDGenerator():
    edf_id = "%010d" % random.randint(0,9999999999)
    return edf_id


# TODO - Define role for user being registered
def registerUser(vid, name, password):
    
    # Check if the user already registered
    # in the database
    if (len(verifyUser(vid)) == 0):
        logger.info(f'User already exists in the database.')
        return

    salt = hw.generateSalt()
    hashed_salt_password = hw.generatePasswordSalt(password, salt)

    sql = connectDB()

    try:
        sql.execute('''
                    INSERT INTO USERS (vid, name, password, salt)
                    VALUES (?, ?, ?, ?)
                    ''', (vid, name, hashed_salt_password, salt))
    except:
        logger.critical(f'Unable to enter {str(vid)} into the database.')
    else:
        database.commit()
        logger.info(f'Successfully registered {str(vid)} into EDF database.')

    return

# TODO - The auto complete function (or a different one)
# should fill the information between form one and form two
# if the user has saved or wants to go back and edit
# a different field.

# TODO - When user signs in with their VID, auto fill form
# document sections based on their information from the
# database
def autoComplete(vid):
    sql = connectDB()
    sql.execute('''
                SELECT vid, name FROM USERS
                WHERE vid=?
                ''', (vid,))
    result = sql.fetchall()
    return result

# TODO - When clicking on confirm to make changes to database
# call this function to verify and quality check the information
# entered


# TODO - check date forms, they are not currently
# checking if the end date is after the start
def qualityCheck(data):
    # Data quality checks:
    # [4] date start time - must be before
    # course start
    # [11] and [12] course start and course end
    # course end cannot be before start

    datediff = 0

    #for x in range(len(data)):
    fulltime_start = datetime.strptime(data[4], "%Y-%m-%d")

    # The hire date shouldn't be older than at least set amount
    # of years
    dayCount = 365 * 80
    dateDiff = datetime.now() - timedelta(days=(dayCount))

    if fulltime_start <= dateDiff:
        logger.info(f'Start date older than {str(dayCount/365)} years.')
        return False
        
    # Check course dates
    #print(f'{data[9]}\n{data[10]}\n{data[11]}')
    course_start = datetime.strptime(data[10], "%Y-%m-%d")
    course_end = datetime.strptime(data[11], "%Y-%m-%d")

    if (course_end < course_start):
        logger.info(f'Course end date happens before the start date.')
        return False

    # Check if user is in the first part of the form
    if data[18] != None:
        conf_start = datetime.strptime(data[17], "%Y-%m-%d")
        conf_end = datetime.strptime(data[18], "%Y-%m-%d")

        if (conf_end < conf_start):
            logger.info(f'Conference end date happens before the start date.')
            return False
            

    # TODO - [13] could be designed
    # with a drop down menu to allow
    # for different types of degrees

    return True

# TODO - When someone else is looking for an existing EDF
# to approve, this method searches for it. Could find either
# by EDF ID or professor
def getEDF():
    return

# TODO - Update current EDF
def updateEDF():
    return

def createEDF(data):
    sql = connectDB()

    edf_id = edfIDGenerator()

    sql.execute('''
                SELECT edf_id FROM EDF
                WHERE edf_id=?
                ''', (edf_id,))
    
    result = sql.fetchall()

    # Generate a new unique ID until there
    # isn't one in the database already
    while (len(result) != 0):
        edf_id = edfIDGenerator()
        sql.execute('''
                SELECT edf_id FROM EDF
                WHERE edf_id=?
                ''', (edf_id,))
        result = sql.fetchall()
    
    # TODO - admin signature value is blank,
    # edf submitted should be 0 or 1 based on
    # the save or submit button.
    admin_signature = ""
    save_submit = 1

    # TODO - array value [5] and [6] should
    # be the account id and budget index,
    # unless they are fed separeately
    # into the EDF outside of the array
    bdgt_index = "121800"
    account = "598030"


    sql.execute('''
                INSERT INTO EDF (
                name,
                vid,
                department,
                position,
                edf_start,
                budget_index,
                account_id,
                course_name,
                course_number,
                credit_hours,
                degree_title,
                college,
                course_start,
                course_end,
                degree_program,
                out_of_pocket,
                workshop_title,
                host,
                location,
                workshop_start,
                workshop_end,
                registration_cost,
                registration_pay_method,
                purpose,
                benefit_college,
                employee_signature,
                admin_signature,
                edf_submitted,
                edf_id
                )
                VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?                
                )
                ''',
                (data[0],data[1],
                 data[2],data[3],
                 data[4],bdgt_index,
                 account,data[5],
                 data[6],data[7],
                 data[8],data[9],
                 data[10],data[11],
                 data[12],data[13],
                 data[14],data[15],
                 data[16],data[17],
                 data[18],data[19],
                 data[20],data[21],
                 data[22],data[23],
                 admin_signature,
                 save_submit,
                 edf_id,))
    
    database.commit()
    logger.info(f'Successfully updated database edf id {edf_id}')
    return

# TODO - remove auto filled forms in login page
# TODO - Change to compare both strings
# after applying to_upper to avoid case sensitive
def verifyUser(username, password):
    sql = connectDB()
    sql.execute('''
                SELECT UPPER(vid), password, salt FROM USERS
                WHERE vid=?
                ''', (username.upper(),))
    #sql.execute('''SELECT * FROM USERS''')
    result = sql.fetchall()

    if (len(result) == 0):
        logger.info(f'No user found.')
        return ""
    
    # Generate the same hash value based on the user's
    # salt value and password entered
    hashPassValue = hw.generatePasswordSalt(password, result[0][2])

    if (hashPassValue == result[0][1]):
        logger.info(f'User {str(username)} verified')
        return result[0][0]
    
    return ""

# TODO - HTML section below
###########################

# TODO - Set log in page as initial page
@app.route("/", methods=["POST", "GET"])
def login():

    logger.info(f'User attempting to log in')
    
    if request.method == "POST":
        session.permanent = True

        # Verify user credentials match database information
        user = request.form["vid"]
        password = request.form["password"]

        verifiedUser = verifyUser(user, password)

        if(len(verifiedUser) != 0):
            # Save username for session
            session['user'] = verifiedUser
            
            session['edfdata'] = [None] * 29
            

            return redirect(url_for("formPartOne"))
        else:
            flash('\nIncorrect username/password.')
            return redirect(url_for("login"))
        
    return render_template("Login.html")

# TODO - User registering to the EDF database
@app.route("/Register", methods=["POST", "GET"])
def register():

    return render_template("Register.html")

# TODO - Instead of going straight to the EDF page
# the first page could show a list of current EDF's
# in the database that are assigned to the specific
# user. The user could select to edit an already
# opened EDF, an admin could select an EDF
# that is waiting for their approval or create
# a brand new EDF which would go to the createEDF
# page.

# First page to enter information into EDF

# TODO - instead of calling autoComplete everytime
# the formPartOne page loads, call it at the login
# once to fill the session[] array with all the 
# user values to avoid multiple SQL calls

# TODO - check date forms, they are not currently
# checking if the end date is after the start
@app.route("/Form_Index", methods=["POST", "GET"])
def formPartOne():
    logger.info(f'Loaded blank EDF form')

    # This line allows the session to be modified
    # and used on a different route method.
    # Not sure if it needs to be set on every
    # route function.
    session.modified = True

    # TODO - could switch back to session[edf]
    # if session.modified fixed the previous issue
    result = autoComplete(session['user'])

    if request.method == "POST":
        # Quality check the data in the forms
        # before entering into database

        # TODO - change to storing the array or values
        # to session variable
        #edf_data = [None] * 29
        #edf_data[0] = result[0][1]
        #edf_data[1] = result[0][0]
        #x = 2

        # Reduce size of edfdata to avoid
        # making a larger list
        #if (len(session['edfdata']) >= 14):
        #    for data in session['edfdata']:
        #        session['edfdata'].pop()

        x = 0
        # EDF data is stored in the array in the order
        # they appear in the EDF form
        for key, val in request.form.items():
            #print(str(key), str(val))
            #edf_data[x] = val

            #session['edfdata'].append(val)
            session['edfdata'][x] = val
            x += 1

        # TODO - using data variable may show
        # the user data on the webpage url
        
        # TODO - fix by using {{session['edfdata']}}
        # in the html page instead of {{data}}
        if (qualityCheck(session['edfdata'])):
            logger.info(f'Data quality check success.')
            return redirect(url_for("formPartTwo"))
        else:
            logger.info(f'Data quality check failed.')
            # TODO - make flash be part of a group
            # that only shows up in the form page
            flash('Check data entered in form.')
            return redirect(url_for("formPartOne", 
                                    data=[result[0][1], result[0][0]]))

    # Data array is used to display information
    # from python program to HTML page.
    return render_template("index.html", 
                           data=[result[0][1], result[0][0]])

# Information page on how to navigate site
@app.route("/Instructions", methods=["POST", "GET"])
def instructPage():
    logger.info(f'Switched to instruct page')
    
    return render_template("Instructions.html")

# More information required to complete an EDF form
@app.route("/Form_Continued", methods=["POST", "GET"])
def formPartTwo():

    # Bring data from previous session information
    locallist = session.get('edfdata', None)

    # If the list is empty, return to
    # the first form
    if (len(locallist) < 1):
        return redirect(url_for("formPartOne"))

    if request.method == "POST":

        # Reduce size of edfdata to avoid
        # making a larger list
        #if (len(session['edfdata']) >= 24):
        #    for data in session['edfdata']:
        #        session['edfdata'].pop()

        x = 14

        for key, val in request.form.items():
            #print(str(key), str(val))
            #session['edfdata'].append(val)
            session['edfdata'][x] = val
            x += 1

        y = 0
        for x in session['edfdata']:
            print(f'[{y}]: {x}')
            y += 1

        if (qualityCheck(session['edfdata'])):
            logger.info(f'Data quality check success.')

            # Enter data into the database
            createEDF(session['edfdata'])
            
            return redirect(url_for("formPartTwo"))
        else:
            logger.info(f'Data quality check failed.')
            # TODO - make flash be part of a group
            # that only shows up in the form page
            flash('Check data entered in form.')
            return redirect(url_for("formPartTwo"))

    return render_template("Form2Page.html")

###########################
# END OF HTML CODE

if __name__ == "__main__":
    # Initialize logging
    # init()
    logger.info(f'Program start')

    if hasattr(sys, '_MEIPASS'):
        base_dir = os.path.join(sys._MEIPASS)

    # Initialize HTML page
    app.secret_key = '2023edf'
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)
    database.close()
