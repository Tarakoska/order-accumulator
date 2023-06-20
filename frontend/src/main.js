import { createApp } from 'vue';
import App from './App.vue';
import VueCookies from 'vue3-cookies';
import VueClipboard from 'vue3-clipboard';

let app = createApp(App);
app.use(VueCookies);
app.use(VueClipboard, {
  autoSetContainer: true,
  appendToBody: true,
});
app.mount('#app');
