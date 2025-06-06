<template>
  <div class="my-orders">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h3 mb-6">My Orders</h1>
        </v-col>
      </v-row>

      <OrdersList />
    </v-container>
  </div>
</template>

<script setup>
import OrdersList from '@/components/OrdersList.vue'
</script>