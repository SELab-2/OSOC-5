<template>
  <q-card-section>
    <div class="row">
      <div class="text-bold text-h4">
        Create user
      </div>
      <q-space />
      <q-select
        v-model="role"
        v-ripple
        borderless
        dense
        class="bg-yellow"
        color="yellow"
        style="padding-left:10px; border-radius: 5px; position: relative; width: 80px"
        :options="roles"
        transition-show="jump-down"
        transition-hide="jump-up"
        transition-duration="300"
        behavior="menu"
        map-options
        emit-value
      />
    </div>
  </q-card-section>
  <q-card-section>
    <q-form
      autocomplete="off"
      style="text-align: center; min-width: 500px; max-width: 1000px; margin: 0 auto;"
    >
      <div class="row">
        <div class="q-pr-xs col-6">
          <q-input
            v-model="firstName"
            outlined
            label="First Name"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'This field cannot be empty',
            ]"
          />
        </div>
        <div class="q-pr-xs col-6">
          <q-input
            v-model="lastName"
            outlined
            label="Last Name"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'This field cannot be empty',
            ]"
          />
        </div>
      </div>
      <q-input
        v-model="email"
        outlined
        label="E-mail"
        type="email"
        lazy-rules
        :rules="[
          (val) => (val && val.length > 0) || 'This field cannot be empty', isValidEmail,
        ]"
      />
      <div :class="generate ? 'q-pb-xl' : ''">
        <q-input
          v-model="password"
          outlined
          label="Password"
          class="inputfield"
          clearable
          clear-icon="close"
          :rules="[
            (val) => (val && val.length > 8) || 'Passwords must be longer than 8 characters',
          ]"
          @update:model-value="generate = false"
        >
          <template #append>
            <q-icon
              name="mdi-cached"
              class="cursor-pointer"
              @click="onGeneratePasswordToggle"
            />
          </template>

          <template #hint>
            <div
              v-if="generate"
              class="warning"
            >
              This password will not be shown again after the user is created,
              so please make sure that you remember it or write it down.
            </div>
          </template>
        </q-input>
      </div>
    </q-form>
  </q-card-section>
  <q-card-actions align="right">
    <btn
      v-close-popup
      flat
      label="Cancel"
      color="yellow"
      @click="onReset"
    />
    <btn
      v-model="password"
      flat
      :label="'Create ' + role"
      color="yellow"
      :disabled="password.length < 8"
      @click="onSubmit"
    />
  </q-card-actions>
</template>

<script lang="ts">
import {defineComponent} from '@vue/runtime-core'
import {useAuthenticationStore} from "../../stores/useAuthenticationStore"
import {ref} from 'vue'
import {useQuasar} from 'quasar'
import roles from '../../models/UserRoles'
import { useCoachStore } from '../../stores/useCoachStore'

export default defineComponent({
  props: {
    created: {
      type: Function,
      required: true
    }
  },
  setup() {
    const q = useQuasar()
    const password = ref('')
    const email = ref('')
    const firstName = ref('')
    const lastName = ref('')
    const authenticationStore = useAuthenticationStore()
    const coachStore = useCoachStore()
    const generate = ref(false)
    const generatedPassword = ref(null)
    return {
      generate,
      generatedPassword,
      email,
      password,
      firstName,
      lastName,
      roles,
      role: ref(roles.at(1)?.value || 'inactive'),
      filter: ref(''),
      roleFilter: ref('all'),
      q,
      authenticationStore,
      coachStore
    }
  },
  methods: {
    onSubmit () {
      this.authenticationStore.register({
          firstName: this.firstName,
          lastName: this.lastName,
          email: this.email,
          password1: this.password,
          password2: this.password,
          is_active: this.role ? this.role != 'inactive' : true,
          is_admin: this.role ? this.role == 'admin' : false
      }).then(() => {
        // run the 'callback'
        this.created()

        this.q.notify({
          icon: 'done',
          color: 'positive',
          message: 'User was succesfully created',
        })
      }).
      catch((error) => {
        this.q.notify({
        icon: 'warning',
        color: 'negative',
        message: `Error ${error.response.data.non_field_errors}`,
        textColor: 'black'
      });
      })
    },
    onReset() {
      this.email = ""
      this.password = ""
    },
    onGeneratePasswordToggle() {
      let result = ''
      const characterSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
      for (let i = 0; i < 12; i++ ) {
        result += characterSet.charAt(Math.floor(Math.random() * characterSet.length));
      }
      this.password = result
      this.generate = true
    },
    isValidEmail (val: string) {
      const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
      return emailPattern.test(val) || 'Invalid email';
    }
  }
})
</script>

<style scoped>

:deep(.q-field__control) {
  border-radius: 10px !important;
}

:deep(.q-btn--rectangle) {
  border-radius: 12px !important;
}

:deep(.q-menu) {
  border-radius: 10px !important;
}

.user-table {
  border-radius: 10px;
}

.warning {
  color: red;
  margin: 10px 20px;
}

.hint {
  color: green;
  margin: 10px;
}
</style>

<style lang="sass">
.my-table
  thead
    /* bg color is important for th; just specify one */
    background-color: $yellow-7

.q-field__bottom
  margin-bottom: 3px
</style>
