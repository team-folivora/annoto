import { login, setup_intercepts } from "./utils";

describe("TasksOverView", () => {
  it("shows full name", () => {
    setup_intercepts();
    login().get("#userLabel").contains("Prof. Dr. Folivora");
  });

  it("shows cards for tasks", () => {
    setup_intercepts();
    login().get(".card#task-ecg-qrs-classification-physiodb");
  });
});
