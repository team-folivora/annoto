import {
  intercept_get_task,
  intercept_login,
  intercept_login_with_failure,
  intercept_next_image,
  login,
} from "./utils";

describe("LoginView", () => {
  it("logs the user in when valid login data is provided", () => {
    login().get("#task-view");
  });

  it("warns if no password or username provided", () => {
    cy.visit("/").get("button#submit").click().get("div.alert.-warning");
  });

  it("errors if invalid login data provided", () => {
    login({ intercept_login: intercept_login_with_failure }).get(
      "div.alert.-danger"
    );
  });
});
