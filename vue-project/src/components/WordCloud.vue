<script>
import { computed } from 'vue';
import * as d3 from 'd3';
import cloud from 'd3-cloud';
import { scaleLinear } from 'd3-scale';

export default {
  props: {
    gameData: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    // 生成词云数据
    const wordData = computed(() => {
      const words = [];
      const publisherMap = {};
      const genreMap = {};
      const platformMap = {};
      const nameMap = {};
      const reviewMap = {
        '用户好评': 0,
        '媒体好评': 0,
        '褒贬不一': 0,
        '人气游戏': 0,
        '冷门佳作': 0,
        '高分神作': 0,
        '差评较多': 0
      };

      props.gameData.forEach(game => {
        // 处理发行商
        if (game.Publisher) {
          publisherMap[game.Publisher] = (publisherMap[game.Publisher] || 0) + 1;
        }

        // 处理游戏类别
        if (game.Genres) {
          game.Genres.split(/[,，;]/).forEach(genre => {
            const trimmed = genre.trim();
            if (trimmed) {
              genreMap[trimmed] = (genreMap[trimmed] || 0) + 1;
            }
          });
        }

        // 处理游戏平台
        if (game.Platforms) {
          game.Platforms.split(/[,，;]/).forEach(platform => {
            const trimmed = platform.trim();
            if (trimmed) {
              platformMap[trimmed] = (platformMap[trimmed] || 0) + 1;
            }
          });
        }

        // 处理中文名（加权）
        if (game['Translated Name']) {
          const weight = (game['User Score'] || 0) * 10 + (game['User Reviews'] || 0) / 100;
          nameMap[game['Translated Name']] = (nameMap[game['Translated Name']] || 0) + weight;
        }

        // 处理评价词
        if (game['User Score'] >= 8) reviewMap['用户好评']++;
        if (game['Meta Score'] >= 80) reviewMap['媒体好评']++;
        if (game['User Score'] >= 5 && game['User Score'] < 8) reviewMap['褒贬不一']++;
        if (game['User Reviews'] >= 1000) reviewMap['人气游戏']++;
        if (game['User Score'] >= 8 && game['User Reviews'] < 100) reviewMap['冷门佳作']++;
        if (game['User Score'] >= 9 && game['Meta Score'] >= 90) reviewMap['高分神作']++;
        if (game['User Score'] < 5) reviewMap['差评较多']++;
      });

      // 合并所有词
      Object.entries(publisherMap).forEach(([text, value]) => {
        words.push({ text, value: value * 5 }); // 发行商权重更高
      });

      Object.entries(genreMap).forEach(([text, value]) => {
        words.push({ text, value });
      });

      Object.entries(platformMap).forEach(([text, value]) => {
        words.push({ text, value });
      });

      Object.entries(nameMap).forEach(([text, value]) => {
        words.push({ text, value: Math.sqrt(value) * 1.5 }); // 对中文名进行加权处理
      });

      Object.entries(reviewMap).forEach(([text, value]) => {
        if (value > 0) words.push({ text,value: value * 0.5 }); // 评价词权重较低
      });

      return words;
    });

    return { wordData };
  },
  mounted() {
    this.renderWordCloud();
  },
  watch: {
    gameData: {
      handler() {
        this.renderWordCloud();
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    renderWordCloud() {
      const container = this.$refs.wordCloud;
      if (!container || !this.wordData.length) return;

      // 清除之前的词云
      container.innerHTML = '';

      const width = container.clientWidth;
      const height = container.clientHeight;

      // 创建颜色比例尺
      const color = scaleLinear()
        .domain([0, d3.max(this.wordData, d => d.value)])
        .range(['#3182bd', '#6baed6', '#9ecae1', '#c6dbef']);

      // 创建词云布局
      const layout = cloud()
        .size([width, height])
        .words(this.wordData)
        .padding(5)
        .rotate(() => (Math.random() > 0.5 ? 0 : 90))
        .fontSize(d => Math.sqrt(d.value) * 10)
        .on('end', draw);

      layout.start();

      function getRandomColor() {
        // 生成明亮的随机色
        const h = Math.floor(Math.random() * 260);
        const s = 60 + Math.random() * 30;
        const l = 50 + Math.random() * 20;
        return `hsl(${h},${s}%,${l}%)`;
      }

      function draw(words) {
        const svg = d3.select(container)
          .append('svg')
          .attr('width', width)
          .attr('height', height)
          .append('g')
          .attr('transform', `translate(${width/2},${height/2})`);

        svg.selectAll('text')
          .data(words)
          .enter()
          .append('text')
          .style('font-size', d => `${d.size}px`)
          .style('fill', getRandomColor)
          .style('text-shadow', '2px 2px 8px rgba(0,0,0,0.15)')
          .attr('text-anchor', 'middle')
          .attr('transform', d => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
          .text(d => d.text);
      }
    }
  }
};
</script>

<template>
  <div class="word-cloud-container">
    <h3>游戏关键词云</h3>
    <div ref="wordCloud" class="word-cloud"></div>
  </div>
</template>

<style scoped>
.word-cloud-container {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.word-cloud-container h3 {
  text-align: center;
  margin-bottom: 15px;
  color: #333;
}

.word-cloud {
  width: 100%;
  height: 400px;
  margin: 0 auto;
}
</style>
