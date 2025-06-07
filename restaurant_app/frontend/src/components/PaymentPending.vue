<template>
  <v-row>
    <v-col cols="12" md="6" class="mx-auto text-center">
      <v-card class="pa-6">
        <v-icon
          size="64"
          color="warning"
          class="mb-4"
        >
          mdi-clock-outline
        </v-icon>
        
        <h1 class="text-h4 mb-4">Payment Processing</h1>
        <p class="text-body-1 mb-6">
          Your payment is being processed. This may take a few moments.
          We'll notify you once the payment is confirmed.
        </p>

        <div class="d-flex flex-column gap-4">
          <v-btn
            color="primary"
            block
            :to="{ 
              name: 'order-details',
              params: { id: orderId },
              query: { email }
            }"
          >
            Track order
          </v-btn>
          
          <v-btn
            color="secondary"
            block
            @click="refreshStatus"
            :loading="isRefreshing"
          >
            Refresh payment status
          </v-btn>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  orderId: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['refresh'])
const isRefreshing = ref(false)

const refreshStatus = async () => {
  isRefreshing.value = true
  await emit('refresh')
  isRefreshing.value = false
}
</script>