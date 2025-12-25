let chartInstance = null;
let candlestickSeriesInstance = null;
let candlestickVolumeInstance = null;
let candleSeriesData = [];
let volumeSeriesData = [];

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
    candleSeriesData = [];
    volumeSeriesData = [];
  } 
}

function updateCandlSeries(data, period = 1) {
  if (data.length != undefined) {
    emptyChart();
    candleSeriesData = data ;
    volumeSeriesData = data.map(d => ({ time: d.time, value: d.volume }) );
  } else {
    candleSeriesData.push(data);
    volumeSeriesData.push({ time: data.time, value: data.volume } );
  }
  updateChart(data, period);
}

function updateChart(data, period = 1) {
  if (data.length > 1) {
    aggregateToPeriod(period);
  } else {
    aggregateLastCandleToPeriod(data, period);
  }
}

function aggregateToPeriod(period) {
  if (period <= 1) {
    candlestickSeriesInstance.setData(candleSeriesData);
    candlestickVolumeInstance.setData(volumeSeriesData.map(d => ({ time: d.time, value: d.value })));
    return;
  } else {
    const aggregatedCandles = [];
    const aggregatedVolumes = [];
    for (let i = period - candleSeriesData[0].time % period; i < candleSeriesData.length; i += period) {
      const chunk = candleSeriesData.slice(i, i + period);
      const open = chunk[0].open;
      const close = chunk[chunk.length - 1].close;
      const high = Math.max(...chunk.map(c => c.high));
      const low = Math.min(...chunk.map(c => c.low));
      const volume = chunk.reduce((sum, c) => sum + Number(c.volume), 0);
      const time = Math.floor(Number(chunk[0].time) / period) * period;
      aggregatedCandles.push({ time, open, high, low, close });
      aggregatedVolumes.push({ time, value: volume });
    }
    candlestickSeriesInstance.setData(aggregatedCandles);
    candlestickVolumeInstance.setData(aggregatedVolumes);
    return
  }
}

function aggregateLastCandleToPeriod(incoming, period) {
  const bucketStartTime = Math.floor(Number(incoming.time) / period) * period;
  let bucketCandles = candleSeriesData.filter(c => Math.floor(Number(c.time) / period) * period === bucketStartTime);
  if (bucketCandles.length === 0) {
    return;
  } else {
    const open = bucketCandles[0].open;
    const close = bucketCandles[bucketCandles.length - 1].close;
    const high = Math.max(...bucketCandles.map(c => c.high));
    const low = Math.min(...bucketCandles.map(c => c.low));
    const volume = bucketCandles.reduce((sum, c) => sum + Number(c.volume), 0);
    const aggregatedCandle = { 
      time: bucketStartTime, 
      open: open,
      high: high,
      low: low,
      close: close
    };
    const aggregatedVolume = { time: bucketStartTime, value: volume };
    candlestickSeriesInstance.update(aggregatedCandle);
    candlestickVolumeInstance.update(aggregatedVolume);
  }
}


window.chart = { initChart, updateCandlSeries, updateChart, emptyChart, aggregateToPeriod, getCandleData: () => candleSeriesData, getVolumeData: () => volumeSeriesData };