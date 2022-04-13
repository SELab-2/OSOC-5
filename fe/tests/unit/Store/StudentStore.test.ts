import { setActivePinia, createPinia } from 'pinia'
import {useStudentStore} from "../../../src/stores/useStudentStore";
import axios from "axios";

describe('Example Store', () => {
    beforeEach(() => {
        // creates a fresh pinia and make it active so it's automatically picked
        // up by any useStore() call without having to pass it to it:
        // `useStore(pinia)`
        setActivePinia(createPinia())
    })

    it('Initialization', () => {
        const store = useStudentStore()
        expect(store.search).toBe("")
        expect(store.alumni).toBe("all")
        expect(store.decision).toBe("none")
        expect(store.byMe).toBe(false)
        expect(store.onProject).toBe(false)
        expect(store.skills.length).toBe(0)
        expect(store.students.length).toBe(0)
        expect(store.isLoading).toBe(false)
        expect(store.possibleSuggestion).toBe(-1)
        expect(store.currentStudent).toBe(null)
    })

    // it('Load students', async () => {
    //     const mock = new MockAdapter(axios);
    //
    //     mock.onGet('/students').reply(200, data)
    // })
})
