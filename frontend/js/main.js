function init() {
    window.chart.initChart();
    const period = 5
    document.getElementById('connect-btn').addEventListener('click', () => {
    if (window._ws) return;
        window._ws = api.connectWebSocket((candle) => {
            ui.displayLatestCandle(candle);
            window.chart.updateCandlSeries(candle, period);
        }, ui.updateStatus);
    });

    document.getElementById('history-btn').addEventListener('click', async () => {
        try {
            const candles = await api.fetchHistory(100, period);
            window.chart.updateCandlSeries(candles, period);  // Add to chart
            // ui.renderHistory(candles);
        } catch {
            // ui.renderHistory([]);
            ui.updateStatus('Failed to load history', 'status-disconnected');
        }
    });

}

document.addEventListener('DOMContentLoaded', init);