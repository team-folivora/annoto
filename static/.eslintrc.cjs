/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  root: true,
  extends: [
    "plugin:vue/vue3-recommended",
    "eslint:recommended",
    "@vue/eslint-config-typescript/recommended",
    "@vue/eslint-config-prettier",
    "prettier",
  ],
  rules: {
    "vue/attributes-order": "error",
    "vue/order-in-components": "error",
  },
  env: {
    "vue/setup-compiler-macros": true,
  },
  overrides: [
    {
      files: [
        "**/__tests__/*.spec.{js,ts,jsx,tsx}",
        "cypress/integration/**.spec.{js,ts,jsx,tsx}",
      ],
      extends: ["plugin:cypress/recommended"],
    },
  ],
};
