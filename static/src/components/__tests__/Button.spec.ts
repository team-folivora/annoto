import { mount } from "@cypress/vue";
import Button from "../Button.vue";

describe("Button", () => {
  it("exists", () => {
    mount(Button);
  });

  it("renders properly", () => {
    mount(Button);
    cy.get("button").should("be.visible");
  });

  it("is not disabled", () => {
    mount(Button);
    cy.get("button").should("not.be.disabled");
  });

  it("shows specific label", () => {
    const str = "Label: ";
    mount(Button, { props: {} });
    cy.get("button").contains(str);
  });
});
