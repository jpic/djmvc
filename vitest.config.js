import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'happy-dom',
    globals: true,
    include: [
      'src/djmvc_bulma/static/djmvc_bulma/js/form-focus.test.js',
      'src/djmvc_bulma/static/djmvc_bulma/js/filter-sidebar.test.js',
      'src/djmvc_bulma/static/djmvc_bulma/js/hamburger.test.js',
      'src/djmvc_bulma/static/djmvc_bulma/js/list-action-bar.test.js',
      'src/djmvc_bulma/static/djmvc_bulma/js/toast.test.js',
    ],
  },
})