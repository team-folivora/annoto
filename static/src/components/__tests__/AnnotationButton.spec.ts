import { mount } from "@cypress/vue";
import AnnotationButton from "../AnnotationButton.vue";

describe("Button", () => {
  it("exists", () => {
    mount(AnnotationButton), {probs: { text: String }};
  });

  it("renders properly", () => {
    mount(AnnotationButton), {probs: { text: String }};
    cy.get("button").should("be.visible");
  });

  it("is not disabled", () => {
    mount(AnnotationButton), {probs: { text: String }};
    cy.get("button").should("not.be.disabled");
  });

  it("shows specific label", () => {
    const str = "Label: ";
    mount(AnnotationButton), {probs: { text: String }};
    cy.get("button").contains(str);
  });
});
