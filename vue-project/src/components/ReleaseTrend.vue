<template>
  <div class="chart-container">
    <h2>游戏发行时间趋势</h2>
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
      
      // 提取年份并统计
      const yearCounts = {};
      props.gameData.forEach(game => {
        if (game['Release Date']) {
          const year = new Date(game['Release Date']).getFullYear();
          yearCounts[year] = (yearCounts[year] || 0) + 1;
        }
      });
      
      // 转换为数组并排序
      const years = Object.keys(yearCounts).sort();
      const counts = years.map(year => yearCounts[year]);

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: years,
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '游戏数量'
        },
        series: [{
          data: counts,
          type: 'line',
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: 'rgba(58, 77, 233, 0.8)'
              },
              {
                offset: 1,
                color: 'rgba(58, 77, 233, 0.1)'
              }
            ])
          },
          itemStyle: {
            color: '#3a4de9'
          },
          smooth: true
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
