import { mount } from "@cypress/vue";
import AnnotationButton from "../AnnotationButton.vue";

describe("Button", () => {
  it("exists", () => {
    mount(AnnotationButton);
  });

  it("renders properly", () => {
    mount(AnnotationButton);
    cy.get("button").should("be.visible");
  });

  it("is not disabled", () => {
    mount(AnnotationButton);
    cy.get("button").should("not.be.disabled");
  });

  it("shows specific label", () => {
    const str = "Label: ";
    mount(AnnotationButton, { props: {} });
    cy.get("button").contains(str);
  });
});
