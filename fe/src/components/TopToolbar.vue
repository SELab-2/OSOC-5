<template>
  <q-header class="bg-white text-white" height-hint="98">
    <q-toolbar class="text-osoc-blue bg-white shadow-2">
      <q-btn flat round>
        <q-avatar size="42px">
          <img src="../assets/logo.svg">
        </q-avatar>
      </q-btn>

      <q-space />
      <q-tabs
        v-model="tab"
        class="absolute-center"
        shrink
      >
        <q-route-tab
          name="students"
          label="Select Students"
          to="/students"
        />
        <q-route-tab
          name="projects"
          label="Projects"
          to="/projects"
          exact
        />
        <q-route-tab
          name="users"
          label="Manage Users"
          to="/users"
          exact
        />
        <q-route-tab
          name="mails"
          label="Mails"
          to="/mails"
          exact
        />
      </q-tabs>
      <q-space />
      <q-btn-dropdown
        flat
        rounded
        icon="mdi-account"
        :label="fullName"
      >
        <q-separator />
        <q-list separator>
          <q-item
            v-for="(item, index) in dropdownitems"
            :key="`${index}`"
            v-close-popup
            clickable
            @click="item.click"
            tabindex="0"
          >
            <q-item-section avatar>
              <q-icon
                size="xs"
                :name="`${item.icon}`"
                color="primary"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label :lines="1">
                {{ item.name }}
              </q-item-label>
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
import { useAuthenticationStore } from '../stores/useAuthenticationStore'

const metaData = {
  meta: {
    themecolor: { name: 'theme-color', content: '#24a3cb' },
  },
}

export default defineComponent({
  setup() {
    const authenticationStore = useAuthenticationStore()

    return {
      color: useMeta(metaData),
      tab: ref('students'),
      authenticationStore
    }
  },
  data() {
    return {
      dropdownitems: [
        {
          name: 'Email Templates',
          icon: 'email',
          click: () => console.log("test"),
        },
        {
          name: 'Change Password',
          icon: 'key',
          click: () => console.log("test"),
        },
        {
          name: 'Sign Out',
          icon: 'logout',
          click: this.authenticationStore.logout,
        },
      ],
    }
  },
  computed: {
    fullName(): string {
      return this.authenticationStore.loggedInUser?.firstName + ' ' + this.authenticationStore.loggedInUser?.lastName
    }
  },
  method: {
    logout(): void {
      this.authenticationStore.logout()
    }
  }
})
</script>
