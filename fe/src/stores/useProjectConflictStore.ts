import { defineStore } from 'pinia'
import { Project } from '../models/Project'
import { Student } from '../models/Student'
import { instance } from '../utils/axios'
import { useProjectStore } from './useProjectStore'
import { useStudentStore } from './useStudentStore'

interface State {
  next: string
  conflicts: Array<{ student: Student; projects: Array<Project> }>
}

export const useProjectConflictStore = defineStore('project_conflict', {
  state: (): State => ({
    next: '',
    conflicts: [],
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

      this.next = data.next
      this.conflicts = resConflicts
    },
    async loadMoreProjects() {
      if (this.next !== null) await this.getConflictingProjects(this.next)
    },
    async resolveConflict(
      conflict: {
        student: Student
        projects: Array<Project>
      },
      selectedProject: Project
    ) {
      const suggestions = selectedProject.suggestedStudents?.filter(
        ({ student }) => student.id === conflict.student.id
      )

      if (!suggestions) throw new Error('An unexpected error has occured')

      console.log(suggestions)
      if (suggestions?.length > 1)
        throw new Error(
          'Please delete the assignment to skills until only 1 is left'
        )

      const suggestion = suggestions[0]

      await instance.post('/projects/resolve_conflicts/', [
        {
          project: selectedProject.id,
          student: conflict.student.id,
          coach: suggestion.coach.id,
          skill: suggestion.skill.id,
        },
      ])
    },
  },
})
