// src/vue-plugin.d.ts

import { Router } from 'vue-router';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $redirectTo: (routeName: string) => void;
  }
}
