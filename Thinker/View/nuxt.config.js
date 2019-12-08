module.exports = {
  /*
   ** Headers of the page
   */
  head: {
    title: "puzzle",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "Nuxt.js project" }
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }]
  },
  modules: ["@nuxtjs/axios", "@nuxtjs/proxy"],
  proxy: {
    "/api": {
      target: "http://puzzle.iwanhae.ga",
      pathRewrite: {
        "^/api": "/"
      }
    },
    "/php": {
      target: "https://php.iwanhae.ga"
    }
  },
  /*
   ** Customize the progress bar color
   */
  loading: { color: "#3B8070" },
  css: ["assets/open-color.css"],
  /*
   ** Build configuration
   */
  build: {
    /*
     ** Run ESLint on save
     */
    extend(config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: "pre",
          test: /\.(js|vue)$/,
          loader: "eslint-loader",
          exclude: /(node_modules)/
        });
      }
    }
  }
};
