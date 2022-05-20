const userColumns = [
    {
        name: 'name',
        required: true,
        label: 'Name',
        align: 'left' as const,
        field: 'name',
        sortable: true,
    },
    {
        name: 'role',
        required: true,
        label: 'Role',
        align: 'left' as const,
        field: 'role',
        sortable: true,
    },
    {
        name: 'assignedto',
        required: false,
        label: 'Assigned To',
        align: 'left' as const,
        field: 'assignedto',
    },
    {
        name: 'email',
        align: 'left' as const,
        label: 'Email',
        field: 'email',
        sortable: true,
    },
    {
        name: 'action',
        align: 'right' as const,
        label: '',
        field: '',
        sortable: false,
    },
]

export default userColumns