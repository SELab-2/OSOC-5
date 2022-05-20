<template>
  <q-header
    class="bg-white text-white"
    height-hint="98"
  >
    <q-toolbar class="shadow-2" :class="`bg-${$q.dark.isActive ? 'dark' : 'white'} text-${$q.dark.isActive ? 'white' : 'osoc-blue'}`">
      <btn flat round href="https://www.osoc.be">
        <q-avatar size="42px">
          <img :src="`/src/assets/logo${$q.dark.isActive ? '_dark' : ''}.svg`">
        </q-avatar>
      </btn>

      <q-space />
      <q-tabs
        class="centered-tabs"
        shrink
        outside-arrows
      >
        <q-route-tab
          name="students"
          label="Select Students"
          :to="lastStudent ?? '/students'"
        />
        <q-route-tab
          name="projects"
          label="Projects"
          to="/projects"
          exact
        />
        <q-route-tab
          v-if="authenticationStore.loggedInUser?.isAdmin"
          name="users"
          label="Manage Users"
          to="/users"
          exact
        />
        <q-route-tab
          v-if="authenticationStore.loggedInUser?.isAdmin"
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
            v-close-popup
            color="yellow"
            class="text-black"
            v-ripple
            clickable
            tabindex="0"
            :to="`/advanced`"
          >
            <q-item-section avatar>
              <q-icon
                size="xs"
                name="settings"
                color="yellow"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label :lines="1">
                Advanced Options
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-item
            v-close-popup
            v-ripple
            clickable
            tabindex="0"
            @click="on_dropdown_click()"
          >
            <q-item-section avatar>
              <q-icon
                size="xs"
                name="key"
                color="yellow"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label :lines="1">
                Change Password
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-item
            v-close-popup
            v-ripple
            clickable
            tabindex="0"
            @click="authenticationStore.logout()"
          >
            <q-item-section avatar>
              <q-icon
                size="xs"
                name="logout"
                color="yellow"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label :lines="1">
                Sign Out
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <q-separator/>
        <div class="text-caption text-bold q-ml-xs q-mt-xs">Color Scheme</div>
        <SegmentedControl
          no-shadow
          color="yellow"
          v-model="authenticationStore.colorScheme"
          :options="[
            { name: 'auto', label: 'Auto' },
            { name: false, label: 'Light' },
            { name: true, label: 'Dark' },
          ]"
        />
      </q-btn-dropdown>
    </q-toolbar>
  </q-header>
  <q-dialog
    v-model="display_popup"
    persistent
  >
    <ChangePasswordDialog :callback="() => display_popup = false" />
  </q-dialog>
</template>

<script lang="ts">
import {defineComponent, ref, Ref} from 'vue'
import { useAuthenticationStore } from '../stores/useAuthenticationStore'
import { useStudentStore } from '../stores/useStudentStore'
import ChangePasswordDialog from "./ChangePasswordDialog.vue";
import SegmentedControl from './SegmentedControl.vue'

export default defineComponent({
  components: { SegmentedControl, ChangePasswordDialog },
  setup() {
    const authenticationStore = useAuthenticationStore()
    const display_popup = ref(false)
    return {
      display_popup,
      authenticationStore,
      on_dropdown_click() {
        display_popup.value = true
      },
    } 
  },
  data() {
    let lastStudent: Ref<string | null> = ref(null)
    return {
      lastStudent,
      dropdownitems: [
        {
          name: 'Change Password',
          icon: 'key',
        },
        {
          name: 'Sign Out',
          icon: 'key',
        },
      ],
    }
  },
  computed: {
    fullName(): string {
      return this.authenticationStore.loggedInUser?.firstName + ' ' + this.authenticationStore.loggedInUser?.lastName
    }
  },
  watch: {
    $route: {
      handler(newValue) {
      if (newValue.name === 'Student Page') {
        this.lastStudent = newValue.path
      }
    },
    immediate: true
    },
    'authenticationStore.colorScheme': {
      handler(newValue: boolean | 'auto') {
        this.$q.dark.set(newValue)
      },
      immediate: true
    }
  },
})
</script>

<style scoped>
@media only screen and (min-width: 900px) {
.centered-tabs {
  position: absolute !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
}
}
</style>

<style>
.q-menu {
  border-radius: 10px !important;
}
</style>
