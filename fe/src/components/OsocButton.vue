<!-- 
  Props:
    glow-color: color of the glow on hover (e.g. 'purple', '#00FFB5'). Quasar-specific colors (e.g. 'primary') are not supported.
    glow-size: size of the glow on hover (e.g. '100px') 
-->

<template>
  <q-btn
    class="bttn box"
    @mousemove="mousemove"
    :color="color"
    :style="glowStyle"
  >
  </q-btn>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { colors } from 'quasar'
export default {
  name: 'btn',
  props: ['glowColor', 'glowSize', 'glowScale', 'color'],
  data() {
    return {
      x: ref(0),
      y: ref(0)
    }
  },
  computed: {
    glow() {
      var color;
      if (this.glowColor) {
        color = (colors.getPaletteColor(this.glowColor) !== "#000000") ? colors.getPaletteColor(this.glowColor) : this.glowColor
      } else if (!this.color) {
        color = 'lightgrey'
      } else if (colors.getPaletteColor(this.color) === "#000000") {
        color = colors.lighten(this.color, 40)
      } else {
        color = colors.lighten(colors.getPaletteColor(this.color), 40)
      }
      return color
    },
    glowStyle() {
      return {
        '--x': `${this.x}px`,
        '--y': `${this.y}px`,
        '--size': (this.glowSize ? this.glowSize : '100px'),
        '--prop-scale': (this.glowScale ? this.glowScale : 1),
        '--color': this.glow
      }
    }
  },
  methods: {
    mousemove(e) {
      const test = e.target.getBoundingClientRect()
      this.x = e.clientX - test.left
      this.y = e.clientY - test.top
    },
  },
}
</script>

<style scoped>
  :deep(.q-focus-helper) {
    background-color: inherit !important 
  }
</style>

<style lang="scss">

.bttn {
  -webkit-transform: translate3d(0, 0, 0); /* Fix for webkit artifacts */
  position: relative;
  cursor: pointer;
  overflow: hidden;
  
  span {
    position: relative;
    pointer-events: none;
  }

  &::before {
    --scale: 0;
    --opacity: 0;

    content: '';
    position: absolute;
    left: calc(var(--x) - var(--size) / 2) !important;
    top: calc(var(--y) - var(--size) / 2) !important;
    width: var(--size);
    height: var(--size);
    background: radial-gradient(circle closest-side, var(--color), transparent);
    transform: scale(var(--scale));
    opacity: var(--opacity);
    
    transition-duration: 0.8s;
    transition-timing-function: cubic-bezier(0.22, 1, 0.32, 1);
  }

  &:hover::before {
    --scale: 1;
    --opacity: 1;
    transition-property: transform, opacity;
  }
    
  &:active::before {
    --scale: calc(3 * var(--prop-scale));
    --opacity: 1;
    transition-property: transform; /* opacity is excluded here due to webkit artifacts (and is not really visible after all) */
  }
}


</style>
