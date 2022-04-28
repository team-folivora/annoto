import { intercept_login, intercept_login_with_failure } from "./utils";

describe("LoginView", () => {
  it("logs the user in when valid login data is provided", () => {
    intercept_login();
    intercept_get_task();
    intercept_next_image();
    cy.visit("/")
      .get("input[name='username']")
      .type("AnnotoUser#1337")
      .get("input[name='password']")
      .type("test1234")
      .get("button#submit")
      .click()
      .wait("@login")
      .get("#task-view");
  });

  it("warns if no password or username provided", () => {
    cy.visit("/").get("button#submit").click().get("div.alert.-warning");
  });

  it("errors if invalid login data provided", () => {
    intercept_login_with_failure();
    cy.visit("/")
      .get("input[name='username']")
      .type("AnnotoUser#1337")
      .get("input[name='password']")
      .type("wrong_password")
      .get("button#submit")
      .click()
      .wait("@login")
      .get("div.alert.-danger");
  });
});
