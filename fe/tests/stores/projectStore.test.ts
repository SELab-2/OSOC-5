import { beforeEach, describe, expect, it, test } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useProjectStore } from "../../src/stores/useProjectStore";
import { Project } from "../../src/models/Project";
import { ProjectSuggestionInterface } from "../../src/models/ProjectSuggestion";

const baseURL = "https://sel2-5.ugent.be/api/";

describe("Skill Store", () => {
  beforeEach(() => {
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia());
  });

  it("removeSuggestion", () => {

    // create a new skillstore
    const projectStore = useProjectStore();

    // check its initial values
    // expect(projectStore.skills).toHaveLength(0)
    expect(projectStore.isLoadingProjects).toBe(false);

    // let callback_finished = false;

    test.concurrent("remove suggestion and wait", async () => {

      // add a skill and check if callback is executed
      const project: Project =
        {
          "name": "name",
          "partnerName": "partnerName",
          "extraInfo": "extraInfo",
          "id": 0
        };
      // @ts-ignore
      projectStore.removeSuggestion(project, undefined);
      // expect(callback_finished).toBeTruthy();

    });


  });
});