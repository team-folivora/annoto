import {
  annotate,
  intercept_next_image_with_failure,
  login,
  proof_condition,
  setup_intercepts,
} from "./utils";

describe("TaskView", () => {
  it("shows full name", () => {
    setup_intercepts();
    login()
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .get("#userLabel").contains("Prof. Dr. Folivora");
  });

  it("shows the proof of condition popup on startup", () => {
    setup_intercepts();
    login()
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .get("#proof-of-condition").should("be.visible");
  });

  it("can close the proof of condition dialog when checkbox is checked", () => {
    setup_intercepts();
    login()
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .then(proof_condition)
      .get("#proof-of-condition")
      .should("not.be.visible");
  });

  it("cannot close the proof of condition dialog when checkbox is not checked", () => {
    setup_intercepts();
    login()
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .get("#proof-of-condition button")
      .click({ force: true })
      .get("#proof-of-condition")
      .should("be.visible");
  });

  it("informs the user when no more images are available for annotation", () => {
    setup_intercepts({
      intercept_next_image: intercept_next_image_with_failure,
    });
    login()
    cy.screenshot()
    cy.wait("@get_tasks")
    cy.screenshot()
    annotate("ecg-qrs-classification-physiodb")
    cy.screenshot()
    cy
      .wait("@get_next_image")
      .get("#no-more-images")
      .should("be.visible");
  });

  it("shows annotation buttons", () => {
    setup_intercepts();
    login()
      .wait("@get_tasks")
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .should("be.visible")
      .get("#annotation-button-other")
      .should("be.visible");
  });

  it("shows image display", () => {
    setup_intercepts();
    login()
      .wait("@get_tasks")
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .wait("@get_next_image")
      .get("#image-display")
      .should("be.visible");
  });

  it("annotation button stores annotation", () => {
    setup_intercepts();
    login()
      .wait("@get_tasks")
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .then(proof_condition)
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
    setup_intercepts();
    login()
      .wait("@get_tasks")
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .click({ force: true })
      .wait("@store_annotation")
      .get("@store_annotation_spy")
      .its("args.0.0.body")
      .should("deep.include", { is_attentive: false });
  });

  it("shows next image once annotation has been made", () => {
    setup_intercepts();
    login()
      .wait("@get_tasks")
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .then(proof_condition)
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .click()
      .wait("@get_next_image")
      .get("#image-display")
      .should("be.visible");
  });
});
