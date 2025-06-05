<template>
  <div class="checkout">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h3 mb-6">Checkout</h1>
        </v-col>
      </v-row>

      <div v-if="cartItemCount > 0">
        <Checkout />
      </div>
      
      <div v-else>
        <v-card>
          <v-card-text class="text-center pa-8">
            <v-icon size="64" color="grey">mdi-cart-outline</v-icon>
            <p class="text-h5 mt-4">Your cart is empty</p>
            <v-btn
              color="primary"
              class="mt-4"
              to="/menu"
            >
              Browse Menu
            </v-btn>
          </v-card-text>
        </v-card>
      </div>
    </v-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Checkout from '@/components/Checkout.vue'

const store = useStore()
const cartItemCount = computed(() => store.getters.cartItemCount)
</script>