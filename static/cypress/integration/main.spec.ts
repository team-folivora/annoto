// https://docs.cypress.io/api/introduction/api.html

describe("Application", () => {
  it("visits the app root url", () => {
    cy.visit("/");
    cy.contains("h1", "Annoto");
  });
});
