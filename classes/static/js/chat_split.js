(function () {
  const channelsList = document.getElementById("channelsList");
  const chatBox = document.getElementById("chatBox");
  const roomTitle = document.getElementById("roomTitle");
  const msgInput = document.getElementById("messageInput");
  const sendBtn = document.getElementById("sendBtn");

  let currentRoom = "{{ current.name|default:'' }}";
  let socket = null;

  // --- Fetch messages dynamically when switching channels ---
  async function loadMessages(roomName) {
    try {
      const response = await fetch(`/chat/api/messages/${roomName}/`);
      if (!response.ok) throw new Error("Failed to fetch messages");
      const data = await response.json();

      chatBox.innerHTML = "";
      data.messages.forEach((msg) => {
        appendMessage(msg.username, msg.content, msg.timestamp);
      });
    } catch (err) {
      console.error("Error loading messages:", err);
    }
  }

  // --- Handle clicking on channel list ---
  channelsList.addEventListener("click", (e) => {
    const item = e.target.closest(".channel-item");
    if (!item) return;

    const roomName = item.dataset.name;
    if (roomName === currentRoom) return; // no need to reload same room

    document.querySelectorAll(".channel-item").forEach((el) => {
      el.classList.toggle("active", el.dataset.name === roomName);
    });

    joinRoom(roomName);
  });

  // --- Switch to a room ---
  function joinRoom(roomName) {
    if (!roomName) return;
    currentRoom = roomName;
    roomTitle.textContent = roomName;
    chatBox.innerHTML = "";

    // Update URL (optional, just for user experience)
    history.replaceState(null, "", `?room_name=${encodeURIComponent(roomName)}`);

    // Load messages dynamically
    loadMessages(roomName);

    // Connect to WebSocket
    connectSocket(roomName);
  }

  // --- WebSocket setup ---
  function connectSocket(roomName) {
    if (socket) {
      try {
        socket.close();
      } catch (e) {}
      socket = null;
    }

    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = `${protocol}://${window.location.host}/ws/chat/${encodeURIComponent(
      roomName
    )}/`;
    socket = new WebSocket(wsUrl);

    socket.onopen = () => console.log("✅ WebSocket connected:", wsUrl);
    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      appendMessage(data.username, data.message, data.timestamp);
    };
    socket.onclose = () => console.log("❌ WebSocket closed");
  }

  // --- Append message to chat ---
  function appendMessage(username, text, timestamp) {
    const div = document.createElement("div");
    div.className = "message";
    div.innerHTML = `
      <div><strong>${username || "Anonymous"}</strong></div>
      <div>${text}</div>
      <div class="meta">${timestamp}</div>
    `;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // --- Send message through WebSocket ---
  sendBtn.addEventListener("click", () => {
    const text = msgInput.value.trim();
    if (!text || !currentRoom || !socket || socket.readyState !== WebSocket.OPEN) return;

    const payload = {
      message: text,
      username: "{{ request.user.username|default:'Anonymous' }}",
    };
    socket.send(JSON.stringify(payload));
    msgInput.value = "";
  });

  msgInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendBtn.click();
    }
  });

  // --- Initial load ---
  if (currentRoom) {
    joinRoom(currentRoom);
  }
})();
