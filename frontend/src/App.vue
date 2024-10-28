<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
 
  <v-container fluid class="pa-0 ma-0" style="
      background: rgb(34, 193, 195) !important;
      background: linear-gradient(90deg, rgba(34, 193, 195, 1) 50%, rgba(45, 126, 253, 1) 100%) !important;
      min-height: 100vh;
    ">
    <RouterView />
  </v-container>

</template>


