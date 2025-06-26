<template>
  <div class="chart-container">
    <h2>Meta评分分布</h2>
    <div ref="chart" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import { ref, onMounted,watch } from 'vue';

export default {
  props: {
    gameData: {
      type: Array,
      required: true
    }
  },
setup(props) {
  const chart = ref(null);
  let chartInstance = null;

  const renderChart = () => {
    if (!props.gameData || props.gameData.length === 0) return;
    if (!chartInstance) chartInstance = echarts.init(chart.value);

    const scoreRanges = [
      { min: 96, max: 100, label: '95-100' },
      { min: 90, max: 95, label: '90-95' },
      { min: 80, max: 89, label: '80-89' },
      { min: 70, max: 79, label: '70-79' },
      { min: 60, max: 69, label: '60-69' },
      { min: 0, max: 60, label: '0-60' }
    ];
    const scoreCounts = scoreRanges.map(range =>
      props.gameData.filter(game =>
        Number(game['Meta Score']) >= range.min && Number(game['Meta Score']) <= range.max
      ).length
    );
    const option = {
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      xAxis: { type: 'category', data: scoreRanges.map(r => r.label), axisLabel: { fontSize: 12 } },
      yAxis: { type: 'value', name: '游戏数量' },
      series: [{
        data: scoreCounts,
        type: 'bar',
        showBackground: true,
        itemStyle: { color: '#5470C6' },
        label: { show: true, position: 'top' }
      }]
    };
    chartInstance.setOption(option);
    window.addEventListener('resize', () => chartInstance.resize());
  };

  onMounted(renderChart);
  watch(() => props.gameData, renderChart, { deep: true });

  return { chart };
}
};
</script>

<style scoped>
.chart-container {
  margin: 20px 0;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  font-size: 18px;
  color: #333;
}
</style>
