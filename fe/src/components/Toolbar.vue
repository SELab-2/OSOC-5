<template>
    <div class="">
        <q-toolbar class="bg-secondary text-white shadow-2">
            <q-btn flat round>
                <q-avatar size="42px">
                    <img src="../assets/logo.svg">
                 </q-avatar>
            </q-btn>
            <div class="text-subtitle1 q-mx-md"><b>Selection Tool</b></div>
            

              
              <q-tabs class="absolute-center" v-model="tab" shrink>
                <q-tab name="students" label="Students" />
                <q-tab name="projects" label="Projects" />
                <q-tab name="users" label="Users" />
              </q-tabs>
            <q-space />
            <q-btn-dropdown flat rounded icon="mdi-account">
              <div class="row items-center q-my-sm">
              <q-avatar class="q-ml-sm" size="40px">
                <img src="https://cdn.quasar.dev/img/boy-avatar.png">
              </q-avatar>
                <div class="text-subtitle1 q-mx-md">{{user.name}}</div>
              </div>
                <q-separator />
                <q-list separator>
                    <q-item v-for="(item, index) in dropdownitems" :key="`${index}`" clickable v-close-popup tabindex="0">
                        <q-item-section avatar>
                          <q-icon size="xs" :name="`${item.icon}`" color="primary"/>
                        </q-item-section>
                        <q-item-section>
                          <q-item-label :lines="1" >{{item.name}}</q-item-label> 
                        </q-item-section>
                      </q-item>
                </q-list>
            </q-btn-dropdown>
        </q-toolbar>
    </div>
</template>

<script>
import { ref } from 'vue'



export default {
    data() {
        return {
            user: {
              name: 'Miet Claeys'
            },
            dropdownitems: [
              {
                  name: 'Email Templates',
                  icon: 'email'
              },
              {
                  name: 'Change Password',
                  icon: 'key'
              },
              {
                  name: 'Sign Out',
                  icon: 'logout'
              }
          ]
      }
      },
  setup () {
    return {
      tab: ref('students')
    }
  }
}
</script>

<style>
</style>