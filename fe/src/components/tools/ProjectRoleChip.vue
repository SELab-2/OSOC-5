<template>
    <!-- v-model:selected is not used here since this displays an icon, which we don't want. As an alternative, @click is used. -->
	<q-chip
    clickable
    @click="enabled = !enabled"
    outline
    :color="role.color + (enabled ? '-8' : '-4')"
    :class="'bg-' + role.color + (enabled ? '-4' : '-1')"
    style="border-width: 1.5px;"
    :style="'padding-left: ' + (role.info ? '2px' : '8px') + '; padding-right: 8px;'">
    <template v-slot:default>
        <div class="row" style="display: flex; align-items: center">
            <q-icon v-if="role.info" 
                name="info" 
                size="sm" 
                :color="role.color + '-6'"/>
            <div  
                :style="'color: ' + (enabled ? 'white' : 'black') + '; padding-left: ' + (role.info ? '3px' : '0px')"
                >{{ role.label }}</div>
            <div class="text-bold" 
                style="padding-left: 3px;" 
                :class="(enabled ? 'text-white' : ('text-' + role.color + '-8'))" 
                >{{ role.amount }}</div>
            <q-tooltip 
                v-if="role.info" 
                :class="'bg-' + role.color + '-2'" 
                class="text-black shadow-2" 
                anchor='bottom middle' 
                self='center middle'
                >{{ role.info }}</q-tooltip>
        </div>
    </template>
    </q-chip>
</template>

<script>
import { ref } from 'vue'

export default {
    props: ['role', 'modelValue'],
    emits: ['update:modelValue'],
    computed: {
        enabled: {
          get() {
            return this.modelValue
          },
          set(value) {
            this.$emit('update:modelValue', value)
          }
        }
      }
}
</script>