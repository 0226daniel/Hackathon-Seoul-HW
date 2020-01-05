import Vue from 'vue';
import axios, { AxiosStatic } from 'axios';

const axi = axios.create({ baseURL: 'http://r.kdw.kr:9999' });
Vue.prototype.$axios = axi;

declare module 'vue/types/vue' {
  interface Vue {
    $axios: AxiosStatic;
  }
}

export default axi;
