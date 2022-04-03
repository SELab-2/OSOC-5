<!-- 
  Props:
    glow-color (optional, default: lighter color than button): color of the glow on hover (e.g. 'purple', '#00FFB5', 'primary').
    glow-size (optional, default: 100px): size of the glow on hover (e.g. '100px') .
    glow-scale (optional, default: 1): scale of the glow when clicked.
    disable-glow: disables the glow effect.
    disable-click: disables the scale effect on click.
    shadow-color: color of the shadow.
-->

<template>
  <q-btn
    ref="glowbutton"
    :class="this.disableGlow ? '' : 'bttn'"
    @mousemove="mousemove"
    :color="color"
    :style="this.disableGlow ? '' : glowStyle"
    ripple="false"
  >
  </q-btn>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { colors } from 'quasar'
export default {
  name: 'btn',
  props: {
    'glowColor': String,
    'glowSize': String,
    'glowScale': Number,
    'disableGlow': Boolean,
    'color': String,
    'shadowColor': String,
    'disableClick': Boolean
  },
  mounted() {
    
    // This class produces a tint change on hover, but is unwanted for the glow button.
    this.$refs.glowbutton.$el.classList.remove('q-hoverable')
    this.$refs.glowbutton.$el.removeChild(this.$refs.glowbutton.$el.children[0])
  },
  data() {
    return {
      x: ref(0),
      y: ref(0)
    }
  },
  computed: {
    glow() {
      var color: String;
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
        '--color': this.glow,
        '--shadow-color': this.shadowColor ? this.shadowColor : 'transparent',
        '--button-scale': this.disableClick ? 1 : 0.98,
        '--shadow-scale': this.disableClick ? 1 : 1.5
      }
    }
  },
  methods: {
    mousemove(e: MouseEvent) {
      const test = e.target.getBoundingClientRect()
      this.x = e.clientX - test.left
      this.y = e.clientY - test.top
    },
  },
}
</script>



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
  --spread: 1;
  box-shadow: 0px 8px 20px calc(-4px * var(--spread)) var(--shadow-color);
  /* Scale effect on click */
  --press: 1;
  transform: scale(var(--press));
  transition-duration: 0.2s;
  transition-property: transform box-shadow;
  transition-timing-function: cubic-bezier(0.22, 1, 0.32, 1);
  &:active {
    --press: var(--button-scale);
    --spread: var(--shadow-scale);
  }
}


</style>
