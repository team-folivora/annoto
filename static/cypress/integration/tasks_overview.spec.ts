import {
  openTask,
  interceptGetTasksWithEmptyList,
  login,
  setupIntercepts,
} from "./utils";
import { task } from "../fixtures/fixture_objects";

describe("TasksOverView", () => {
  it("shows full name", () => {
    setupIntercepts();
    login().get("#userLabel").contains("Prof. Dr. Folivora");
  });

  it("shows cards for tasks", () => {
    setupIntercepts();
    login().get(`.card#task-${task.id}`);
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
      .then(() => openTask(task.id))
      .url()
      .should("include", `/tasks/${task.id}`);
  });
});
