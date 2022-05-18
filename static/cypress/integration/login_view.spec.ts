import { intercept_login_with_failure, login, setup_intercepts } from "./utils";

describe("LoginView", () => {
  it("logs the user in when valid login data is provided", () => {
    setup_intercepts();
    login().get("#tasks-overview");
  });

  it("warns if no password or email provided", () => {
    cy.visit("/").get("button#submit").click().get("div.alert.-warning");
  });

  it("errors if invalid login data provided", () => {
    setup_intercepts({ intercept_login: intercept_login_with_failure });
    login().get("div.alert.-danger");
  });
});
