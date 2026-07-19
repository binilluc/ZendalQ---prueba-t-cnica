// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  // SPA mode: this is a small internal tool with no SEO needs, and it avoids
  // having to juggle two different API base URLs (container-internal for SSR
  // vs public for the browser) inside Docker.
  ssr: false,
  css: ['~/assets/css/main.css'],
  // Components live under feature subfolders (components/tickets/…); keep
  // auto-import names as the bare filename instead of prefixing them with
  // the folder (TicketForm, not TicketsTicketForm).
  components: [{ path: '~/components', pathPrefix: false }],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  }
})
