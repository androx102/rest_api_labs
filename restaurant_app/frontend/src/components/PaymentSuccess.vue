<template>
  <v-row>
    <v-col cols="12" md="6" class="mx-auto text-center">
      <v-card class="pa-6">
        <v-icon
          size="64"
          color="success"
          class="mb-4"
        >
          mdi-check-circle
        </v-icon>
        
        <h1 class="text-h4 mb-4">Payment Successful!</h1>
        <p class="text-body-1 mb-6">
          Thank you for your order. Your payment has been processed successfully.
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
            View Order Details
          </v-btn>
          
          <v-btn
            color="secondary"
            block
            to="/menu"
            variant="outlined"
          >
            Continue Shopping
          </v-btn>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
defineProps({
  orderId: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true
  }
})
</script>