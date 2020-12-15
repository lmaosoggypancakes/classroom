var username;
const class_id = (window.location.pathname.split("/")[2])
// CSRF TOKEN
const csrftoken = Cookies.get('csrftoken');
document.addEventListener('DOMContentLoaded', () => {
    // Buttons to toggle views \
    document.querySelector('#assignments').addEventListener('click', () => { show_view("assignments-div") })
    document.querySelector('#chat').addEventListener('click', () => { show_view("chat-div") })
    document.querySelector('#students').addEventListener('click', () => { show_view("student-div") })
    try {
        document.querySelector('#question').onkeyup = (e) => {
            if (e.keyCode === 13) {
                if($('#question').val() !== "") {
                    create_class()
                    }
                }
            };
        }
    catch {}
    try {
    document.querySelector('#new-hw').addEventListener('click', (e) => {
        if (document.querySelector('.hw-form').style.display !== 'block') {
        document.querySelector('.hw-form').style.display = 'block'
        }
        else {
            document.querySelector('.hw-form').style.display = 'none';
        }
    })
    }
    catch {}
    try {
        document.querySelector('.assignment').addEventListener("click", (e) => {
            var hw_id = document.querySelector('.assignment').firstChild.nextElementSibling.value
            console.log(class_id)
            console.log(hw_id)
            window.location.pathname = "/work/" + class_id + "/" + hw_id
        })
    }
    catch {}
    document.querySelector('#leave').addEventListener('click', (e) => {
        var leave = confirm("Are you sure you want to leave?")
        if (leave === true) {
            fetch('/api/leave/' + class_id).then(response => response.json()).then(data => {alert(data.message)})
        }
    })
    // by default, load the chat
    show_view("chat-div")
    const msg = document.querySelector('#msg');
    const socket = new WebSocket(
        'wss://'
        + window.location.host
        + '/ws/chat/'
        + window.location.pathname[7]
        + '/'
    );
    document.querySelector('#announce').addEventListener('click', (e) => {
        var announcement = prompt("Message: ")
        if(announcement !== "") {
            socket.send(JSON.stringify({
                'annoucement': announcement
            }));
        }
    });
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const msg = document.createElement('li')
        if(data.message) {
        msg.innerHTML = data.message;
        document.querySelector('#messageslist').appendChild(msg)
        }
        else {
            alert(`Message from ${username}: ${data.annoucement}`)
        }
    };
    socket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        socket
    };

    document.querySelector('#msg').focus();
    document.querySelector('#msg').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            msgDom = document.querySelector('#msg').value;
            msgDom = `<strong>${msgDom}</strong> from <strong>${username}</strong>`
            socket.send(JSON.stringify({
                'message': msgDom
            }));
            document.querySelector('#msg').value = '';
            msg.focus()
        }
    };
    get_user();
    document.querySelector('#invite').addEventListener('click', (e) => {
        const invite = prompt('Username of student you would like to invite: ')
        socket.send(JSON.stringify({
            'username': invite
        }))
    })
})

function create_class() {
    var data = parse_data(document.querySelector('.output').innerHTML, document.querySelector('#question').value)
    const request = new Request(
        '/api/create/' + class_id,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        body: JSON.stringify(data)
    }).then(response => response.json()).then(data => {alert(data.message)})
}
function get_user() {
    fetch('/api/user').then(response => response.json()).then(data => {
        username = data.username;
    })
}

function show_view(div) {
    divs = ["assignments-div", "student-div", "chat-div"]
    document.getElementById(div).style.display = 'block';
    try {
    if (div === "assignments-div") {
        document.querySelector('.hw-form').style.display = 'none';
        }
    }
    catch {}
    divs.forEach(item => {
        if(div != item) {
            document.getElementById(`${item}`).style.display = 'none';
        }
    });
}


function parse_data(date, question) {
    var date_as_array = date.split(".");
    var day = parseInt(date_as_array[0])
    var month = parseInt(date_as_array[1])
    var year = parseInt(date_as_array[2])
    var date_as_json = new Object({
        "day": day,
        "month": month,
        "year": year,
        "question": question
    })
    return date_as_json
}