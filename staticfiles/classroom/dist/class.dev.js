"use strict";

var username;
var class_id = window.location.pathname.split("/")[2]; // CSRF TOKEN

var csrftoken = Cookies.get('csrftoken');
document.addEventListener('DOMContentLoaded', function () {
  // Buttons to toggle views \
  document.querySelector('#assignments').addEventListener('click', function () {
    show_view("assignments-div");
  });
  document.querySelector('#chat').addEventListener('click', function () {
    show_view("chat-div");
  });
  document.querySelector('#students').addEventListener('click', function () {
    show_view("student-div");
  });

  try {
    document.querySelector('#question').addEventListener('keyUp', function (e) {
      if (e.keyCode === 13) {
        if ($('#question').val() !== "") {
          create_class();
        }
      }
    });
  } catch (_unused) {}

  try {
    document.querySelector('#new-hw').addEventListener('click', function (e) {
      if (document.querySelector('.hw-form').style.display !== 'block') {
        document.querySelector('.hw-form').style.display = 'block';
      } else {
        document.querySelector('.hw-form').style.display = 'none';
      }
    });
  } catch (_unused2) {}

  try {
    document.querySelector('.assignment').addEventListener("click", function (e) {
      var hw_id = document.querySelector('.assignment').firstChild.nextElementSibling.value;
      console.log(class_id);
      console.log(hw_id);
      window.location.pathname = "/work/" + class_id + "/" + hw_id;
    });
  } catch (_unused3) {}

  document.querySelector('#leave').addEventListener('click', function (e) {
    var leave = confirm("Are you sure you want to leave?");

    if (leave === true) {
      fetch('/api/leave/' + class_id).then(function (response) {
        return response.json();
      }).then(function (data) {
        alert(data.message);
      });
    }
  }); // by default, load the chat

  show_view("chat-div");
  var msg = document.querySelector('#msg');
  var socket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + window.location.pathname[7] + '/');
  document.querySelector('#announce').addEventListener('click', function (e) {
    var announcement = prompt("Message: ");

    if (announcement !== "") {
      socket.send(JSON.stringify({
        'annoucement': announcement
      }));
    }
  });

  socket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    var msg = document.createElement('li');

    if (data.message) {
      msg.innerHTML = data.message;
      document.querySelector('#messageslist').appendChild(msg);
    } else {
      alert("Message from ".concat(username, ": ").concat(data.annoucement));
    }
  };

  socket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
    socket;
  };

  document.querySelector('#msg').focus();

  document.querySelector('#msg').onkeyup = function (e) {
    if (e.keyCode === 13) {
      // enter, return
      msgDom = document.querySelector('#msg').value;
      msgDom = "<strong>".concat(msgDom, "</strong> from <strong>").concat(username, "</strong>");
      socket.send(JSON.stringify({
        'message': msgDom
      }));
      document.querySelector('#msg').value = '';
      msg.focus();
    }
  };

  get_user();
  document.querySelector('#invite').addEventListener('click', function (e) {
    var invite = prompt('Username of student you would like to invite: ');
    socket.send(JSON.stringify({
      'username': invite
    }));
  });
});

function create_class() {
  var data = parse_data(document.querySelector('.output').innerHTML, document.querySelector('#question').value);
  var request = new Request('/api/create/' + class_id, {
    headers: {
      'X-CSRFToken': csrftoken
    }
  });
  fetch(request, {
    method: 'POST',
    body: JSON.stringify(data)
  }).then(function (response) {
    return response.json();
  }).then(function (data) {
    alert(data.message);
  });
}

function get_user() {
  fetch('/api/user').then(function (response) {
    return response.json();
  }).then(function (data) {
    username = data.username;
  });
}

function show_view(div) {
  divs = ["assignments-div", "student-div", "chat-div"];
  document.getElementById(div).style.display = 'block';

  try {
    if (div === "assignments-div") {
      document.querySelector('.hw-form').style.display = 'none';
    }
  } catch (_unused4) {}

  divs.forEach(function (item) {
    if (div != item) {
      document.getElementById("".concat(item)).style.display = 'none';
    }
  });
}

function parse_data(date, question) {
  var date_as_array = date.split(".");
  var day = parseInt(date_as_array[0]);
  var month = parseInt(date_as_array[1]);
  var year = parseInt(date_as_array[2]);
  var date_as_json = new Object({
    "day": day,
    "month": month,
    "year": year,
    "question": question
  });
  return date_as_json;
}