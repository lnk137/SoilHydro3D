import { defineStore } from "pinia";
import { ref } from "vue";

export const useUrlStore = defineStore("UrlStore", () => {
  
  const server_url = ref("http://127.0.0.1:4201");

  return { server_url };
});
