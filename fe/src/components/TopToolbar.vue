<template>
  <q-header class="bg-white text-white" height-hint="98">
    <q-toolbar class="text-osoc-blue bg-white shadow-2">
      <btn flat round href="https://www.osoc.be">
        <q-avatar size="42px">
          <img src="../assets/logo.svg">
        </q-avatar>
      </btn>

      <q-space/>
      <q-tabs
        v-model="tab"
        class="centered-tabs"
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
      <q-space/>
      <q-btn-dropdown
        flat
        rounded
        icon="mdi-account"
        :label="fullName"
      >
        <q-separator/>

        <q-list separator>
          <q-item
            v-close-popup
            clickable
            @click=on_dropdown_click()
            tabindex="0"
          >
            <q-item-section avatar>
              <q-icon
                size="xs"
                name="key"
                color="primary"
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
            @click="authenticationStore.logout()"
            tabindex="0"
          >
            <q-item-section avatar>
              <q-icon
                size="xs"
                name="logout"
                color="primary"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label :lines="1">
                Sign Out
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
    </q-toolbar>
  </q-header>
  <q-dialog v-model="display_popup" persistent>
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">Change Password</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input
          outlined
          autofocus
          v-model="password1"
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
          outlined
          autofocus
          v-model="password2"
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
      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="Cancel" v-close-popup />
        <q-btn flat label="Submit Password Change" @click="change_password_confirm" />
      </q-card-actions>
    </q-card>
  </q-dialog>

</template>

<script lang="ts">
import {defineComponent, ref} from 'vue'
import { useQuasar } from 'quasar'
import { useAuthenticationStore } from '../stores/useAuthenticationStore'

export default defineComponent({
  data() {
    return {
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
  setup() {
    const $q = useQuasar()
    const authenticationStore = useAuthenticationStore()
    const password1 = ref('')
    const password2 = ref('')
    const display_popup = ref(false)
    return {
      isPwd1: ref(true),
      isPwd2: ref(true),
      password1,
      password2,
      display_popup,
      tab: ref('students'),
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
  computed: {
    fullName(): string {
      return this.authenticationStore.loggedInUser?.firstName + ' ' + this.authenticationStore.loggedInUser?.lastName
    }
  },
})
</script>

<style>
@media only screen and (min-width: 900px) {
.centered-tabs {
  position: absolute !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
}
}

</style>
