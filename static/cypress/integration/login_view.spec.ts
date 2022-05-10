import { intercept_login_with_failure, login, setup_intercepts } from "./utils";

describe("LoginView", () => {
  it("logs the user in when valid login data is provided", () => {
    setup_intercepts();
    login().get("#task-view");
  });

  it("warns if no password or email provided", () => {
    cy.visit("/")
      .get("button#submit")
      .click()
      .get("html")
      .contains("E-Mail and Password need to be set...");
  });

  it("errors if invalid login data provided", () => {
    setup_intercepts({ intercept_login: intercept_login_with_failure });
    login().get("html").contains("E-Mail or Password is not correct...");
  });
});
