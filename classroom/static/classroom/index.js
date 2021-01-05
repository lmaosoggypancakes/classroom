
document.addEventListener("DOMContentLoaded", () => {

    if(window.location.pathname === "/") {
        const m = window.createNotification({});
        const ws = new WebSocket(
            'ws://' + window.location.host + '/'
        )
        ws.onopen = (e) => {
            console.log("Connected!");
        }
        ws.onmessage = (e) => {
            console.log(e.data)
            m({
                title: 'New User',
                message: e.data,
                positionClass: 'nfc-bottom-right',
                displayCloseButton: true,
                theme: 'info',
                showDuration: 5000
            })
        }
    }
    
})

function stop_anim() {
    document.querySelector('.form').style.AnimtionPlayState = 'paused';
}
document.addEventListener('scroll', (e) => {
    var scrollTop = $(window).scrollTop();
    if (scrollTop > 100) {
        $("#create-1").css('animation-play-state', 'running')
    }
    if (scrollTop > 150) {
        $("#create-2").css('animation-play-state', 'running')
    }
    if ($("#name").val() != '') {
        if (scrollTop > 200) {
            $("#create-3").css('animation-play-state', 'running')
        }
    }
    
})
document.addEventListener('DOMContentLoaded', () => {
    var final_name;
    var final_icon;
    $('#final_create').click(() => {
        final_name = $('#name').val();
        const form = document.querySelector('#final_create_form')
        document.querySelector('#final_name').value = final_name;
        document.querySelectorAll('.name').forEach(item => {
            if (item.checked === true) {
                final_icon = item.value
            }
        })
        document.querySelector('#final_icon').value = final_icon;
        form.submit()
    })
    document.querySelectorAll('.name').forEach(item => {
        item.addEventListener('click', () => {
            $('#custom_icon').val('')
        })
    })
    try {
    document.querySelector('#custom_icon').addEventListener('keypress', () => {      
        if($('#custom_icon').val() === '') {
            document.getElementById("english").checked = false;
            document.getElementById("math").checked = false;
            document.getElementById("science").checked = false;
            document.getElementById("math").checked = false;
        }
    });
    } catch (err)  {console.error(err)}
});