import {
  intercept_get_task,
  intercept_next_image,
  intercept_next_image_with_failure,
  intercept_store_annotation,
  login,
  proof_condition,
  intercept_get_image,
} from "./utils";

describe("TaskView", () => {
  it("shows username", () => {
    intercept_get_task();
    intercept_next_image();
    login().get("#userLabel").contains("AnnotoUser#1337");
  });

  it("shows the proof of condition popup on startup", () => {
    intercept_get_task();
    intercept_next_image();
    login().get("#proof-of-condition").should("be.visible");
  });

  it("can close the proof of condition dialog when checkbox is checked", () => {
    intercept_get_task();
    intercept_next_image();
    login()
      .then(proof_condition)
      .get("#proof-of-condition")
      .should("not.be.visible");
  });

  it("cannot close the proof of condition dialog when checkbox is not checked", () => {
    intercept_get_task();
    intercept_next_image();
    login()
      .get("#proof-of-condition button")
      .click({ force: true })
      .get("#proof-of-condition")
      .should("be.visible");
  });

  it("informs the user when no more images are available for annotation", () => {
    intercept_get_task();
    intercept_next_image_with_failure();
    login()
      .wait("@get_task")
      .wait("@get_next_image")
      .get("#no-more-images")
      .should("be.visible");
  });

  it("shows annotation buttons", () => {
    intercept_get_task();
    intercept_next_image();
    login()
      .wait("@get_task")
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .should("be.visible")
      .get("#annotation-button-other")
      .should("be.visible");
  });

  it("shows image display", () => {
    intercept_get_task();
    intercept_next_image();
    login()
      .wait("@get_task")
      .wait("@get_next_image")
      .get("#image-display")
      .should("be.visible");
  });

  it("annotation button stores annotation", () => {
    intercept_get_task();
    intercept_next_image();
    intercept_get_image();
    intercept_store_annotation();
    login()
      .then(proof_condition)
      .wait("@get_task")
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .click()
      .wait("@store_annotation")
      .get("@store_annotation_spy")
      .its("args.0.0.body")
      .should("deep.include", { is_attentive: true });
  });

  it("annotation request includes condition from popup", () => {
    cy.on("uncaught:exception", () => false);
    intercept_get_task();
    intercept_next_image();
    intercept_get_image();
    intercept_store_annotation();
    login()
      .wait("@get_task")
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .click({ force: true })
      .wait("@store_annotation")
      .get("@store_annotation_spy")
      .its("args.0.0.body")
      .should("deep.include", { is_attentive: false });
  });

  it("shows next image once annotation has been made", () => {
    intercept_get_task();
    intercept_next_image();
    intercept_get_image();
    intercept_store_annotation();
    login()
      .then(proof_condition)
      .wait("@get_task")
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .click()
      .wait("@get_next_image")
      .get("#image-display")
      .should("be.visible");
  });
});
