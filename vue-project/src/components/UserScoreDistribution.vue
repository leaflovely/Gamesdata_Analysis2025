<template>
  <div class="chart-container">
    <h2>用户评分分布</h2>
    <div ref="chart" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import { ref, onMounted, watch } from 'vue';

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
      
      // 计算评分分布
      const scoreRanges = [
        { min: 9, max: 10, label: '9-10' },
        { min: 8, max: 8.9, label: '8-8.9' },
        { min: 7, max: 7.9, label: '7-7.9' },
        { min: 6, max: 6.9, label: '6-6.9' },
        { min: 0, max: 5.9, label: '0-5.9' }
      ];
      
      const scoreCounts = scoreRanges.map(range => {
        return props.gameData.filter(game => 
          game['User Score'] >= range.min && game['User Score'] <= range.max
        ).length;
      });

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: scoreRanges.map(range => range.label),
          axisLabel: {
            fontSize: 12
          }
        },
        yAxis: {
          type: 'value',
          name: '游戏数量'
        },
        series: [{
          data: scoreCounts,
          type: 'bar',
          showBackground: true,
          itemStyle: {
            color: '#91CC75'
          },
          label: {
            show: true,
            position: 'top'
          }
        }]
      };

      chartInstance.setOption(option);
      
      window.addEventListener('resize', function() {
        chartInstance.resize();
      });
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
