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

        <q-list separator>
          <q-item
            v-close-popup
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
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">
          Change Password
        </div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input
          v-model="password1"
          outlined
          autofocus
          :type="isPwd1 ? 'password' : 'text'"
          class="inputfield"
          label="New Password 1"
          lazy-rules
          :rules="[(val) => (val && val.length > 7) || 'Password is too short.']"
        />
        <q-icon
          :name="isPwd1 ? 'visibility_off' : 'visibility'"
          class="cursor-pointer"
          @click="isPwd1 = !isPwd1"
        />
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input
          v-model="password2"
          outlined
          autofocus
          :type="isPwd2 ? 'password' : 'text'"
          class="inputfield"
          label="New Password 2"
        />
        <q-icon
          :name="isPwd2 ? 'visibility_off' : 'visibility'"
          class="cursor-pointer"
          @click="isPwd2 = !isPwd2"
        />
      </q-card-section>
      <q-card-actions
        align="right"
        class="text-primary"
      >
        <q-btn
          v-close-popup
          flat
          label="Cancel"
        />
        <q-btn
          flat
          label="Submit Password Change"
          @click="change_password_confirm"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import {defineComponent, ref, Ref} from 'vue'
import { useQuasar } from 'quasar'
import { useAuthenticationStore } from '../stores/useAuthenticationStore'
import { useStudentStore } from '../stores/useStudentStore'
import SegmentedControl from './SegmentedControl.vue'

export default defineComponent({
  components: { SegmentedControl },
  setup() {
    const $q = useQuasar()
    const authenticationStore = useAuthenticationStore()
    const password1 = ref('')
    const password2 = ref('')
    const display_popup = ref(false)
    return {
      studentStore: useStudentStore(),
      isPwd1: ref(true),
      isPwd2: ref(true),
      password1,
      password2,
      display_popup,
      authenticationStore,
      on_dropdown_click() {
        display_popup.value = true
      },
      change_password_confirm() {
        if (password1.value == password2.value) {
          display_popup.value = false
          authenticationStore.changePassword({p1:password1.value, p2:password2.value}).then(() => {
            $q.notify({
              icon: 'done',
              color: 'positive',
              message: 'Password was successfully changed',
            })
          }).
          catch((error) => {
            $q.notify({
            icon: 'warning',
            color: 'warning',
            message: `Error ${error} while changing password, please try again`,
            textColor: 'black'
          });
        })
        } else {
          $q.notify({
            color: 'negative',
            message: 'Passwords do not match'
          })
        }
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
  computed: {
    fullName(): string {
      return this.authenticationStore.loggedInUser?.firstName + ' ' + this.authenticationStore.loggedInUser?.lastName
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
