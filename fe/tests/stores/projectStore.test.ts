import { beforeEach, describe, expect, it, test } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useProjectStore } from "../../src/stores/useProjectStore";
import { Project } from "../../src/models/Project";
import { ProjectSuggestionInterface } from "../../src/models/ProjectSuggestion";


describe("Project Store", () => {
  beforeEach(() => {
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia());
  });

  it("fetchSuggestedStudents", async () => {

  })

});