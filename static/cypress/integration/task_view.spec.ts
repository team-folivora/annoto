import {
  intercept_get_task,
  intercept_next_image,
  intercept_next_image_with_failure,
  login,
} from "./utils";

describe("TaskView", () => {
  it("shows username", () => {
    intercept_get_task();
    intercept_next_image();
    login().get("#userLabel").contains("AnnotoUser#1337");
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
});
