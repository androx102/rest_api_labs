<template>
  <div class="payment-redirect">
    <v-container>
      <!-- Loading State -->
      <div v-if="isLoading" class="d-flex justify-center align-center" style="min-height: 400px">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="d-flex justify-center align-center">
        <v-alert
          type="error"
          class="ma-4"
        >
          {{ error }}
        </v-alert>
      </div>

      <!-- Payment Status Components -->
      <PaymentSuccess
        v-else-if="paymentStatus === 'confirmed'"
        :order-id="orderId"
        :email="email"
      />
      
      <PaymentPending
        v-else-if="paymentStatus === 'pending'"
        :order-id="orderId"
        :email="email"
        @refresh="checkPaymentStatus"
      />
      
      <PaymentFailed
        v-else
        :order-id="orderId"
        :email="email"
      />
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/utils/axios'
import PaymentSuccess from '@/components/PaymentSuccess.vue'
import PaymentPending from '@/components/PaymentPending.vue'
import PaymentFailed from '@/components/PaymentFailed.vue'

const route = useRoute()
const router = useRouter()

const isLoading = ref(true)
const error = ref('')
const paymentStatus = ref('')
const orderId = ref('')
const email = ref('')

const checkPaymentStatus = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    orderId.value = route.params.id
    email.value = route.query.email

    if (!orderId.value || !email.value) {
      throw new Error('Missing required parameters')
    }

    const response = await axios.get(
      `/orders/${orderId.value}?check_payment=true&email=${email.value}`
    )
    paymentStatus.value = response.data.status
  } catch (err) {
    console.error('Payment status check failed:', err)
    error.value = 'Failed to verify payment status'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  checkPaymentStatus()
})
</script>