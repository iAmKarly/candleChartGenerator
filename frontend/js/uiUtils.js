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

function renderHistory(candles) {
  historyListEl.innerHTML = '';
  if (!candles || !candles.length) {
    historyListEl.innerHTML = '<li>No history loaded.</li>';
    return;
  }
  candles.forEach(c => {
    const li = document.createElement('li');
    li.textContent = `Time: ${c.time}, Open: ${c.open}, High: ${c.high}, Low: ${c.low}, Close: ${c.close}, Volume: ${c.volume}`;
    historyListEl.appendChild(li);
  });
}

window.ui = { updateStatus, displayLatestCandle, renderHistory };