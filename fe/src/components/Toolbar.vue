<template>
    <div class="">
        <q-toolbar class="bg-white text-secondary shadow-2">
            <q-btn flat round>
                <q-avatar size="42px">
                    <img src="../assets/logo.svg">
                 </q-avatar>
            </q-btn>
              <q-space />
              
              <q-tabs v-model="tab" shrink>
                <q-tab name="students" label="Select Students" />
                <q-tab name="projects" label="Projects" />
                <q-tab name="users" label="Manage Users" />
              </q-tabs>
            <q-space />
            <q-btn-dropdown flat rounded icon="mdi-account">
                <q-list>
                    <q-item v-for="(item, index) in items" :key="`${index}`" clickable v-close-popup tabindex="0">
                        <q-item-section>
                          <q-icon size="md" :name="`${item.icon}`" color="primary"/>
                        </q-item-section>
                        <q-item-section>
                          <q-item-label>{{item.name}}</q-item-label> 
                          <q-item-label caption>February 22, 2016</q-item-label>
                        </q-item-section>
                        <q-item-section side>
                          <q-icon name="info" />
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
            items: [
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