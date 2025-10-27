
  (function() {
    const channelName = "{{ channel.name }}";
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(wsScheme + '://' + window.location.host + '/ws/chat/' + channelName + '/');

    const messages = document.getElementById('messages');
    const form = document.getElementById('chat-form');
    const input = document.getElementById('msg-input');
    const roomName = "{{ room_name }}";
    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/');


    function addMessage(m) {
      const el = document.createElement('div');
      el.className = 'chat-message';
      el.innerHTML = '<strong>' + (m.user || 'Anon') + ':</strong> ' + escapeHtml(m.content) +
                     '<div class="text-muted small">' + new Date(m.created_at).toLocaleString() + '</div>';
      messages.appendChild(el);
      messages.scrollTop = messages.scrollHeight;
    }

    function escapeHtml(unsafe) {
      return unsafe
           .replace(/&/g, "&amp;")
           .replace(/</g, "&lt;")
           .replace(/>/g, "&gt;")
           .replace(/"/g, "&quot;")
           .replace(/'/g, "&#039;");
    }

    socket.onopen = function(e) {
      console.log("Connected to chat socket");
    }

    socket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      if (data.type === "recent_messages") {
        data.messages.forEach(m => addMessage(m));
      } else if (data.type === "message") {
        addMessage(data.message);
      }
    }

    socket.onclose = function(e) {
      console.log('Socket closed', e);
    }

    form.addEventListener('submit', function(e){
      e.preventDefault();
      const content = input.value.trim();
      if (!content) return;
      socket.send(JSON.stringify({type: 'message', content: content}));
      input.value = '';
    });
  })();


const roomName = "{{ room_name }}";
const chatSocket = new WebSocket(
      'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
  );

  chatSocket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      document.querySelector('#chat-log').value += (data.message + '\n');
  };

  document.querySelector('#chat-message-submit').onclick = function(e) {
      const input = document.querySelector('#chat-message-input');
      chatSocket.send(JSON.stringify({'message': input.value}));
      input.value = '';
  };