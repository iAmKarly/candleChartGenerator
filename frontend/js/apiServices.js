const API_URL_WS = 'ws://localhost:8000/ws';
const API_URL_HTTP = 'http://localhost:8000';

function connectWebSocket(onMessage, onStatus) {
  let socket = new WebSocket(API_URL_WS);
  socket.onopen = () => onStatus('Connected', 'status-connected');
  socket.onmessage = (e) => onMessage(JSON.parse(e.data));
  socket.onclose = () => onStatus('Disconnected', 'status-disconnected');
  socket.onerror = () => onStatus('Error', 'status-disconnected');
  return socket;
}

async function fetchHistory(limit = 100, periodSeconds = 1) {
  const res = await fetch(`${API_URL_HTTP}/history?limit=${limit*periodSeconds}`);
  return res.ok ? res.json() : Promise.reject(res.statusText);
}

window.api = { connectWebSocket, fetchHistory };