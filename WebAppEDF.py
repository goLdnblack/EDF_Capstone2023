# SQL code
import sqlite3

import os,sys, random

# Handle HTML swithing
from flask import Flask, flash
from flask import url_for, session
from flask import render_template, request, redirect

import datetime

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

# TODO - is there an exemption not being caught
# if the user is able to enter the URL of form
# two and bypass the first form?
def qualityCheck(data):
    # Data quality checks:
    # [4] date start time - must be before
    # course start
    # [11] and [12] course start and course end
    # course end cannot be before start

    # TODO - [13] should have extra values for yes
    # and Masters/Doctorate/Bachelor/Associate

    # Check if list is larger than 14 to check
    # data in form 2

    # [17] and [18] start date and end date
    # [18] cannot happen before [17]

    return True

# TODO - When someone else is looking for an existing EDF
# to approve, this method searches for it. Could find either
# by EDF ID or professor
def getEDF():
    return

# TODO - Update current EDF
def updateEDF():
    return

# TODO - remove auto filled forms in login page
# TODO - Change to compare both strings
# after applying to_upper to avoid case sensitive
def verifyUser(username, password):
    sql = connectDB()
    sql.execute('''
                SELECT vid, password, salt FROM USERS
                WHERE vid=?
                ''', (username,))
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
        # Verify user credentials match database information
        user = request.form["vidlogin"]
        password = request.form["password"]

        verifiedUser = verifyUser(user, password)

        if(len(verifiedUser) != 0):
            # Save username for session
            session['user'] = verifiedUser
            

            # TODO - could create the EDF array
            # here to begin saving data between
            # pages
            # edf_data = [None] * 29
            session['edfdata'] = []
            

            return redirect(url_for("formPartOne"))
        else:
            return redirect(url_for("login"))
        
    return render_template("Login.html")

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
        if (len(session['edfdata']) >= 14):
            for data in session['edfdata']:
                session['edfdata'].pop()

        # EDF data is stored in the array in the order
        # they appear in the EDF form
        for key, val in request.form.items():
            #print(str(key), str(val))
            #edf_data[x] = val

            session['edfdata'].append(val)
            #x += 1

        print(f'Size of list in form index: {str(len(session["user"]))}')
        print(f'{str(session["user"])}')

        # TODO - quality check the data
        if (qualityCheck(session['edfdata'])):
            logger.info(f'Data quality check success.')
            return redirect(url_for("formPartTwo"))
        else:
            logger.info(f'Data quality check failed.')
            return redirect(url_for("index.html", 
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
    print(f'{str(session["edfdata"])}')
    locallist = session.get('edfdata', None)


    print(f'Size of list before POST form continued {str(len(locallist))}')

    if request.method == "POST":

        # Reduce size of edfdata to avoid
        # making a larger list
        if (len(session['edfdata']) >= 24):
            for data in session['edfdata']:
                session['edfdata'].pop()

        
        for key, val in request.form.items():
            #print(str(key), str(val))
            session['edfdata'].append(val)

        print(f'Size of list {str(len(session["edfdata"]))}')

        for data in session['edfdata']:
            print(str(data))

    return render_template("Form2Page.html")


###########################

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
