import { mount } from "@cypress/vue";
import ImageDisplay from "../ImageDisplay.vue";

describe("ImageDisplay", () => {
  it("exists", () => {
    mount(ImageDisplay, {
      props: {
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
      },
    });
  });

  it("renders properly", () => {
    mount(ImageDisplay, {
      props: {
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
      },
    });
    cy.get("img")
      .invoke("attr", "src")
      .should(
        "eq",
        "http://localhost:5000/tasks/ecg-qrs-classification-physiodb/sloth.jpg?"
      );
  });
});
