import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'happy-dom',
    globals: true,
    include: [
      'src/djmvc_bulma/static/djmvc_bulma/js/hamburger.test.js',
    ],
  },
})