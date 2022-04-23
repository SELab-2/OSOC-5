<template>
  <div
    class="relative-position container flex justify-center"
    style="width: 100vw"
  >
    <div
      class="q-pa-md q-gutter-md"
      style="width: 1000px"
    >
      <div class="row">
        <div class="text-bold text-h4">
          Add User
        </div>
      </div>
      <q-form
          @submit="onSubmit"
          @reset="onReset"

          class="q-px-xl q-mb-lg"
          style="text-align: center; max-width: 1000px; margin: 0 auto; margin-top: 7em;"
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
        <div >
          <q-input
              outlined
              v-model="password"
              label="Password"
              :type="!generate ? 'password' : 'text'"
              class="inputfield"
              :readonly="generate"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'This field cannot be empty',
              ]"
          />
        </div>
        <div class="warning" v-if="generate">
          This password will not be shown again after the user is created,
          so please make sure that you remember it or write it down.
        </div>
        <div class="row">
          <q-checkbox
            v-model="generate"
            color="primary"
            label="Use Generated Password"
            @click="onGeneratePasswordToggle"
          />
        </div>
        <div class="row">
          <q-checkbox
            v-model="admin"
            color="primary"
            label="Does this user have admin privileges?"
          />
          <q-space></q-space>
        </div>
        <div class="row">
          <q-checkbox
            v-model="active"
            color="primary"
            label="Is this user active?"
          />
          <q-space></q-space>
        </div>
        <div class="hint">
          Users that are set as inactive will not be able to login without an admin switching them to
          the 'active' state.
        </div>
        <btn
          label="add user"
          type="submit"
          size="md"
          color="primary"
          class="q-mx-md cornered"
          glow-color="#00ECAA"
        />
      </q-form>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted} from '@vue/runtime-core'
import {useAuthenticationStore} from "../../stores/useAuthenticationStore"
import {ref} from 'vue'
import {exportFile, useQuasar} from 'quasar'
import SegmentedControl from '../../components/SegmentedControl.vue'
import { User } from '../../models/User'
import {floor, random} from 'Math'
export default defineComponent({
  components: { SegmentedControl },
  setup() {
    const q = useQuasar()
    const password = ref('')
    const email = ref('')
    const firstName = ref('')
    const lastName = ref('')
    const admin = ref(false)
    const active = ref(true)
    const authenticationStore = useAuthenticationStore()
    const generate = ref(false)
    const generatedPassword = ref(null)
    return {
      generate,
      generatedPassword,
      email,
      password,
      firstName,
      lastName,
      admin,
      active,
      filter: ref(''),
      roleFilter: ref('all'),
      q,
      authenticationStore
    }
  },
  methods: {
    onSubmit () {
      this.authenticationStore.register(
        {firstName: this.firstName, lastName: this.lastName, email: this.email, 
        password1: this.password, password2: this.password, is_active: this.active, is_admin: this.admin}
        ).then(() => {
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
      this.email.value = ""
      this.password.value = ""
    },
    onGeneratePasswordToggle() {
      if (this.generate) {
        let result = ''
        const characterSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        for ( var i = 0; i < 12; i++ ) {
          result += characterSet.charAt(Math.floor(Math.random() * characterSet.length));
        }
        this.password = result
      } else {
        this.password = ""
      }
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
