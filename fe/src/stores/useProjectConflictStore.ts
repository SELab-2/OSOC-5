import { defineStore } from 'pinia'
import { Project } from '../models/Project'
import { Student } from '../models/Student'
import { instance } from '../utils/axios'
import { useProjectStore } from './useProjectStore'
import { useStudentStore } from './useStudentStore'

interface State {
  conflicts: { student: Student; projects: Project[] }[]
  nextPage: string
  selectedStudentId: number
}

export const useProjectConflictStore = defineStore('project/conflict', {
  state: (): State => ({
    conflicts: [],
    nextPage: '',
    selectedStudentId: 0,
  }),
  actions: {
    async getConflictingProjects(url?: string) {
      const studentStore = useStudentStore()
      const projectStore = useProjectStore()

      const { data } = await instance.get(
        url ?? 'projects/get_conflicting_projects'
      )

      const conflicts = data.results as Array<{
        student: string
        projects: Array<string>
      }>

      const resConflicts = []
      for (const conflict of conflicts) {
        const student = await studentStore.getStudent(conflict.student)
        const projects = await Promise.all(
          conflict.projects.map(
            async (project: string) =>
              await projectStore.getOrFetchProject(project)
          )
        )

        resConflicts.push({ student, projects })
      }

      this.conflicts = resConflicts
      this.nextPage = data.next
    },
    async resolveConflict(
      selectedProject: Project,
      selectedConflict: { student: Student; projects: Project[] }
    ) {

      if (!(selectedProject.suggestedStudents)) throw new Error('No suggested students present.')

      const suggestions = selectedProject.suggestedStudents.filter(
        ({ student }) => student.id === selectedConflict.student.id
      )

      if (suggestions.length == 0) throw new Error('An unexpected error has occured')

      if (suggestions.length > 1)
        throw new Error(
          'Please delete the assignment to skills until only 1 is left'
        )

      const suggestion = suggestions[0]

      await instance.post('/projects/resolve_conflicts/', [
        {
          project: selectedProject.url,
          student: selectedConflict.student.url,
          coach: suggestion.coach.url,
          skill: suggestion.skill.url,
        },
      ])

      const projectStore = useProjectStore()
      await projectStore.loadProjects()

      const studentStore = useStudentStore()
      studentStore.students = studentStore.students.filter(
        ({ url }) => url !== selectedConflict.student.url
      )
    },
  },
})
