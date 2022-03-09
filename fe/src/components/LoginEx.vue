<template>
            <div class="left relative-position" style="height: 100vh">
                <div style="max-width: 80%; margin-left: 10%; max-height: 90%">
                    <img src="https://osoc.be/img/logo/logo-osoc-color.svg" style="margin-top: 50%" />
                </div>
            </div>

            <div class="q-pa-md right relative-position" style="height: 100vh;">
                <q-form
                    @submit="onSubmit"
                    @reset="onReset"
                    class="q-gutter-md"
                    style="text-align: center; max-width: 500px; margin: 0 auto; margin-top: 50%"
                >
                    <h3 class="text-bold">Login</h3>
                    <q-input
                        filled
                        v-model="email"
                        label="E-mail"
                        lazy-rules
                        :rules="[
                            (val) => (val && val.length > 0) || 'Please enter your email address.',
                        ]"
                    />

                    <q-input
                        filled
                        type="password"
                        v-model="password"
                        label="Password"
                        lazy-rules
                        :rules="[
                            (val) => (val && val.length > 0) || 'Please enter a password.',
                        ]"
                    />

                    <div>
                        <q-btn
                            rounded
                            label="Log in"
                            type="submit"
                            size="md"
                            color="white"
                            text-color="black"
                            class="q-mx-md"
                        />
                        <label class="text-bold">or</label>
                        <q-icon name="mdi-github" size="2.5em" class="q-mx-md cursor-pointer" />
                        <q-separator inset class="middle-sep q-my-md" />
                        <label class="underlined cursor-pointer q-my-md">Signup</label>
                    </div>
                </q-form>
            </div>
</template>




<script lang="ts">
import { useQuasar } from 'quasar'
import { ref } from 'vue'

export default {
    setup() {
        const $q = useQuasar()

        const email = ref(null)
        const password = ref(null)

        return {
            email,
            password,

            onSubmit() {
                $q.notify({
                    color: 'green-4',
                    textColor: 'white',
                    icon: 'cloud_done',
                    message: 'Submitted',
                })
            },

            onReset() {
                email.value = null
                password.value = null
            },
        }
    },
}
</script>



<style>
.middle-sep {
    width: 60%;
    margin-left: 20% !important;
}

.underlined {
    text-decoration: underline;
}

.left {
    float: left;
    width: 50%;
}

.right {
    float: right;
    width: 50%;
}

</style>