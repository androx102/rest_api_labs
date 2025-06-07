<template>
  <div class="track-order">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h3 mb-6">Track Order</h1>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="6" class="mx-auto">
          <v-card>
            <v-card-title>Find Your Order</v-card-title>
            <v-card-text>
              <v-form ref="form" v-model="isFormValid" @submit.prevent="trackOrder">
                <v-text-field
                  v-model="orderNumber"
                  label="Order Number"
                  :rules="[rules.required]"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="email"
                  label="Email"
                  type="email"
                  :rules="[rules.required, rules.email]"
                  required
                ></v-text-field>

                <v-btn
                  color="primary"
                  block
                  type="submit"
                  :loading="isLoading"
                  :disabled="!isFormValid || isLoading"
                >
                  Track Order
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'

const router = useRouter()
const form = ref(null)
const isFormValid = ref(false)
const isLoading = ref(false)
const showError = ref(false)
const errorMessage = ref('')

const orderNumber = ref('')
const email = ref('')

const rules = {
  required: v => !!v || 'This field is required',
  email: v => /.+@.+\..+/.test(v) || 'Email must be valid'
}

const trackOrder = async () => {
  if (!form.value.validate()) return
  
  isLoading.value = true
  try {
    const response = await axios.get(`/orders/${orderNumber.value}?email=${encodeURIComponent(email.value)}`)
    router.push({
      name: 'order-details',
      params: { id: orderNumber.value },
      query: { email: email.value }
    })
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Failed to find order'
    showError.value = true
  } finally {
    isLoading.value = false
  }
}
</script>