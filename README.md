# Group-Project
##	About the project

This project is a location-based, territory controlled, trivia game that allows students (currently at Texas State University) to do the following:
* to create a profile
* select one of three teams (based on University school colors)
* answer trivia questions based on the majors (i.e. Computer Science, English, Nursing, etc.) who occupy the building  

##	Team members

Adam Garcia, Brittany Torelli, Casey Sledge, Claudia Ortiz, Collin Weir, Jeremiah Burks, Kaleb Jacobson

##	Neccessary Libraries

The program is developed in Pycharm using flask. In order to compile the program, you will need the following libraries: 

  * Flask
  
  * Flask-script
  
  * Flask-socketIO
  
  * Jinja2
  
  * MarkupSafe
  
  * SQLAlchemy
  
  * eventlet
  
Additionally, all clients will need the SocketIO.js library, version 1.4.5, available at socket.io/download, or by using the source below in the client page:
  
  * https://cdn.socket.io/socket.io-1.4.5.js
  
In order to host the project on a live server vs local we used digital ocean. You can do this following the steps in their api 

  •	PUT LINK HERE
  
To run the program on a local machine, compile and run the python file runserver.py

For new installations, running the server will create and populate the database backend using specified JSON files for hard-coded information. These source files include coordinates for the buildings you wish to represent on the map, a starter set of questions and their answers, and the basic state of the game. For demonstration purposes the state file (state.json) shows some buildings as occupied by various teams. This behavior can be controlled by deleting the database, changing the buildingScore and buildingOwner values of the building to 0, and restarting the server. 

##	Basic overview about the functionality achieved

After creating an account, using Google Maps API, the location of the user is used to determine what building (if any) the user is in. If not in a building the user cannot answer any questions. The user gets a base session of 5 questions per building per day. This is to encourage the user to not only explore the campus, but to answer questions outside their major and comfort zone in order to help their team. If the If the building is neutral (no team owns it) the building will be set to a base score of 5 points and captured by the team of the first person to answer a question correctly. If the building currently has an owner, the points on the building will decrement by 1 point per question as opposing teams answer questions correctly, and increment by 1 point per question as the current owner’s team answers questions correctly. Currently you can view the top scorers on the leaderboard page, and search through each team to see player’s profiles. When playing the game, a map is present showing an icon on your current location, and every building that has questions associated with them bordered. Each building will be colored either blue (unclaimed) or the corresponding teams color. The buildings color’s transparency will change as the score of the building becomes closer to 0 or max points.

##	Future design implementation

We plan to add more questions, which will including true or false. As well as add the ability to select the level of difficulty of the questions for the chance to earn more than 5 points in the session the user gets per day. 
Also an update to the questions and building JSON file implementing the enum associated with each major instead of hard coding literal numbers. 

##	Major bottlenecks

Hosting the server so that the game is live instead of on a local machine. 
Learning socketIO

