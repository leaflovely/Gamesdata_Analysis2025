<template>
  <div class="chart-container">
    <h2>用户评价比例</h2>
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
      
      // 计算评价比例
      const totalPositive = props.gameData.reduce((sum, game) => {
        return sum + (parseFloat(game['User Positive']) || 0);
      }, 0);
      
      const totalMixed = props.gameData.reduce((sum, game) => {
        return sum + (parseFloat(game['User Mixed']) || 0);
      }, 0);
      
      const totalNegative = props.gameData.reduce((sum, game) => {
        return sum + (parseFloat(game['User Negative']) || 0);
      }, 0);
      
      const total = totalPositive + totalMixed + totalNegative;
      
      const reviewData = [
        { value: totalPositive, name: '正面评价' },
        { value: totalMixed, name: '中立评价' },
        { value: totalNegative, name: '负面评价' }
      ];

      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: ['正面评价', '中立评价', '负面评价']
        },
        series: [
          {
            name: '评价比例',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: reviewData,
            color: ['#67C23A', '#E6A23C', '#F56C6C']
          }
        ]
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
