function init() {
    window.chart.initChart();
    let period = 1;
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
            window.chart.updateCandlSeries(candles, period);
        } catch {
            ui.updateStatus('Failed to load history', 'status-disconnected');
        }
    });

    document.getElementById('period-select').addEventListener('change', async (e) => {
        const value = e.target.value;
        let periodDD = 1;
        if (value === '1 second') periodDD = 1;
        else if (value === '5 seconds') periodDD = 5;
        else if (value === '15 seconds') periodDD = 15;
        else if (value === '30 seconds') periodDD = 30;
        console.log('Selected period:', periodDD);
        period = periodDD;
        try {
            const candles = await api.fetchHistory(100, period);
            window.chart.updateCandlSeries(candles, period); 
        } catch {
            ui.updateStatus('Failed to load history', 'status-disconnected');
        }
    });
}

document.addEventListener('DOMContentLoaded', init);