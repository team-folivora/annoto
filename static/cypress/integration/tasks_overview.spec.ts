import {
  annotate,
  intercept_get_tasks_with_empty_list,
  login,
  setup_intercepts,
} from "./utils";

describe("TasksOverView", () => {
  it("shows full name", () => {
    setup_intercepts();
    login().get("#userLabel").contains("Prof. Dr. Folivora");
  });

  it("shows cards for tasks", () => {
    setup_intercepts();
    login().get(".card#task-ecg-qrs-classification-physiodb");
  });

  it("informs the user when there are no tasks", () => {
    setup_intercepts({
      intercept_get_tasks: intercept_get_tasks_with_empty_list,
    });
    login().get("#no-more-tasks");
  });

  it("shows the task view when a task was selected", () => {
    setup_intercepts();
    login()
      .then(() => annotate("ecg-qrs-classification-physiodb"))
      .get("#task-view");
  });
});
