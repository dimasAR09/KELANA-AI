const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: "tgdit5",

  e2e: {
    baseUrl: "https://kelana-ai-henna.vercel.app" ,
    setupNodeEvents(on, config) {

    },
  },

  component: {
    devServer: {
      framework: "react",
      bundler: "webpack",
    },
  },
});
