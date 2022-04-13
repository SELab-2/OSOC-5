<template>
  <div>
    <q-item>
      <q-item-section side>
        <q-avatar
          :color="color ? color + '-1' : 'grey-4'"
          :text-color="color ? color + '-4': 'black'"
          :icon="useIcon"
        />
      </q-item-section>
      <q-item-section>
        <q-item-label v-if="title">
          {{ title }}
        </q-item-label>
        <q-item-label caption>
          {{ content }}
        </q-item-label>
      </q-item-section>
    </q-item>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";

export default defineComponent({
  props: {
    title: {
      type: String,
      required: false,
      default: ""
    },
    content: {
      type: String,
      required: true
    },
    color: {
      type: String,
      required: true
    },
    useIcon: {
      type: String,
      required: true
    }
  },
  computed: {
    test() : string {
      console.log(this.title)
      return ""
    }
  }
})
</script>
