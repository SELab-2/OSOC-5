import {beforeEach, describe, expect, it,  vi} from 'vitest'
import {createPinia, setActivePinia} from 'pinia'
import {useMailStore} from "../../src/stores/useMailStore";
import axios, { AxiosRequestConfig } from "axios"
import { instance } from '../../src/utils/axios'
import { UrlMockMappingGet, UrlMockMappingPost, UrlMockMappingPatch, UrlMockMappingDelete} from '../mockUrlMappings'
import { StudentInterface, Student} from '../../src/models/Student'
import { useAuthenticationStore } from '../../src/stores/useAuthenticationStore';
import { MailInterface, Mail } from '../../src/models/Mail';

const baseURL = 'https://sel2-5.ugent.be/api/'

const getcall_i = vi.spyOn(instance, 'get').mockImplementation((url: string, data?: unknown, config?:
    AxiosRequestConfig<unknown>) => Promise.resolve(JSON.parse(JSON.stringify(UrlMockMappingGet[url]))))
const postcall_i = vi.spyOn(instance, 'post').mockImplementation((url: string, data?: unknown, config?:
    AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingPost[url]))
const patchcall_i = vi.spyOn(instance, 'patch').mockImplementation((url: string, data?: unknown, config?:
    AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingPatch[url]))
const deletecall_i = vi.spyOn(instance, 'delete').mockImplementation((url: string, data?: unknown, config?:
    AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingDelete[url]))

describe('Skill Store', () => {
    beforeEach(() => {
        // creates a fresh pinia and make it active so it's automatically picked
        // up by any useStore() call without having to pass it to it:
        // `useStore(pinia)`
        setActivePinia(createPinia())
        getcall_i.mockClear()
        postcall_i.mockClear()
        patchcall_i.mockClear()
        deletecall_i.mockClear()
    })

    it('loadStudentsMails', async () => {

        const mailStore = useMailStore()
        await mailStore.loadStudentsMails({"test": "test"}, () => true)
        expect(mailStore.mailStudents).toHaveLength(1)

    })
    
    it('updateStatusStudents', async () => {

        const mailStore = useMailStore()
        let data = new Student((await instance.get<StudentInterface>('students/1/')).data)
        await mailStore.updateStatusStudents(1, [data])
        expect(postcall_i).toHaveBeenCalledTimes(1)
        
    })

    it('getMails', async () => {

        const mailStore = useMailStore()
        let data = new Student((await instance.get<StudentInterface>('students/1/')).data)
        expect(mailStore.mails.get(1)).toBeUndefined()
        await mailStore.getMails(data)
        expect(mailStore.mails.get(1)).toBeDefined()

    })

    it('updateStatus', async () => {

        const mailStore = useMailStore()
        let data = new Student((await instance.get<StudentInterface>('students/1/')).data)
        mailStore.updateStatus(data)
        expect(patchcall_i).toHaveBeenCalled()

    })

    it('sendMail', async () => {

        const mailStore = useMailStore()
        const authenticationStore = useAuthenticationStore()
        let fetchedUser = {id: 1, role: "nope", url: "coaches/1", firstName: "test", lastName: "test", email: "test", isAdmin: true, isActive: true} as User
        authenticationStore.loggedInUser = fetchedUser
        let data = new Student((await instance.get<StudentInterface>('students/1/')).data)
        mailStore.sendMail(data, 1, "2019-01-16", "THIS IS A TEST, I REPEAT, THIS IS A TEST")
        expect(postcall_i).toHaveBeenCalledOnce()

    })

    it('deleteMail', async () => {

        const mailStore = useMailStore()
        let data = new Mail((await instance.get<MailInterface>('emails/1')).data)
        mailStore.deleteMail(data)
        expect(deletecall_i).toHaveBeenCalledOnce()

    })
})