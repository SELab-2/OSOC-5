<template>
  <q-header
    elevated
    class="bg-white text-white"
    height-hint="98"
  >
    <q-toolbar class="text-blue bg-white">
      <q-btn
        flat
        round
      >
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
          exact
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
            @click=on_dropdown_click(index)
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
  <q-dialog v-model="display_popup" persistent>
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">Change Password</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input
          outlined
          autofocus
          v-model="old_password"
          :type="isPwd1 ? 'password' : 'text'"
          class="inputfield"
          label="Old Password"
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
          v-model="password1"
          :type="isPwd2 ? 'password' : 'text'"
          class="inputfield"
          label="New Password 1"
        />
        <q-icon
          :name="isPwd2 ? 'visibility_off' : 'visibility'"
          class="cursor-pointer"
          @click="isPwd2 = !isPwd2"
        />
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input
          outlined
          autofocus
          v-model="password2"
          :type="isPwd3 ? 'password' : 'text'"
          class="inputfield"
          label="New Password 2"
        />
        <q-icon
          :name="isPwd3 ? 'visibility_off' : 'visibility'"
          class="cursor-pointer"
          @click="isPwd3 = !isPwd3"
        />
      </q-card-section>
      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="Cancel" v-close-popup />
        <q-btn flat label="Add role" @click="change_password_confirm" />
      </q-card-actions>
    </q-card>
  </q-dialog>

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
    const authenticationStore = useAuthenticationStore()
    const password1 = ref('')
    const password2 = ref('')
    const old_password = ref('')
    const display_popup = ref(false)
    return {
      isPwd1: ref(true),
      isPwd2: ref(true),
      isPwd3: ref(true),
      password1,
      password2,
      old_password,
      display_popup,
      color: useMeta(metaData),
      tab: ref('students'),
      authenticationStore,
      on_dropdown_click(test: number) {
        if (test == 0) {
          display_popup.value = true
        } else {
          authenticationStore.logout()
        }
      },
      change_password_confirm() {
        display_popup.value = false
        if (old_password.value == authenticationStore.loggedInUser?.password) {
          authenticationStore.changePassword({p1:password1.value, p2:password2.value})
        }
      },
    }
  },
  computed: {
    fullName(): string {
      return this.authenticationStore.loggedInUser?.first_name + ' ' + this.authenticationStore.loggedInUser?.last_name
    }
  }
})
</script>
