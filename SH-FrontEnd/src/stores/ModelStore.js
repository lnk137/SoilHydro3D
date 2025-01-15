import { defineStore } from "pinia";
import { ref } from "vue";

export const useModelStore = defineStore("ModelStore", () => {
  const layer_thickness = ref(1);
  const type = ref("");
  const target = ref("");

  return { layer_thickness, type };
});
