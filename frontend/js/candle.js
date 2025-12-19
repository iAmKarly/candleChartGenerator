let chartInstance = null;
let candlestickSeriesInstance = null;

function initChart() {
  const { createChart, CandlestickSeries } = window.LightweightCharts;
  const chartOptions = { layout: { textColor: 'black', background: { type: 'solid', color: 'white' } } };
  chartInstance = createChart(document.getElementById('chart-div'), chartOptions);
  candlestickSeriesInstance = chartInstance.addSeries(CandlestickSeries, 
    { upColor: '#26a69a', downColor: '#ef5350', borderVisible: false, wickUpColor: '#26a69a', wickDownColor: '#ef5350' }
  );
  return chartInstance;
}

function addCandleData(data) {
  if (candlestickSeriesInstance) {
    const currentData = candlestickSeriesInstance.data();
    const combinedData = currentData.concat(data);
    if (combinedData.length > 100) {
        combinedData.splice(0, combinedData.length - 100);
    }
    candlestickSeriesInstance.setData(combinedData);
    chartInstance.timeScale().fitContent();
  }
}

function updateCandle(candle) {
  if (candlestickSeriesInstance) {
    candlestickSeriesInstance.update(candle);
  }
}

window.chart = { initChart, addCandleData, updateCandle };