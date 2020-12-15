# Welcome!
### This is my submission for CS50 Web's Final Project: Capstone.

Classrooms50 is a platform where students can join a teacher's classroom. Students can answer and submit assigments, join a class, and chat, real-time, with fellow students and teachers. Teachers can create assignments for all students in a class, invite students to classes, kick misbehaving students, and create and delete classrooms.

# API 

Whether deployed to the web or in production, Classroom50 has a range of API routes to manage user data.

`/api/user`

Sending a GET request to this route will return the current logged in user. It will return, as a JSON object, the following data: 

```
{
            "username": self.username,
            "id": self.id,
            "is_teacher": self.is_teacher,
            "timestamp": self.last_login.strftime("%b %#d %Y, %#I:%M %p"),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

```

`api/create`

Creates a new classroom with the sent JSON data. Note that a CSRF token is required; this can be obtained using vanilla JS or with the JavaScript Cookie library.

```
    const request = new Request(
        '/api/create',
        {headers: {'X-CSRFToken': csrf_token}}
    );
```

```
        fetch(request, {
        method: 'POST',
        body: JSON.stringify({
            "question": "what is the square root of 9?",
            "day": "04",
            "month": "12",
            "year": "2020"
        })
    })
```

The following example will create an assignment for each student with the question *what is the square root of 9?* that will be due on *December 4, 2020*
The body will be left blank for users to fill in with their answer. Note that the requested user **must** be logged in as a teacher.

# Live Chat

The live chat portion of this project utilizes Channels and Redis, with the framework django-channels to provide communications. Chat rooms are divided based on classrooms, so students can only talk with other students in the same classroom.

# Forgot Password?

Another backend feature provided in this project is the ability for a user to reset their password. To ensure this security, this takes place over a sequence of steps: 
1. The user is prompted to provide the email of their account with the forgotten password.
2. Using a GMail framework, an email is sent to the requested email (for security reasons this email will be empty when submitting. this can be easily changed by setting the `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` variables in `settings.py` to your email's address and password, respectively.)
3. The email will lead to the base url with the extension `reset/password/<str:hash>` where `<str:hash>` is the hashed version of the email, to provide security.
4. Once the user visits the link, he/she can change their password, then they are logged back in and redirected to the home view.
5. Lastly, the request is deleted from the database and the user's account is restored.

# File overview

This project is structured very similar to that of a regular Django project. 
- `capstone/asgi.py`: file to manage ASGI deployment(in order to provide support for WebSockets. Django Channels takes over deploying while ASGI is being used in this case.)
- `capstone/consumers.py`: file that manages WebSocket events, in this case being used solely for the live chat functionality and invites. Each WebSocket event is defined as a class method.
- `capstone/routing.py`: file that sets the URL at which the web socket (django-channels and redis) will listen to.
- `capstone/settings.py`: old fashioned settings file, with few addons to support ASGI development and Email sending.
- `capstone/urls.py`: Manages the URLs for the entire project, for this submission it utilizes only one app.
- `capstone/wsgi.py`: Unused file due to using asgi.py
- `static/classroom/class.js`: JavaScript file that manages div-displaying within the class view, as well as fetching and making classes.
- `static/classroom/index.js`: General JS file with event listeners to provide dynamic form submitting in the create classroom view.
- `static/classroom/styles.css`: Stylesheet to manage most of the templates' styles, as well as to provide for responsive design.
- `classroom/admin.py`: Admin file used to add, edit, and delete any Users, Classes or Assignments.
- `classroom/emails.py`: email function that hashes the email, turns it into a URL and saves the request in a database.
- `classroom/ip.py`: Simple IP function that returns the user's IP based on the request object.
- `classroom/models.py, classroom, views.py, classroom/urls.py`: Files that manage user events, database management, and URL redirects and template loading.

# Deploying to the web

Because this is an ASGI app, one may find themselves having trouble if they wish to deploy this app. As it is open source, I have added a requirements.txt file which contains all of the required python libraries. Further details on how to deploy can be found in the docs of whatever platform you want to deploy on.

# Justification

My justification for why my submission is both more complex than other projects and mobile-responsive is that I utilize more than one Django model, get my hands dirty with model relations, and the use of Javascript to assist in mobile response. Additionally, it has implementation of web sockets and emails to provide a better user experience.

# Final Notices/Disclaimers

This application uses JQuery, a javascript library that saves time coding and contains lots of community created apps. In this project, one is used, the Calandar widget in the create assignment view.

Additionally, I have created the WebSocket implementation with the help of a tutorial from the Django-Channels documentation. Further details can be found on their website:

Jquery calandar plugin documentation:
https://www.jqueryscript.net/demo/multilingual-calendar-date-picker/
Django Channels:
https://channels.readthedocs.io/en/stable/
Tutorial followed:
https://channels.readthedocs.io/en/stable/tutorial/index.html
Jquery:
https://jquery.com/