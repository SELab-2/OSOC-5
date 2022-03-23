<template>
  <q-header elevated class="bg-white text-white" height-hint="98">
    <q-toolbar class="text-blue bg-white">
      <q-btn flat round>
        <q-avatar size="42px">
          <img src="../assets/logo.svg" />
        </q-avatar>
      </q-btn>

      <q-space />
      <q-tabs class="absolute-center" v-model="tab" shrink>
        <q-route-tab name="students" label="Select Students" to="/students" exact />
        <q-route-tab name="projects" label="Projects" to="/projects" exact />
        <q-route-tab name="users" label="Manage Users" to="/users" exact />
      </q-tabs>
      <q-space />
      <q-btn-dropdown flat rounded icon="mdi-account">
        <div class="row items-center q-my-sm">
          <q-avatar class="q-ml-sm" size="40px">
            <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
          </q-avatar>
          <div class="text-subtitle1 q-mx-md">{{ user.name }}</div>
        </div>
        <q-separator />
        <q-list separator>
          <q-item
            v-for="(item, index) in dropdownitems"
            :key="`${index}`"
            clickable
            v-close-popup
            tabindex="0"
          >
            <q-item-section avatar>
              <q-icon size="xs" :name="`${item.icon}`" color="primary" />
            </q-item-section>
            <q-item-section>
              <q-item-label :lines="1">{{ item.name }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
    </q-toolbar>
  </q-header>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

import { useMeta } from 'quasar'

const metaData = {
  meta: {
    themecolor: { name: 'theme-color', content: '#24a3cb' },
  },
}

export default defineComponent({
  data() {
    return {
      user: {
        name: 'Miet Claeys',
      },
      dropdownitems: [
        {
          name: 'Email Templates',
          icon: 'email',
        },
        {
          name: 'Change Password',
          icon: 'key',
        },
        {
          name: 'Sign Out',
          icon: 'logout',
        },
      ],
    }
  },
  setup() {
    return {
      color: useMeta(metaData),
      tab: ref('students'),
    }
  },
})
</script>
