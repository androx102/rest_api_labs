<template>
  <div class="cart">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h3 mb-6">My Cart</h1>
        </v-col>
      </v-row>
      
      <Cart />
      
      <v-row v-if="cartItemCount > 0">
        <v-col cols="12" class="text-right">
          <v-btn
            color="primary"
            size="large"
            to="/checkout"
          >
            Proceed to Checkout ({{ cartTotal }} PLN)
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Cart from '@/components/Cart.vue'

const store = useStore()
const cartItemCount = computed(() => store.getters.cartItemCount)
const cartTotal = computed(() => store.getters.cartTotal)
</script>