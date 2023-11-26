const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  pluginOptions: {
    electronBuilder: {
      customFileProtocol: "./",
      builderOptions: {
        productName: "Word Guard",
        win: {
          target: ["nsis"],
          icon: "public/icons/icon.png",
        },
        nsis: {
          installerIcon: "public/icons/icon.ico",
          uninstallerIcon: "public/icons/icon.ico",
        },
      },
    },
  },
});
