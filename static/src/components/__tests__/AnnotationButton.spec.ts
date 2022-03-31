import { mount } from "@cypress/vue";
import AnnotationButton from "../AnnotationButton.vue";

describe("Button", () => {
  it("exists", () => {
    mount(AnnotationButton, { props: { text: "Test" } });
  });

  it("renders properly", () => {
    mount(AnnotationButton, { props: { text: "Test" } });
    cy.get("button").should("be.visible");
  });

  it("is not disabled", () => {
    mount(AnnotationButton, { props: { text: "Test" } });
    cy.get("button").should("not.be.disabled");
  });

  it("shows specific label", () => {
    const label = "Cypress";
    mount(AnnotationButton, { props: { text: label } });
    cy.get("button").contains(label);
  });
});
