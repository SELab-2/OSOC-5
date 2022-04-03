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
  <q-route-tab
    style="padding: 0px 0px"
    ref="glowbutton"
    :class="this.disableGlow ? '' : ''"
  >
  <template #default="prop">
    <btn style="padding: 0px 16px !important; height: 50px !important; margin: 0px 0px !important" :color="color" :glow-color="glowColor" disable-click :label="label"/>
  </template>
  </q-route-tab>
</template>


<script lang="ts">
  import { ref } from 'vue'
  import { colors } from 'quasar'
export default {
  name: 'tab',
  props: {
    'label': String,
    'glowColor': String,
    'glowSize': String,
    'glowScale': Number,
    'disableGlow': Boolean,
    'color': String,
    'shadowColor': String
  },
  mounted() {
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
      // console.log(e)
      this.x =  e.layerX
      this.y =  e.layerY
    },
  },
}
</script>

<style scoped>
  :deep(.q-ripple) {
    display:none;
  }
  
  :deep(.q-btn--rectangle) {
    border-radius: 0px !important;
  }

  :deep(.q-tab__content) {
    padding: 0px !important;
  }
</style>
