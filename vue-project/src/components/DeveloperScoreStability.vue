<template>
  <div class="chart-container">
    <h2>开发商评分稳定性</h2>
    <div ref="chart" style="width: 100%; height: 600px;"></div>
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
      
      // 按开发商分组评分数据
      const developerScores = {};
      props.gameData.forEach(game => {
        if (game.Developer && game['Meta Score']) {
          if (!developerScores[game.Developer]) {
            developerScores[game.Developer] = [];
          }
          developerScores[game.Developer].push(game['Meta Score']);
        }
      });
      
      // 筛选至少有3个游戏的开发商
      const validDevelopers = Object.entries(developerScores)
        .filter(([_, scores]) => scores.length >= 3)
        .sort((a, b) => b[1].length - a[1].length)
        .slice(0, 10); // 只取前10个
      
      // 计算箱线图数据
      const boxplotData = validDevelopers.map(([developer, scores]) => {
        scores.sort((a, b) => a - b);
        const q1 = calculatePercentile(scores, 25);
        const median = calculatePercentile(scores, 50);
        const q3 = calculatePercentile(scores, 75);
        const min = Math.min(...scores);
        const max = Math.max(...scores);
        
        return {
          name: developer,
          value: [min, q1, median, q3, max],
          itemStyle: {
            color: getRandomColor()
          }
        };
      });
      
      function calculatePercentile(arr, p) {
        const index = (arr.length - 1) * p / 100;
        const lower = Math.floor(index);
        const upper = Math.ceil(index);
        if (lower === upper) return arr[lower];
        return arr[lower] + (arr[upper] - arr[lower]) * (index - lower);
      }
      
      function getRandomColor() {
        const colors = [
          '#5470C6', '#91CC75', '#FAC858', '#EE6666', '#73C0DE',
          '#3BA272', '#FC8452', '#9A60B4', '#EA7CCC', '#60C0DD'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
      }

      const option = {
        tooltip: {
          trigger: 'item',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '15%'
        },
        xAxis: {
          type: 'category',
          data: boxplotData.map(item => item.name),
          axisLabel: {
            interval: 0,
            rotate: 45
          },
          boundaryGap: true,
          nameGap: 30
        },
        yAxis: {
          type: 'value',
          name: 'Meta评分',
          min: 0,
          max: 100,
          splitArea: {
            show: false
          }
        },
        series: [
          {
            name: '评分分布',
            type: 'boxplot',
            data: boxplotData,
            tooltip: {
              formatter: function(param) {
                return [
                  '开发商: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                  '最大值: ' + param.value[4] + '<br>',
                  '上四分位数: ' + param.value[3] + '<br>',
                  '中位数: ' + param.value[2] + '<br>',
                  '下四分位数: ' + param.value[1] + '<br>',
                  '最小值: ' + param.value[0]
                ].join('');
              }
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
  margin-bottom: 20px;
  font-size: 18px;
  color: #333;
}
</style>
