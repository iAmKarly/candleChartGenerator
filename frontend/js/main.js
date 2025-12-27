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
        period = periodDD;
        try {
            const candles = await api.fetchHistory(100, period);
            window.chart.updateCandlSeries(candles, period); 
            console.log('Updated chart with new period data', period);
        } catch {
            ui.updateStatus('Failed to load history', 'status-disconnected');
        }
    });

    document.getElementById('trades-per-second').addEventListener('change', async(e) => {
        const tps = parseInt(e.target.value);
        window.chart.emptyChart();
        await window.api.setTradesPerSecond(tps);
        console.log('Updated trades per second to:', tps);
    });

    document.getElementById('maker-taker-ratio').addEventListener('change', async (e) => {
        const ratio = parseFloat(e.target.value);
        window.chart.emptyChart();
        await window.api.setMakerTakerRatio(ratio);
        console.log('Updated maker-taker ratio to:', ratio);
    });
}

document.addEventListener('DOMContentLoaded', init);