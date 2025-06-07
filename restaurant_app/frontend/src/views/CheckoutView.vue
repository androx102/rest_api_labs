<template>
  <div class="checkout">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h3 mb-6">Checkout</h1>
        </v-col>
      </v-row>

      <div v-if="cartItemCount > 0">
        <div v-if="!showPayment">
          <Checkout @order-confirmed="handleOrderConfirmed" />
        </div>
        
        <div v-else>
          <v-card>
            <v-card-title>Payment</v-card-title>
            <v-card-text class="text-center">
              <v-alert
                v-if="paymentError"
                type="error"
                class="mb-4"
              >
                {{ paymentError }}
              </v-alert>

              <v-progress-circular
                v-if="isLoading"
                indeterminate
                color="primary"
                size="64"
              ></v-progress-circular>
              
              <p v-else class="text-body-1">
                Redirecting to payment page...
              </p>
            </v-card-text>
          </v-card>
        </div>
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
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import Checkout from '@/components/Checkout.vue'
import axios from '@/utils/axios'

const store = useStore()
const router = useRouter()

const showPayment = ref(false)
const paymentError = ref('')
const isLoading = ref(false)
const cartItemCount = computed(() => store.getters.cartItemCount)
const cartTotal = computed(() => store.getters.cartTotal)
const currentCurrency = computed(() => store.getters.currentCurrency)

const handleOrderConfirmed = async (orderData) => {
  isLoading.value = true
  paymentError.value = ''
  
  try {
    // Initialize payment
    const response = await axios.post('/payment/initialize/', {
      orderNumber: orderData.orderNumber,
      currency: currentCurrency.value
    })

    if (response.data.status === 'success' && response.data.redirectUri) {
      // Clear cart before redirect
      store.commit('clearCart')
      
      // Redirect to PayU payment page
      window.location.href = response.data.redirectUri
    } else {
      throw new Error('Invalid response from payment server')
    }

  } catch (err) {
    console.error('Payment error:', err)
    paymentError.value = 'Failed to initialize payment. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>