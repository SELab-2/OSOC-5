const columnsCoaches = [
    {
        name: 'displayName',
        align: 'left' as const,
        label: 'Coach name',
        field: (row: { firstName: string; lastName: string }) =>
            row.firstName + ' ' + row.lastName,
        sortable: true,
    },
]

export default columnsCoaches