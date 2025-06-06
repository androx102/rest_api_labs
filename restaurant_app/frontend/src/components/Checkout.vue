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
                {{ formatPrice(item.price * item.quantity) }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
          <v-divider></v-divider>
          <v-card-text class="text-right">
            <p class="text-h6">Total: {{ formatPrice(cartTotal) }}</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Customer Details Form -->
      <v-col cols="12" md="6">
        <v-form
          ref="form"
          v-model="isFormValid"
          @submit.prevent="submitOrder"
        >
          <v-card>
            <v-card-title>Customer Details</v-card-title>
            <v-card-text>
              <v-text-field
                v-model="formData.customer_name"
                label="Name"
                :rules="[rules.required]"
                clearable
              ></v-text-field>

              <v-text-field
                v-model="formData.customer_email"
                label="Email"
                :rules="[rules.required, rules.email]"
              ></v-text-field>

              <v-text-field
                v-model="formData.customer_phone"
                label="Phone Number"
                :rules="[rules.required, rules.phone]"
                clearable
              ></v-text-field>

              <v-textarea
                v-model="formData.delivery_address"
                label="Delivery Address*"
                :rules="[rules.required]"
                rows="3"
                auto-grow
              ></v-textarea>
            </v-card-text>
          </v-card>

          <v-btn
            color="primary"
            block
            size="large"
            type="submit"
            :loading="isSubmitting"
            :disabled="!isFormValid || isSubmitting"
          >
            Place Order
          </v-btn>
        </v-form>
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
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'

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
const currentCurrency = computed(() => store.getters.currentCurrency)
const isAuthenticated = computed(() => store.getters.isAuthenticated)

const formData = ref({
  customer_name: '',
  customer_email: '',
  customer_phone: '',
  delivery_address: ''
})

const rules = {
  required: v => !!v || 'This field is required',
  email: v => /.+@.+\..+/.test(v) || 'Email must be valid',
  phone: v => !v || /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/.test(v) || 'Please enter a valid phone number'
}

const formatPrice = (price) => {
  return store.getters.formatPrice(price)
}

const submitOrder = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  isSubmitting.value = true
  
  try {
    // Prepare order items with original PLN prices
    const items = cartItems.value.map(item => ({
      menu_item: item.id,
      quantity: item.quantity,
      price: item.originalPrice || item.price // Use original PLN price if available
    }))

    const orderData = {
      customer_name: formData.value.customer_name,
      customer_email: formData.value.customer_email,
      customer_phone: formData.value.customer_phone,
      delivery_address: formData.value.delivery_address,
      items: items,
      currency: currentCurrency.value // Send current currency info to backend
    }

    // Log the request data for debugging
    console.log('Sending order data:', orderData)

    // Send order to backend
    const response = await axios.post('http://127.0.0.1:8000/api/v1/orders/', orderData, {
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

// Fetch and fill user data if authenticated
onMounted(async () => {
  if (isAuthenticated.value) {
    try {
      const response = await axios.get('/user/')
      formData.value = {
        ...formData.value,
        customer_name: response.data.name || '',
        customer_email: response.data.email || '',
        customer_phone: response.data.phone_number || '',
        delivery_address: response.data.delivery_address || ''
      }
    } catch (err) {
      console.error('Failed to fetch user data:', err)
    }
  }
})
</script>