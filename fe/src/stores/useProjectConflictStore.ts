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

export const ProjectConflictStore = defineStore('project_conflict', {
  state: (): State => ({
    next: '',
    conflicts: [],
  }),
  actions: {
    async getConflictingProjects() {
      const studentStore = useStudentStore()
      const projectStore = useProjectStore()

      const conflicts = (
        await instance.get('projects/get_conflicting_projects')
      ).data as Array<{ student: string; projects: Array<string> }>
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
    },
  },
})
