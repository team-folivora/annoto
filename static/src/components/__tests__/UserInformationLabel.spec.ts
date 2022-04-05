import { mount } from "@cypress/vue";
import UserInformationLabel from "../UserInformationLabel.vue";

// TODO Label renders correctly

// TODO Label exists

describe("UserInformationLabel", () => {
    it("exists", () => {
      mount(UserInformationLabel, { props: { username: "" } });
    });


// TODO Label Input gets correctly handed to json