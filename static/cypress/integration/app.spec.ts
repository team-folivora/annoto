describe("Application", () => {
  it("visits the app root url", () => {
    cy.visit("/").contains("h1", "Annoto");
  });
});
