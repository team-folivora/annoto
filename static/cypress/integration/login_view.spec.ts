import { interceptLoginWithFailure, login, setupIntercepts } from "./utils";

describe("LoginView", () => {
  it("logs the user in when valid login data is provided", () => {
    setupIntercepts();
    login().get("#tasks-overview");
  });

  it("warns if no password or email provided", () => {
    cy.visit("/").get("button#submit").click().get("div.alert.-warning");
  });

  it("errors if invalid login data provided", () => {
    setupIntercepts({ interceptLogin: interceptLoginWithFailure });
    login().get("div.alert.-danger");
  });
});
