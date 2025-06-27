<template>
  <div class="chart-container">
    <h2>开发商/发行商游戏数量统计</h2>
    <div ref="chart" style="width: 100%; height: 500px;"></div>
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
      
      // 统计开发商和发行商
      const developerCounts = {};
      const publisherCounts = {};
      
      props.gameData.forEach(game => {
        if (game.Developer) {
          developerCounts[game.Developer] = (developerCounts[game.Developer] || 0) + 1;
        }
        if (game.Publisher) {
          publisherCounts[game.Publisher] = (publisherCounts[game.Publisher] || 0) + 1;
        }
      });
      
      // 转换为数组并排序
      const developerData = Object.entries(developerCounts)
        .map(([name, value]) => ({ name, value }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 10);
      
      const publisherData = Object.entries(publisherCounts)
        .map(([name, value]) => ({ name, value }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 10);

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['开发商', '发行商']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '游戏数量'
        },
        yAxis: {
          type: 'category',
          data: developerData.map(item => item.name),
          axisLabel: {
            fontSize: 12
          }
        },
        series: [
          {
            name: '开发商',
            type: 'bar',
            data: developerData.map(item => item.value),
            itemStyle: {
              color: '#5470C6'
            },
            label: {
              show: true,
              position: 'right'
            }
          },
          {
            name: '发行商',
            type: 'bar',
            data: publisherData.map(item => item.value),
            itemStyle: {
              color: '#91CC75'
            },
            label: {
              show: true,
              position: 'right'
            }
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
  margin-bottom: 40px;
  font-size: 18px;
  color: #333;
}
</style>
