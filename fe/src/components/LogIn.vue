<template>
    <section class="xop-container">
        <div class="xop-div xop-left">
            <article>
                <img src="https://osoc.be/img/logo/logo-osoc-color.svg" />
            </article>
        </div>

        <div class="xop-div xop-right">
            <article>
                <q-icon
                    v-if="dark"
                    name="mdi-white-balance-sunny"
                    size="2.5em"
                    class="q-ma-md cursor-pointer fixed-top-right"
                    @click="toggle"
                />
                <q-icon
                    v-else
                    name="mdi-moon-waning-crescent"
                    size="2.5em"
                    class="q-ma-md cursor-pointer fixed-top-right"
                    @click="toggle"
                />

                <q-form
                    @submit="onSubmit"
                    @reset="onReset"
                    class="q-gutter-md"
                    style="text-align: center; max-width: 500px; margin: 0 auto;"
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
                        class="move-up"
                        filled
                        :type="isPwd ? 'password' : 'text'"
                        v-model="password"
                        label="Password"
                        lazy-rules
                        :rules="[
                            (val) => (val && val.length > 0) || 'Please enter a password.',
                        ]"
                    >
                        <template v-slot:append>
                            <q-icon
                                :name="isPwd ? 'visibility_off' : 'visibility'"
                                class="cursor-pointer"
                                @click="isPwd = !isPwd"
                            />
                        </template>
                    </q-input>
                    <label class="fpwd cursor-pointer">Forgot your password?</label>
                    <br />

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
            </article>
        </div>
    </section>
</template>




<script lang="ts">
import { useQuasar } from 'quasar'
import { ref } from 'vue'

export default {
    setup() {
        const $q = useQuasar()



        const email = ref(null)
        const password = ref(null)
        const dark = ref(false)

        $q.dark.set(dark.value)

        return {
            email,
            password,
            dark,
            isPwd: ref(true),

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

            toggle() {
                dark.value = !dark.value;
                $q.dark.set(dark.value)
            }
        }
    },
}
</script>




<style>
html,
body,
section {
    height: 100vh;
}

body {
    text-align: center;
}

.xop-container {
    display: flex;
}

.xop-div {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.xop-left,
.xop-right {
    background-size: cover;
    background-position: center;
    flex: 1;
    padding: 1rem;
    transition: all 0.2s ease-in-out;
}

.underlined {
    text-decoration: underline;
}

.move-up {
    position: relative;
}

.fpwd {
    float: right;
    position: absolute;
    top: 235px;
    right: 0px;
    text-decoration: underline;
    font-size: 80%;
}
</style>