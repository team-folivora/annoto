import { mount } from "@cypress/vue";
import ImageDisplay from "../ImageDisplay.vue";

describe("ImageDisplay", () => {
  it("playground", () => {
    mount(ImageDisplay, { props: { src: "image_url" } });
  });

  it("renders properly", () => {
    mount(ImageDisplay, { props: { src: "image_url" } });
    cy.get("img").invoke("attr", "src").should("eq", "image_url");
  });
});
