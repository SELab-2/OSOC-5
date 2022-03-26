import {defineStore} from "pinia";
import {instance} from "../utils/axios";
import {convertObjectKeysToCamelCase} from "../utils/case-conversion";

export const useStudentStore = defineStore('user/student', {
    state: () => ({
        students: [],
        isLoadingStudents: false,
    }),
    actions: {
        async loadStudents() {
            this.isLoadingUsers = true
            instance
                .get('students/')
                .then(({ data }) => {
                    this.isLoadingUsers = false
                    console.log(data)
                    this.students = convertObjectKeysToCamelCase(data).results
                    console.log(this.students)
                })
        }
    }
})