<template>
  <div ref="dom" class="charts chart-line"></div>
</template>

<script>
import echarts from 'echarts'
import tdTheme from './theme.json'
import { on, off } from '@/libs/tools'
echarts.registerTheme('tdTheme', tdTheme)
export default {
  name: 'ChartLine',
  props: {
    value: Object,
    text: String,
    subtext: String,
    signal: Boolean
  },
  computed: {
    data () {
      return this.value
    }
  },
  data () {
    return {
      dom: null
    }
  },
  watch: {
    signal () {
      if (this.signal) {
        this.genChart()
      }
      this.$emit('closeSignal')
    }
  },
  methods: {
    resize () {
      this.dom.resize()
    },
    genChart () {
      this.$nextTick(() => {
        let xAxisData = Object.keys(this.data)
        let seriesData = Object.values(this.data)
        let option = {
          title: {
            text: this.text,
            subtext: this.subtext,
            x: 'center'
          },
          xAxis: {
            type: 'category',
            data: xAxisData
          },
          yAxis: {
            type: 'value'
          },
          series: [{
            name: 'cpu_total',
            data: seriesData,
            type: 'line'
          }]
        }
        this.dom = echarts.init(this.$refs.dom, 'tdTheme')
        this.dom.setOption(option, true)
      })
    }
  },
  mounted () {
    this.$nextTick(() => {
      let xAxisData = Object.keys(this.data)
      let seriesData = Object.values(this.data)
      let option = {
        title: {
          text: this.text,
          subtext: this.subtext,
          x: 'center'
        },
        xAxis: {
          type: 'category',
          data: xAxisData
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          name: 'cpu_total',
          data: seriesData,
          type: 'line'
        }]
      }
      this.dom = echarts.init(this.$refs.dom, 'tdTheme')
      this.dom.setOption(option)
      on(window, 'resize', this.resize)
    })
  },
  beforeDestroy () {
    off(window, 'resize', this.resize)
  }
}
</script>
