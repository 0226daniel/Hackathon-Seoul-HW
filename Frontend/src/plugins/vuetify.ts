import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import ko from 'vuetify/src/locale/ko';

Vue.use(Vuetify);

export default new Vuetify({
  lang: {
    locales: { ko },
    current: 'ko',
  },
  theme: {
    dark: true,
  },
});
