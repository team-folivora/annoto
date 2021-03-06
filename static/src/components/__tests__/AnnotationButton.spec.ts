import { mount } from "@cypress/vue";
import AnnotationButton from "@/components/AnnotationButton.vue";

describe("Button", () => {
  it("exists", () => {
    mount(AnnotationButton, {
      props: {
        label: "Test",
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
  });

  it("renders properly", () => {
    mount(AnnotationButton, {
      props: {
        label: "Test",
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
    cy.get("i-button").should("be.visible");
  });

  it("is not disabled", () => {
    mount(AnnotationButton, {
      props: {
        label: "Test",
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
    cy.get("i-button").should("not.be.disabled");
  });

  it("shows specific label", () => {
    const label = "Cypress";
    mount(AnnotationButton, {
      props: {
        label: label,
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
    cy.get("i-button").contains(label);
  });
});
