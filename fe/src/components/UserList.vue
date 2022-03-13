<template>
    <div class="q-pa-md q-gutter-md">
        <div id="q-app" style="min-height: 100vh">
            <div class="q-ma-sm">
                <q-table
                    :rows="users"
                    :columns="columns"
                    row-key="id"
                    v-model:pagination="pagination"
                    hide-pagination
                >
                    <template v-slot:body="props">
                        <q-tr
                            :class="props.rowIndex%2 == 0 ? 'bg-accent' : ''"
                            :props="props"
                        >
                            <q-td key="name" @click="console.log(props)" :props="props">{{
                                props.row.name
                            }}</q-td>
                            <q-td key="role" :props="props">
                                <q-select
                                    borderless
                                    dense
                                    style="max-width: 100px"
                                    v-model="props.row.role"
                                    :options="roles"
                                    transition-show="jump-down"
                                    transition-hide="jump-up"
                                    transition-duration="300"
                                    behavior="menu"
                                />
                            </q-td>
                            <q-td key="email" :props="props">{{
                                props.row.email
                            }}</q-td>
                            <q-td style="width: 10px" key="remove">
                                <q-btn
                                    flat
                                    round
                                    dense
                                    text-color="red"
                                    icon="mdi-delete-outline"
                                />
                            </q-td>
                        </q-tr>
                    </template>
                </q-table>
                <div class="row justify-center q-mt-md">
                    <q-pagination
                        v-model="pagination.page"
                        color="grey-8"
                        :max="pagesNumber"
                        size="sm"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed } from 'vue'

const columns = [
    {
        name: 'name',
        required: true,
        label: 'Name',
        align: 'left',
        field: 'name',
        sortable: true,
    },
    {
        name: 'role',
        required: true,
        label: 'Role',
        align: 'left',
        field: 'role',
        sortable: true,
    },
    {
        name: 'email',
        align: 'right',
        label: 'Email',
        field: 'email',
        sortable: true,
    },
    {
        name: 'delete',
        align: 'center',
        sortable: false,
    },
]

const roles = ['admin', 'coach', 'disabled']
let pagination = ref({
    sortBy: 'desc',
    descending: false,
    page: 1,
    rowsPerPage: 5,
    // rowsNumber: xx if getting data from a server
})
export default {
    computed: {
        // a computed getter
        pagesNumber() {
            // `this` points to the component instance
            return Math.ceil(this.users.length / pagination.value.rowsPerPage)
        },
    },
    data() {
        return {
            users: [
                {
                    id: 123,
                    name: 'Miet Claeys',
                    email: 'miet@osoc.be',
                    role: ref('admin'),
                },
                {
                    id: 1234,
                    name: 'Wouter Hennen',
                    email: 'wouter.hennen@ugent.be',
                    role: ref('admin'),
                },
                {
                    id: 1235,
                    name: 'Lisa De Jonghe',
                    email: 'lisa.dejonghe@ugent.be',
                    role: ref('admin'),
                },
                {
                    id: 1236,
                    name: 'Lander Saerens',
                    email: 'lander.saerens@ugent.be',
                    role: ref('coach'),
                },
                {
                    id: 1237,
                    name: 'Friedrich Vandenberghe',
                    email: 'friedrich.vandenberghe@ugent.be',
                    role: ref('coach'),
                },
                {
                    id: 1238,
                    name: 'Miet Claeys',
                    email: 'miet@osoc.be',
                    role: ref('coach'),
                },
                {
                    id: 1239,
                    name: 'Wouter Hennen',
                    email: 'wouter.hennen@ugent.be',
                    role: ref('coach'),
                },
                {
                    id: 1230,
                    name: 'Lisa De Jonghe',
                    email: 'lisa.dejonghe@ugent.be',
                    role: ref('disabled'),
                },
                {
                    id: 1231,
                    name: 'Lander Saerens',
                    email: 'lander.saerens@ugent.be',
                    role: ref('disabled'),
                },
                {
                    id: 1232,
                    name: 'Friedrich Vandenberghe',
                    email: 'friedrich.vandenberghe@ugent.be',
                    role: ref('disabled'),
                },
            ],
        }
    },
    setup() {
        return {
            active: ref(true),
            columns,
            roles,
            pagination,
        }
    },
}
</script>

<style></style>
