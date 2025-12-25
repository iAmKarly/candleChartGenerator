const statusEl = document.getElementById('connection-status');
const outputEl = document.getElementById('candle-output');
const historyListEl = document.getElementById('history-list');

function updateStatus(text, className) {
  statusEl.textContent = text;
  statusEl.className = className;
}

function displayLatestCandle(candle) {
  outputEl.textContent = JSON.stringify(candle, null, 2);
}

window.ui = { updateStatus, displayLatestCandle };