function init() {
    window.chart.initChart();
    document.getElementById('connect-btn').addEventListener('click', () => {
    if (window._ws) return;
        window._ws = api.connectWebSocket((candle) => {
            ui.displayLatestCandle(candle);
            window.chart.addCandleData([candle]);
            window.chart.updateCandle(candle);
        }, ui.updateStatus);
    });

    document.getElementById('history-btn').addEventListener('click', async () => {
        try {
            const candles = await api.fetchHistory(100);
            window.chart.addCandleData(candles);  // Add to chart
            // ui.renderHistory(candles);
        } catch {
            // ui.renderHistory([]);
            ui.updateStatus('Failed to load history', 'status-disconnected');
        }
    });

}

document.addEventListener('DOMContentLoaded', init);