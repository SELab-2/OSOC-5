<!-- 
  Props:
    glow-color (optional, default: lighter color than button): color of the glow on hover (e.g. 'purple', '#00FFB5', 'primary').
    glow-size (optional, default: 500px): size of the glow on hover (e.g. '1000px') .
    glow-scale (optional, default: 1): scale of the glow when clicked.
    disable-click: disables the scale effect on click.
    shadow-color: color of the shadow.
-->

<template>
  <q-btn
    unelevated
    :flat="flat"
    ref="glowbutton"
    class="bttn"
    :class="focusable ? 'focusable' : ''"
    @mousemove="mousemove"
    :color="color"
    :style="glowStyle"
  >
  <slot/>
  </q-btn>
</template>

<style scoped>
  :deep(.q-ripple) {
    display:none;
  }
</style>

<script lang="ts">
  import { ref, defineComponent } from 'vue'
  import { colors } from 'quasar'
export default defineComponent({
  name: 'btn',
  props: {
    'glowColor': String,
    'glowSize': {
      type: String,
      default: "500px"
    },
    'glowScale': {
      type: [Number,String],
      default: 1
    },
    'color': String,
    'shadowColor': {
      type: String,
      default: 'transparent'
    },
    'shadowStrength': {
      type: [Number,String],
      default: 1
    },
    'disableClick': Boolean,
    'unelevated': Boolean,
    'flat': Boolean,
    'focusable': Boolean
  },
  
  data() {
    return {
      x: ref(0),
      y: ref(0)
    }
  },
  mounted() {
    // This class produces a tint change on hover, but is unwanted for the glow button.
    const button = this.$refs.glowbutton as any
    button.$el.classList.remove('q-hoverable')
    button.$el.removeChild(button.$el.children[0])
    this.x = button.$el.clientWidth / 2
    this.y = button.$el.clientHeight / 2
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
    shadow() {
      if (this.unelevated || this.flat) return 'transparent'
      var color: string = colors.getPaletteColor(`shadow-${this.color}`)
      if (color !== "#000000") return color
      color = colors.getPaletteColor(this.shadowColor)
      return color === "#000000" ? this.shadowColor : color
    },
    glowStyle() {
      return {
        '--x': `${this.x}px`,
        '--y': `${this.y}px`,
        '--size': this.glowSize,
        '--prop-scale': this.glowScale,
        '--color': this.glow,
        '--shadow-color': this.shadow,
        '--button-scale': this.disableClick ? 1 : 0.98,
        '--shadow-scale': this.disableClick ? 1 : 1.5,
        '--shadow-strength': this.shadowStrength
      }
    }
  },
  methods: {
    mousemove(e: MouseEvent) {
      const test = (e.target as HTMLElement)?.getBoundingClientRect()
      this.x = e.clientX - test.left
      this.y = e.clientY - test.top
    },
  },
})
</script>

<style lang="scss">

.bttn {
  -webkit-transform: translate3d(0, 0, 0); /* Fix for webkit artifacts */
  position: relative;
  cursor: pointer;
  overflow: hidden;
  border-radius: 10px;
  span {
    pointer-events: none;
  }

  &::before {
    --scale: 0;
    --opacity: 0;
    
    will-change: transform; /* Fix for webkit artifacts */
    content: '';
    position: absolute;
    left: calc(var(--x) - var(--size) / 2) !important;
    top: calc(var(--y) - var(--size) / 2) !important;
    width: var(--size);
    height: var(--size);
    background: radial-gradient(circle closest-side, var(--color), transparent 20%);
    
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
  --spread: var(--shadow-strength);
  box-shadow: 0px 8px 20px calc(-4px * var(--spread)) var(--shadow-color);
  /* Scale effect on click */
  --press: 1;
  transform: scale(var(--press));
  transition-duration: 0.2s;
  transition-property: transform box-shadow;
  transition-timing-function: cubic-bezier(0.22, 1, 0.32, 1);
  &:active {
    --press: var(--button-scale);
    --spread: calc(var(--shadow-strength) * var(--shadow-scale));
  }
}

.focusable:focus::before {
  --scale: 1;
  --opacity: 1;
  transition-property: transform, opacity;
}


</style>
