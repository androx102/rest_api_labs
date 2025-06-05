<template>
  <v-container>
    <v-row>
      <!-- Order Summary -->
      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-card-title>Order Summary</v-card-title>
          <v-list>
            <v-list-item v-for="item in cartItems" :key="item.id">
              <v-list-item-title>
                {{ item.name }} x {{ item.quantity }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ (item.price * item.quantity).toFixed(2) }} PLN
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
          <v-divider></v-divider>
          <v-card-text class="text-right">
            <p class="text-h6">Total: {{ cartTotal }} PLN</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Customer Details Form -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Customer Details</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="isFormValid">
              <v-text-field
                v-model="formData.customer_name"
                label="Full Name"
                :rules="[(v) => !!v || 'Name is required']"
                required
              ></v-text-field>

              <v-text-field
                v-model="formData.customer_email"
                label="Email"
                type="email"
                :rules="[
                  (v) => !!v || 'Email is required',
                  (v) => /.+@.+\..+/.test(v) || 'Email must be valid'
                ]"
                required
              ></v-text-field>

              <v-text-field
                v-model="formData.customer_phone"
                label="Phone Number"
                :rules="[(v) => !!v || 'Phone number is required']"
                required
              ></v-text-field>

              <v-textarea
                v-model="formData.delivery_address"
                label="Delivery Address"
                :rules="[(v) => !!v || 'Delivery address is required']"
                required
              ></v-textarea>

              <v-btn
                color="primary"
                block
                size="large"
                :loading="isSubmitting"
                :disabled="!isFormValid || isSubmitting"
                @click="submitOrder"
              >
                Place Order
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success/Error Alerts -->
    <v-snackbar
      v-model="showSuccess"
      color="success"
      timeout="3000"
    >
      Order placed successfully! Your order number is: {{ orderNumber }}
    </v-snackbar>

    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'

const store = useStore()
const router = useRouter()

const form = ref(null)
const isFormValid = ref(false)
const isSubmitting = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const orderNumber = ref('')

const cartItems = computed(() => store.state.cart.items)
const cartTotal = computed(() => store.getters.cartTotal)

const formData = ref({
  customer_name: '',
  customer_email: '',
  customer_phone: '',
  delivery_address: ''
})

const submitOrder = async () => {
  if (!form.value.validate()) return

  isSubmitting.value = true
  
  try {
    // Prepare order items
    const items = cartItems.value.map(item => ({
      menu_item: item.id,
      quantity: item.quantity
    }))

    // Prepare order data - don't stringify items array
    const orderData = {
      customer_name: formData.value.customer_name,
      customer_email: formData.value.customer_email,
      customer_phone: formData.value.customer_phone,
      delivery_address: formData.value.delivery_address,
      items: items  // Send as array, not stringified
    }

    // Log the request data for debugging
    console.log('Sending order data:', orderData)

    // Send order to backend
    const response = await axios.post('http://127.0.0.1:8000/api/orders/', orderData, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    console.log('Order response:', response.data)
    
    // Handle success
    orderNumber.value = response.data.order_number_uuid
    showSuccess.value = true
    
    // Clear cart
    store.commit('clearCart')
    
    // Redirect to order confirmation after a short delay
    setTimeout(() => {
      router.push({
        name: 'order',
        query: { 
          order: orderNumber.value,
          email: formData.value.customer_email
        }
      })
    }, 2000)

  } catch (error) {
    // Enhanced error handling
    console.error('Order error:', error.response?.data || error.message)
    errorMessage.value = error.response?.data?.error || 'Failed to place order'
    showError.value = true
  } finally {
    isSubmitting.value = false
  }
}
</script>