import { defineStore } from "pinia";
import { ref } from "vue";

export const usePathStore = defineStore("PathStore", () => {
  
  const file_path = ref("");
  const output_path = ref("");
  const file_name = ref("");
  const full_path=ref("");

  return { file_path, output_path,file_name,full_path };
});
