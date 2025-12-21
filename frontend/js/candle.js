let chartInstance = null;
let candlestickSeriesInstance = null;
let candlestickVolumeInstance = null;

function initChart() {
  const { createChart, CandlestickSeries, HistogramSeries } = window.LightweightCharts;
  const chartOptions = { layout: 
    { 
     textColor: 'black', background: 
      { type: 'solid', color: 'white' } 
    },
      timeScale: { timeVisible: true }
  };
  chartInstance = createChart(document.getElementById('chart-div'), chartOptions);
  candlestickSeriesInstance = chartInstance.addSeries(CandlestickSeries, 
    { 
      upColor: '#26a69a', 
      downColor: '#ef5350',
       borderVisible: false, 
       wickUpColor: '#26a69a', 
       wickDownColor: '#ef5350'
    }
  );
  candlestickVolumeInstance = chartInstance.addSeries(HistogramSeries, 
    {
      priceFormat: { type: 'volume' },
      color: '#26a69a', base: 0
    }
  );
  candlestickVolumeInstance.moveToPane(2);
  return chartInstance;
}

function emptyChart() {
  if (candlestickSeriesInstance) {
    candlestickSeriesInstance.setData([]);
    candlestickVolumeInstance.setData([]);
  } 
}

function addCandleData(data) {
  if (candlestickSeriesInstance) {
    const candleData = Array.isArray(data) ? data : [data];
    const currentCandleData = candlestickSeriesInstance.data();
    const combinedCandleData = currentCandleData.concat(candleData);
    const currentVolumeData = candlestickVolumeInstance.data();
    const combinedVolumeData = currentVolumeData.concat(candleData.map(d => ({ time: d.time, value: d.volume })));
    candlestickSeriesInstance.setData(combinedCandleData);
    candlestickVolumeInstance.setData(combinedVolumeData);
  }
}

function updateCandle(data) {
  if (!candlestickSeriesInstance) return;

  const normalize = (d) => ({
    time: (typeof d.time === 'string') ? d.time : Math.floor(Number(d.time)),
    open: Number(d.open),
    high: Number(d.high),
    low: Number(d.low),
    close: Number(d.close),
    volume: Number(d.volume) || 0
  });

  const candle = Array.isArray(data) ? data[data.length - 1] : data;
  if (!candle) return;
  const c = normalize(candle);

  const existing = candlestickSeriesInstance.data() || [];
  if (existing.length === 0) {
    candlestickSeriesInstance.setData([c]);
    if (candlestickVolumeInstance) candlestickVolumeInstance.setData([{ time: c.time, value: c.volume }]);
  } else {
    // realistic behavior: update only the last/current candle
    candlestickSeriesInstance.update(c);
    if (candlestickVolumeInstance) candlestickVolumeInstance.update({ time: c.time, value: c.volume });
  }


}

window.chart = { initChart, addCandleData, updateCandle, emptyChart };