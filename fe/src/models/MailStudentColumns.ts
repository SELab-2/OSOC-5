const columnsMails = [
    {
        name: 'visibility',
        required: false,
        label: '',
        align: 'left' as const,
        field: '',
        sortable: false,
    },
    {
        name: 'name',
        required: true,
        label: 'Name',
        align: 'left' as const,
        field: 'name',
        sortable: true,
    },
    {
        name: 'status',
        required: true,
        label: 'Status',
        align: 'left' as const,
        field: 'status',
        sortable: true,
    },
    {
        name: 'email',
        align: 'right' as const,
        label: 'Email',
        field: 'email',
        sortable: true,
    }
]

export default columnsMails