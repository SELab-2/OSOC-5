const columnsSkills = [
  {
    name: 'skill',
    align: 'left' as const,
    label: 'Project Skill',
    field: 'skill',
    sortable: true,
  },
  {
    name: 'amount',
    align: 'left' as const,
    label: 'Amount',
    field: 'amount',
    sortable: true,
  },
  {
    name: 'comment',
    align: 'left' as const,
    label: 'Comment',
    field: 'comment',
    sortable: true,
  },
  {
    name: 'color',
    align: 'center' as const,
    label: 'Color',
    field: 'color',
    sortable: false,
  },
  {
    name: 'edit',
    align: 'center' as const,
    label: '',
    field: '',
    sortable: false,
  },
  {
    name: 'action',
    align: 'center' as const,
    label: '',
    field: '',
    sortable: false,
  },
]

export default columnsSkills
