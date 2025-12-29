const API_URL_WS = 'ws://localhost:8000/ws';
const API_URL_HTTP = 'http://localhost:8000';
let currentController = null;

function connectWebSocket(onMessage, onStatus) {
  let socket = new WebSocket(API_URL_WS);
  socket.onopen = () => onStatus('Connected', 'status-connected');
  socket.onmessage = (e) => onMessage(JSON.parse(e.data));
  socket.onclose = () => onStatus('Disconnected', 'status-disconnected');
  socket.onerror = () => onStatus('Error', 'status-disconnected');
  return socket;
}

function startGenerator() {
  return fetch(`${API_URL_HTTP}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }).then(res => res.ok ? res.json() : Promise.reject(res.statusText));
}

function stopGenerator() {
  return fetch(`${API_URL_HTTP}/stop`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }).then(res => res.ok ? res.json() : Promise.reject(res.statusText));
}

async function fetchHistory(limit = 100, periodSeconds = 1) {
  const res = await fetch(`${API_URL_HTTP}/history?limit=${limit*periodSeconds}`);
  return res.ok ? res.json() : Promise.reject(res.statusText);
}

async function setTradesPerSecond(tps) {
  if (currentController) {
    currentController.abort();
  }
  currentController = new AbortController();
  const { signal } = currentController;
  
  try {
  const res = await fetch(`${API_URL_HTTP}/config/trades_per_second?numTradesPerSecond=${tps}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    signal: signal
  });
  if (!res.ok) throw new Error(res.statusText);
    return await res.json();
  } catch (err) {
    if (err.name === 'AbortError') {
      console.log('Previous request cancelled');
    } else {
      throw err;
    }
  } finally {
    if (currentController?.signal === signal) {
      currentController = null;
    }
  }
}

async function setMakerTakerRatio(ratio) {
  if (currentController) {
    currentController.abort();
  }
  currentController = new AbortController();
  const { signal } = currentController;
  
  try {
  const res = await fetch(`${API_URL_HTTP}/config/maker_taker_ratio?ratio=${ratio}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    signal: signal
  });
  if (!res.ok) throw new Error(res.statusText);
    return await res.json();
  } catch (err) {
    if (err.name === 'AbortError') {
      console.log('Previous request cancelled');
    } else {
      throw err;
    }
  } finally {
    if (currentController?.signal === signal) {
      currentController = null;
    }
  }
}

window.api = { connectWebSocket, fetchHistory, setTradesPerSecond, setMakerTakerRatio , startGenerator, stopGenerator };
