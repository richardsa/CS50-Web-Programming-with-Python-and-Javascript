// For todays date;
Date.prototype.today = function () {
    return ((this.getDate() < 10)?"0":"") + this.getDate() +"/"+(((this.getMonth()+1) < 10)?"0":"") + (this.getMonth()+1) +"/"+ this.getFullYear();
}

// For the time now
Date.prototype.timeNow = function () {
     return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
}

document.addEventListener('DOMContentLoaded', () => {
    // prompt user to set username if not already set
    if (!localStorage.getItem('displayname'))
        $('#login-modal').modal('show');

     if (localStorage.getItem('displayname') && localStorage.getItem('channel')) {
         const channel = localStorage.getItem('channel');
         const channelLink = document.getElementById('previous-room-link');
         $('#previous-room').show();
         channelLink.href = "/channel/" + channel;
     }

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    const displayNameForm = document.getElementById('display-name-form');
    /* listen for login form submit */
    $(displayNameForm ).on('submit', function(e){
         e.preventDefault();
         const displayName = $('#display-name').val();
         console.log(displayName)
         $('#login-modal').modal('hide');
         $('#display-name').val('');
         localStorage.setItem('displayname', displayName);
    });



    socket.on('connect', () => {
        if(window.location.href.indexOf("channel") > -1) {
            const chatForm = document.getElementById('chatForm');
            const channel = chatForm.dataset.channel;
            // set storage
            localStorage.setItem('channel', channel);
            console.log(channel);
            const displayName = localStorage.getItem('displayname');
            $(chatForm ).on('submit', function(e){
                e.preventDefault();
                const chatText = $('#chat-text').val();
                const newDate = new Date();
                let timestamp = newDate.today() + " @ " + newDate.timeNow();
                console.log(timestamp )
                socket.emit('submit chat', {'chatText': chatText, 'channel': channel, 'displayName': displayName, 'timestamp': timestamp });
                $('#chat-text').val('');
            });
        }

        // listen for add room form submit
        const channelNameForm = document.getElementById('room-name-form');
        $(channelNameForm).on('submit', function(e){
             e.preventDefault();
             const roomName = $('#room-name').val();
             console.log(roomName)
             $('#create-modal').modal('hide');
             $('#room-name').val('');
             socket.emit('create room', {'channel': roomName});
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('display chats', data => {
        const li = document.createElement('li');
        li.innerHTML = `On <span class="timestamp">${data.timestamp}</span> <span class="username">${ data.displayName } </span> wrote <span class="message">${ data.chatText } </span>`;
        document.querySelector('#chats').append(li);
        const elem = document.getElementById('chats');
        elem.scrollTop = elem.scrollHeight;

    });

    // When a new vote is announced, add to the unordered list
    socket.on('enter room', data => {
        const channel = data["channel"];
        console.log('channel' + channel);
        window.location.href = "/channel/" + channel;
    });

});
