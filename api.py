# this file will handle the api calls between the server and client
from init import socketio, SocketIO, app, datab
import flask_socketio
import flask
import models
import questionLogic
from state import requestState, updateState

@socketio.on('connect')
def on_connect():
    # get the connecting user's user ID
    # flask.session works in socket IO handlers :)
    uid = flask.session.get('auth_user', None)
    if uid is None:
        app.logger.warn('received socket connection from unauthed user ', uid)
        return

    app.logger.info('new client connected for user %d', uid)

    # add this connection to the user's 'room', so we can send to all
    # the user's open browser tabs
    flask_socketio.join_room('user-{}'.format(uid))


@socketio.on('disconnect')
def on_disconnect():
    uid = flask.session.get('auth_user', None)
    if uid is None:
        app.logger.warn('received socket connection from unauthed user ', uid)
        return

    flask_socketio.close_room('user-{}'.format(uid))
    app.logger.info('client disconnected')


@socketio.on('ready')
def readyState(obj):
    uid = flask.session.get('auth_user', None)
    if (not obj):
        print ("Setting response:")
        response = requestState({"type": "new"}) #TODO, Fix Error, response is being set to NULL!
        print("Response is:")
        print (response)
        flask_socketio.emit('stateFullUpdate', response, room='user-{}'.format(uid))

#TODO FIX CHECK LOCATION using building short codes
def check_location(user_location):
    latitude = user_location['latitude']
    longitude = user_location['longitude']



@socketio.on('changeLocation')
def location_change(u_loc):
    #TODO: u_loc has building short code and "continuous" int, 0 send question, 1 do nto send question
    print("LOCATION_CHANGE")
    if u_loc != None:
        app.logger.info('received user location')

    else:
        app.logger.info('did not receive user location')
        return

    # TODO, pull out building
    # TODO, if building is not empty, pull out via shortcode
    b_shortcode = u_loc['building']
    print ("In location change, building code is:")
    print (b_shortcode)

    continuous = u_loc["continuous"]  #A true or false value that marks if the user is in the same building they were in previously

    if b_shortcode is "":
            print("building code is blank, do not care")
    else:

        b = models.Building.query.filter_by(building_shortcode = b_shortcode).first()
        b_id = b.id

        uid = u_loc['uid']
        latitude = u_loc['latitude']
        longitude = u_loc['longitude']

        print(latitude, " ", longitude)
        user = models.User.query.get(uid)
        print(user.email)

        if continuous is 1: #Continous is true, the user has move significantly but has not left their building.
            u_session = models.question_session.query.filter(models.question_session.user_id == user.id, models.question_session.building_id == b_id).first()
            if u_session is None:
                print("User is still in building, but no previous session found, this is weird and should not happen")

        else: #continuous is false, could be building is first entered or rentered. Time to generate question data

            if True: #If the user location is in a building, TODO, add verification that client data is correct
                if user.building != b_id: #And that building is not stored on the user's record
                    user.building = b_id  #store the building id to the user's record
                    datab.session.commit()
                question_serv(uid, b_id)

            else: #The user is not in a building
                if user.building != "": #If they have existing building data, clear it.
                    user.building = ""
                    datab.session.commit()
                print("User position updated outside of valid building")
                blankObj = None
                flask_socketio.emit('noChangeEvent', blankObj, room='user-{}'.format(uid))

    #flask_socketio.emit('enterBuilding', {"building": user_building}, room='user-{}'.format(uid))
    #EnterBuilding event is being bypassed by going straight to the generateQuestions function.

#This method works with the change location function to determine if a long/lat coordinate is actually inside the expect
#building. Buildings are given by the building shortcode.
def pointWithinBuilding(longitude, latitude, b_code):
    building = models.Building.query.filter_by(building_shortcode = b_code).first()
    coordinate_list = models.coordinate_point.query.filter_by(building.id)
    coordinate_list = list(coordinate_list)

    #TODO, finish function. Should return false if point is not in building. Currently assuming the point is correctly in the building.
    return True

#@socketio.on('generateQuestions')
def question_serv(uid, bldid):
    #uid = cli['userID']

    #bldid = cli['buildingID']

    print ("****Question was called****")

    print("Building ID:")
    print(bldid)

    user_question_session= questionLogic.question_handler(uid, bldid) #Create question session, or pull session if it exist
    if user_question_session.session_is_closed:
        socketio.emit('noMoreQuestions', {'result': "You are out of questions"}, room='user-{}'.format(uid))
    else:
        Q_obj = user_question_session.serializeCurrentQuestion()
        socketio.emit('question', Q_obj, room='user-{}'.format(uid))

@socketio.on('answer')
def answer_question(cli):
    print("****answer****")
    app.logger.info("****Answer****")
    # call the database and test the answer and question
    userAnswer = cli['userAnswerId']
    questionID = cli['questionId']

    questionObj = models.Question.query.get(questionID)

    print ("your answer:")
    print (userAnswer)
    print ("correct answer:")
    print (questionObj.q_answer)

    if int(userAnswer) == int(questionObj.q_answer):
        print("You got it right!")
        result = "You got it right!"
    else:
        print("You got it wrong :(")
        result = "You got it wrong."

    # delete database question entry from stack
    # TODO: flask.session.get(uid)? add delete to session object

    socketio.emit('result', result) #result = some boolean based on if above

    # if no more questions, emit end status

    # TODO: get user at max test from questionLogic
    #socketio.emit('qLimit') #qLimit = some message saying "Reached max for today, try again tomorrow"

    # TODO : recalculate state on the basis of a correct question.
    # updateState()

    uid = flask.session.get('auth_user')
    user = models.User.query.get(uid)
    user_question_session = questionLogic.question_handler(user.id, user.building)
    user_question_session.removeAnsweredQuestion()
    Q_obj = user_question_session.serializeCurrentQuestion()

    print("Sending next question")
    print(Q_obj)


    socketio.emit('question', Q_obj, room='user-{}'.format(uid))


def updateUserStats(uid, answerIsCorrect): #Uid is the id of the user, result is a bool for question
    return