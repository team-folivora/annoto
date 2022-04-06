import { mount } from "@cypress/vue";
import AnnotationButton from "../AnnotationButton.vue";

describe("Button", () => {
  it("exists", () => {
    mount(AnnotationButton, {
      props: { label: "Test", src: "/images/test.jpg", competency: "Dr.", isAttentive: true },
    });
  });

  it("renders properly", () => {
    mount(AnnotationButton, {
      props: { label: "Test", src: "/images/test.jpg", competency: "Dr.", isAttentive: true },
    });
    cy.get("i-button").should("be.visible");
  });

  it("is not disabled", () => {
    mount(AnnotationButton, {
      props: { label: "Test", src: "/images/test.jpg", competency: "Dr.", isAttentive: true },
    });
    cy.get("i-button").should("not.be.disabled");
  });

  it("shows specific label", () => {
    const label = "Cypress";
    mount(AnnotationButton, {
      props: { label: label, src: "/images/test.jpg", competency: "Dr.", isAttentive: true },
    });
    cy.get("i-button").contains(label);
  });
});
