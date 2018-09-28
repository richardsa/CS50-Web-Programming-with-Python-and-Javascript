document.addEventListener('DOMContentLoaded', () => {
    // prompt user to set username if not already set
    if (!localStorage.getItem('displayname'))
        $('#login-modal').modal('show');

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    const displayNameForm = document.getElementById('display-name-form');
    /* listen for form submit */
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
            console.log(channel);
            const displayName = localStorage.getItem('displayname');
            $(chatForm ).on('submit', function(e){
                e.preventDefault();
                const chatText = $('#chat-text').val();
                socket.emit('submit chat', {'chatText': chatText, 'channel': channel, 'displayName': displayName});
                $('#chat-text').val('');
            });
        }
    });

    // When a new vote is announced, add to the unordered list
    socket.on('display chats', data => {
        const li = document.createElement('li');
        li.innerHTML = `<span class="username">${data.displayName}:</span> ${data.chatText}`;
        document.querySelector('#chats').append(li);

    });



});
