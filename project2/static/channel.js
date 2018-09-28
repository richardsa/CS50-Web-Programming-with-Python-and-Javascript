document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);



    socket.on('connect', () => {
        const chatForm = document.getElementById('chatForm');
        const channel = "Default"
        const displayName = localStorage.getItem('displayname');
        $(chatForm ).on('submit', function(e){
            e.preventDefault();
            const chatText = $('#chat-text').val();
            socket.emit('submit chat', {'chatText': chatText, 'channel': channel, 'displayName': displayName});
            $('#chat-text').val('');
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('display chats', data => {
        const li = document.createElement('li');
        li.innerHTML = `username: ${data.displayName} and chat: ${data.chatText}`;
        document.querySelector('#chats').append(li);

    });


});
