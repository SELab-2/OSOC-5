<template>
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
        label="New Password"
        :type="isPwd1 ? 'password' : 'text'"
        lazy-rules
        :rules="[(val) => (val && val.length > 7) || 'Password is too short.']"
      >
        <template #append>
          <q-icon
            :name="isPwd1 ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd1 = !isPwd1"
          />
        </template>
      </q-input>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <q-input
        v-model="password2"
        outlined
        autofocus
        label="Confirm Password"
        :type="isPwd2 ? 'password' : 'text'"
        lazy-rules
        :rules="[(val) => (val && val === password1) || 'Passwords do not match.']"
      >
        <template #append>
          <q-icon
            :name="isPwd2 ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd2 = !isPwd2"
          />
        </template>
      </q-input>
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
        :disabled="password1.length <= 8 || password2.length <= 8 || password1 !== password2"
        @click="change_password_confirm"
      />
    </q-card-actions>
  </q-card>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { useAuthenticationStore } from "../stores/useAuthenticationStore";
import { ref } from "vue";
import { useStudentStore } from "../stores/useStudentStore";

export default defineComponent ({
  props: {
    callback: {
      type: Function,
      required: true
    }
  },
  setup() {
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
    }
  },
  methods: {
    change_password_confirm() {
      this.authenticationStore.changePassword({p1:this.password1, p2:this.password2}).then(() => {
        this.$q.notify({
          icon: 'done',
          color: 'positive',
          message: 'Password was successfully changed',
        })
        this.callback()
      }).
      catch((error) => {
        console.log(error.response)
        this.$q.notify({
          icon: 'warning',
          color: 'negative',
          message: `Error ${error.response.data.new_password2}`,
          textColor: 'black'
        });
      })
    },
  }
})
</script>
