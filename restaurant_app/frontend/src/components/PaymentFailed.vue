<template>
  <v-row>
    <v-col cols="12" md="6" class="mx-auto text-center">
      <v-card class="pa-6">
        <v-icon
          size="64"
          color="error"
          class="mb-4"
        >
          mdi-alert-circle
        </v-icon>
        
        <h1 class="text-h4 mb-4">Payment Failed</h1>
        <p class="text-body-1 mb-6">
          We're sorry, but your payment could not be processed. 
          Please try again or contact our support team if the problem persists.
        </p>

        <div class="d-flex flex-column gap-4">
          <v-btn
            color="primary"
            block
            :to="{ 
              name: 'checkout'
            }"
          >
            Try Again
          </v-btn>
          
          <v-btn
            color="secondary"
            block
            to="/menu"
            variant="outlined"
          >
            Return to Menu
          </v-btn>

          <v-btn
            color="info"
            block
            variant="text"
            href="mailto:support@yourrestaurant.com"
          >
            Contact Support
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