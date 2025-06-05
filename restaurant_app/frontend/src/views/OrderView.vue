<template>
  <div class="order">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h3 mb-6">Track Order</h1>
        </v-col>
      </v-row>

      <!-- Order Lookup Form -->
      <v-row v-if="!orderDetails">
        <v-col cols="12" md="6" class="mx-auto">
          <v-card>
            <v-card-title>Find Your Order</v-card-title>
            <v-card-text>
              <v-form ref="form" v-model="isFormValid">
                <v-text-field
                  v-model="orderNumber"
                  label="Order Number"
                  :rules="[(v) => !!v || 'Order number is required']"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="email"
                  label="Email"
                  type="email"
                  :rules="[
                    (v) => !!v || 'Email is required',
                    (v) => /.+@.+\..+/.test(v) || 'Email must be valid'
                  ]"
                  required
                ></v-text-field>

                <v-btn
                  color="primary"
                  block
                  :loading="isLoading"
                  :disabled="!isFormValid || isLoading"
                  @click="trackOrder"
                >
                  Track Order
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Order Details -->
      <v-row v-else>
        <v-col cols="12">
          <OrderDetails 
            :order="orderDetails"
            @back="orderDetails = null"
          />
        </v-col>
      </v-row>

      <!-- Error Alert -->
      <v-snackbar
        v-model="showError"
        color="error"
        timeout="3000"
      >
        {{ errorMessage }}
      </v-snackbar>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import OrderDetails from '@/components/OrderDetails.vue'

const route = useRoute()
const form = ref(null)
const isFormValid = ref(false)
const isLoading = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const orderDetails = ref(null)

const orderNumber = ref(route.query.order || '')
const email = ref(route.query.email || '')

const trackOrder = async () => {
  if (!form.value.validate()) return
  
  isLoading.value = true
  try {
    // Add email as query parameter
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/orders/${orderNumber.value}?email=${encodeURIComponent(email.value)}`
    )
    orderDetails.value = response.data
    console.log('Order details:', response.data)  // Debug log
  } catch (error) {
    console.error('Track order error:', error.response?.data)
    errorMessage.value = error.response?.data?.error || 'Failed to find order'
    showError.value = true
  } finally {
    isLoading.value = false
  }
}

// Auto-track if order number and email are in URL
onMounted(() => {
  if (orderNumber.value && email.value) {
    trackOrder()
  }
})
</script>