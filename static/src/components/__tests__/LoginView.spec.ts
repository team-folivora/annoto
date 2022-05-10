import { mount } from "@cypress/vue";
import LoginView from "../LoginView.vue";
import { ElMessage } from "element-plus";
import {
  intercept_login,
  intercept_login_with_failure,
} from "../../../cypress/integration/utils";
import { OpenAPI } from "@/api/core/OpenAPI";

beforeEach(() => {
  OpenAPI.BASE = "http://localhost:5000";
});

afterEach(() => {
  ElMessage.closeAll();
});

describe("LoginView", () => {
  it("exists", () => {
    mount(LoginView);
  });

  it("has a field for email", () => {
    mount(LoginView);
    cy.get("input[name='email']");
  });

  it("has a field for password", () => {
    mount(LoginView);
    cy.get("input[name='password']");
  });

  it("has a submit button", () => {
    mount(LoginView);
    cy.get("button#submit");
  });

  it("warns if no password set", () => {
    mount(LoginView);
    cy.get("input[name='email']")
      .type("testmail")
      .get("button#submit")
      .click()
      .get("html")
      .contains("E-Mail and Password need to be set...");
  });

  it("warns if no email set", () => {
    mount(LoginView);
    cy.get("input[name='password']")
      .type("password")
      .get("button#submit")
      .click()
      .get("html")
      .contains("E-Mail and Password need to be set...");
  });

  it("emits login with correct credentials", () => {
    // spying on the emitted events not working yet
    intercept_login();
    mount(LoginView);
    cy.get("input[name='email']")
      .type("team@folivora.online")
      .get("input[name='password']")
      .type("password")
      .get("button#submit")
      .click();
  });

  it("shows failure message with wrong credentials", () => {
    intercept_login_with_failure();
    mount(LoginView);
    cy.get("input[name='email']")
      .type("team@folivora.online")
      .get("input[name='password']")
      .type("password")
      .get("button#submit")
      .click()
      .get("html")
      .contains("E-Mail or Password is not correct...");
  });
});
