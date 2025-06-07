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
                {{ store.getters.formatPrice(item.price * item.quantity) }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
          <v-divider></v-divider>
          <v-card-text class="text-right">
            <p class="text-h6">Total: {{ store.getters.formatPrice(cartTotal) }}</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Customer Details Form -->
      <v-col cols="12" md="6">
        <v-form ref="form" v-model="isFormValid" @submit.prevent="submitOrder">
          <v-card>
            <v-card-title>Customer Details</v-card-title>
            <v-card-text>
              <v-text-field
                v-model="formData.customer_name"
                label="Name*"
                :rules="[rules.required]"
                :readonly="isAuthenticated"
              ></v-text-field>

              <v-text-field
                v-model="formData.customer_email"
                label="Email*"
                :rules="[rules.required, rules.email]"
                :readonly="isAuthenticated"
              ></v-text-field>

              <v-text-field
                v-model="formData.customer_phone"
                label="Phone Number*"
                :rules="[rules.required, rules.phone]"
              ></v-text-field>

              <v-textarea
                v-model="formData.delivery_address"
                label="Delivery Address*"
                :rules="[rules.required]"
                rows="3"
                auto-grow
              ></v-textarea>
            </v-card-text>

            <v-card-actions>
              <v-btn
                color="primary"
                block
                size="large"
                type="submit"
                :loading="isSubmitting"
                :disabled="!isFormValid || isSubmitting"
              >
                Proceed to Payment
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'

const store = useStore()
const router = useRouter()

const form = ref(null)
const isFormValid = ref(false)
const isSubmitting = ref(false)

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

const submitOrder = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  isSubmitting.value = true
  
  try {
    const orderResponse = await axios.post('/orders/', {
      customer_name: formData.value.customer_name,
      customer_email: formData.value.customer_email,
      customer_phone: formData.value.customer_phone,
      delivery_address: formData.value.delivery_address,
      items: cartItems.value.map(item => ({
        menu_item: item.id,
        quantity: item.quantity
      })),
      currency: currentCurrency.value,
    })

    store.commit('clearCart')
    window.location.href = orderResponse.data.redirectUri

  } catch (error) {
    console.error('Order error:', error)
  } finally {
    isSubmitting.value = false
  }
}

onMounted(async () => {
  if (isAuthenticated.value) {
    try {
      const response = await axios.get('/user/')
      formData.value = {
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