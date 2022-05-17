const columnsCoaches = [
  {
    name: 'displayName',
    align: 'left' as const,
    label: 'Coach name',
    field: (row: { firstName: string; lastName: string }) =>
      row.firstName + ' ' + row.lastName,
    sortable: true,
  },
  {
    name: 'isActive',
    align: 'left' as const,
    label: 'Is active',
    field: 'isActive',
    sortable: true,
  },
  {
    name: 'isAdmin',
    align: 'left' as const,
    label: 'Is admin',
    field: 'isAdmin',
    sortable: true,
  },
]

export default columnsCoaches
