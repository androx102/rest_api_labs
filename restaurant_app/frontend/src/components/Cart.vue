<template>
  <v-row v-if="cartItems.length > 0">
    <v-col cols="12">
      <v-card>
        <v-list>
          <v-list-item
            v-for="item in cartItems"
            :key="item.id"
            class="mb-2"
          >
            <v-list-item-title class="text-h6">
              {{ item.name }}
            </v-list-item-title>

            <v-list-item-subtitle>
              Price: {{ formatPrice(item.price) }} x {{ item.quantity }}
              = {{ formatPrice(item.price * item.quantity) }}
            </v-list-item-subtitle>

            <template v-slot:append>
              <div class="d-flex align-center">
                <v-btn
                  icon="mdi-minus"
                  variant="text"
                  @click="updateQuantity(item.id, item.quantity - 1)"
                  :disabled="item.quantity <= 1"
                ></v-btn>

                <span class="mx-2">{{ item.quantity }}</span>

                <v-btn
                  icon="mdi-plus"
                  variant="text"
                  @click="updateQuantity(item.id, item.quantity + 1)"
                ></v-btn>

                <v-btn
                  icon="mdi-delete"
                  color="error"
                  variant="text"
                  class="ml-4"
                  @click="removeFromCart(item.id)"
                ></v-btn>
              </div>
            </template>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-card-text class="text-right">
          <p class="text-h6">
            Total: {{ formatPrice(cartTotal) }}
          </p>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <v-row v-else>
    <v-col cols="12">
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
    </v-col>
  </v-row>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const cartItems = computed(() => store.state.cart.items)
const cartTotal = computed(() => store.getters.cartTotal)
const currentCurrency = computed(() => store.getters.currentCurrency)
const currencySymbol = computed(() => store.getters.currencySymbol)

const formatPrice = (price) => {
  return store.getters.formatPrice(price)
}

const updateQuantity = (id, quantity) => {
  if (quantity < 1) return
  store.dispatch('updateCartItemQuantity', { id, quantity })
}

const removeFromCart = (id) => {
  store.dispatch('removeFromCart', id)
}
</script>

<style scoped>
.v-list-item {
  margin-bottom: 8px;
}
</style>