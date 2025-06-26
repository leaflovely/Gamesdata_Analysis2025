<template>
  <div class="chart-container">
    <h2>游戏类型分布</h2>
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
      
      // 统计游戏类型
      const genreCounts = {};
      props.gameData.forEach(game => {
        if (game.Genres) {
          const genres = game.Genres.split(',').map(g => g.trim());
          genres.forEach(genre => {
            genreCounts[genre] = (genreCounts[genre] || 0) + 1;
          });
        }
      });
      
      // 转换为数组并按数量排序
      const genreData = Object.entries(genreCounts)
        .map(([name, value]) => ({ name, value }))
        .sort((a, b) => b.value - a.value);

      // 只显示前10个类型，其他归为"其他"
      const topGenres = genreData.slice(0, 10);
      if (genreData.length > 10) {
        const otherCount = genreData.slice(10).reduce((sum, genre) => sum + genre.value, 0);
        topGenres.push({ name: '其他', value: otherCount });
      }

      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right: 0,
          top: 70,
          data: topGenres.map(item => item.name)
        },
        series: [
          {
            name: '游戏类型',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['35%', '45%'],
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
            data: topGenres
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
