// counterStore.spec.ts
import { setActivePinia, createPinia } from 'pinia'
import {useSkillStore} from "../../../src/stores/useSkillStore";

describe('Example Store', () => {
    beforeEach(() => {
        // creates a fresh pinia and make it active so it's automatically picked
        // up by any useStore() call without having to pass it to it:
        // `useStore(pinia)`
        setActivePinia(createPinia())
    })

    it('store example', () => {
        const store = useSkillStore()
        expect(store.skills.length).toBe(0);
    })

})