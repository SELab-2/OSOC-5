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
            outlined
            v-model="firstName"
            label="First Name"
            lazy-rules
            :rules="[
                  (val) => (val && val.length > 0) || 'This field cannot be empty',
                ]"
          />
        </div>
        <div class="q-pr-xs col-6">
          <q-input
            outlined
            v-model="lastName"
            label="Last Name"
            lazy-rules
            :rules="[
                  (val) => (val && val.length > 0) || 'This field cannot be empty',
                ]"
          />
        </div>
      </div>
      <q-input
        outlined
        v-model="email"
        label="E-mail"
        type="email"
        lazy-rules
        :rules="[
              (val) => (val && val.length > 0) || 'This field cannot be empty',
            ]"
      />
      <div :class="generate ? 'q-pb-xl' : ''">
        <q-input
          outlined
          v-model="password"
          label="Password"
          class="inputfield"
          clearable
          clear-icon="close"
          lazy-rules
          @update:model-value="generate = false"
          :rules="[
                (val) => (val && val.length > 0) || 'This field cannot be empty',
                (val) => (val.length >= 8) || 'Passwords must be longer then 7 characters',
              ]"
        >
          <template v-slot:append>
            <q-icon
              @click="onGeneratePasswordToggle"
              name="mdi-cached"
              class="cursor-pointer"
            />
          </template>

          <template v-slot:hint>
            <div class="warning" v-if="generate">
              This password will not be shown again after the user is created,
              so please make sure that you remember it or write it down.
            </div>
          </template>
        </q-input>
      </div>
    </q-form>
  </q-card-section>
  <q-card-actions align="right">
    <btn flat label="Cancel" @click="onReset" color="yellow" v-close-popup />
    <btn flat v-model="password" :label="'Create ' + role" @click="onSubmit" color="yellow" v-close-popup
    :disabled="password.length <= 8"/>
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
        color: 'warning',
        message: `Error ${error} while creating user, please try again`,
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
      for ( var i = 0; i < 12; i++ ) {
        result += characterSet.charAt(Math.floor(Math.random() * characterSet.length));
      }
      this.password = result
      this.generate = true
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
  margin: 10px;
  margin-left: 20px;
  margin-right: 20px;
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
</style>
