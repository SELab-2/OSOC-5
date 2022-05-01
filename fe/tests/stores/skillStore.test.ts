import {beforeEach, describe, expect, it, test} from 'vitest'
import {createPinia, setActivePinia} from 'pinia'
import {useSkillStore} from "../../src/stores/useSkillStore";

const baseURL = 'https://sel2-5.ugent.be/api/'

describe('Skill Store', () => {
    beforeEach(() => {
        // creates a fresh pinia and make it active so it's automatically picked
        // up by any useStore() call without having to pass it to it:
        // `useStore(pinia)`
        setActivePinia(createPinia())
    })

    it('getSkill: get invalid skill', () => {
        // if u can mock the instance of axios then we can check if the call is made

        // create a new skillstore
        const skillStore = useSkillStore()

        // check its initial values
        // expect(skillStore.skills).toHaveLength(0)
        expect(skillStore.isLoadingSkills).toBe(false)

        // test invalid
        // console.log(skillStore.skills)
        skillStore.getSkill(baseURL + "skills/1/")
        // console.log(skillStore.skills)
        skillStore.getSkill(baseURL + "skills/-1/")
        // console.log(skillStore.skills)

    })

    it('loadSkills', () => {

        // create a new skillstore
        const skillStore = useSkillStore()

        // check its initial values
        expect(skillStore.skills).toHaveLength(0)
        expect(skillStore.isLoadingSkills).toBe(false)

        // load skills
        skillStore.loadSkills()

        // check if it's loading skills
        expect(skillStore.isLoadingSkills).toBe(true)


    });
    it('addSkill', () => {

        // create a new skillstore
        const skillStore = useSkillStore()

        // check its initial values
        // expect(skillStore.skills).toHaveLength(0)
        expect(skillStore.isLoadingSkills).toBe(false)

        let callback_finished = false

        test.concurrent('add skill and wait', async () => {

            // add a skill and check if callback is executed
            skillStore.addSkill("newSkillName", "color", () => { callback_finished = true})
            expect(callback_finished).toBeTruthy()

        })


    });
    it('deleteSkill', () => {

        // create a new skillstore
        const skillStore = useSkillStore()

        // check its initial values
        // expect(skillStore.skills).toHaveLength(0)
        expect(skillStore.isLoadingSkills).toBe(false)

        // delete skill,
        // todo: would be nice in future if this deletes the skill that was previously made
        skillStore.deleteSkill(-1)

    })
})