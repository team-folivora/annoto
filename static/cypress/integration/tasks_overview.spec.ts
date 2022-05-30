import {
  openTask,
  interceptGetTasksWithEmptyList,
  login,
  setupIntercepts,
} from "./utils";

describe("TasksOverView", () => {
  it("shows full name", () => {
    setupIntercepts();
    login().get("#userLabel").contains("Prof. Dr. Folivora");
  });

  it("shows cards for tasks", () => {
    setupIntercepts();
    login().get(".card#task-ecg-qrs-classification-physiodb");
  });

  it("informs the user when there are no tasks", () => {
    setupIntercepts({
      interceptGetTasks: interceptGetTasksWithEmptyList,
    });
    login().get("#no-more-tasks");
  });

  it("shows the task view when a task was selected", () => {
    setupIntercepts();
    login()
      .then(() => openTask("ecg-qrs-classification-physiodb"))
      .get("#task-view");
  });
});
