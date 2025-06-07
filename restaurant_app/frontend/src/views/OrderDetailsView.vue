<template>
  <div class="order-details">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h3 mb-6">Order Details</h1>
        </v-col>
      </v-row>

      <!-- Loading State -->
      <v-overlay
        :model-value="isLoading"
        class="align-center justify-center"
      >
        <v-progress-circular
          color="primary"
          indeterminate
          size="64"
        ></v-progress-circular>
      </v-overlay>

      <!-- Error State -->
      <v-row v-if="error">
        <v-col cols="12" md="6" class="mx-auto">
          <v-alert
            type="error"
            class="mb-4"
          >
            {{ error }}
          </v-alert>
          <v-btn
            color="primary"
            block
            to="/track-order"
          >
            Back to Order Tracking
          </v-btn>
        </v-col>
      </v-row>

      <!-- Order Details -->
      <template v-if="orderDetails && !error">
        <v-row>
          <v-col cols="12" md="8" class="mx-auto">
            <v-card>
              <v-card-title class="d-flex align-center">
                <span>Order #{{ orderDetails.order_number_uuid.slice(0,8) }}</span>
                <v-spacer></v-spacer>
                <v-chip
                  :color="getStatusColor(orderDetails.status)"
                  size="small"
                >
                  {{ orderDetails.status }}
                </v-chip>
              </v-card-title>

              <v-card-text>
                <!-- Order Info -->
                <div class="mb-4">
                  <p><strong>Date:</strong> {{ new Date(orderDetails.created_at).toLocaleString() }}</p>
                  <p><strong>Email:</strong> {{ orderDetails.customer_email }}</p>
                  <p><strong>Phone:</strong> {{ orderDetails.customer_phone }}</p>
                  <p><strong>Delivery Address:</strong> {{ orderDetails.delivery_address }}</p>
                </div>

                <!-- Order Items -->
                <v-list>
                  <v-list-subheader>Order Items</v-list-subheader>
                  <v-list-item
                    v-for="item in orderDetails.items"
                    :key="item.id"
                    :value="item"
                  >
                    <v-list-item-title>
                      {{ item.menu_item_name }} x {{ item.quantity }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      {{ formatPrice(item.menu_item_price * item.quantity) }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>

                <!-- Total -->
                <v-divider class="my-4"></v-divider>
                <div class="text-right">
                  <p class="text-h6">
                    Total: {{ formatPrice(orderDetails.total_amount) }}
                  </p>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from '@/utils/axios'

const route = useRoute()
const router = useRouter()
const store = useStore()

const isLoading = ref(true)
const error = ref('')
const orderDetails = ref(null)

const formatPrice = (price) => {
  return store.getters.formatPrice(price)
}

const getStatusColor = (status) => {
  const colors = {
    'pending': 'warning',
    'confirmed': 'info',
    'preparing': 'info',
    'out_for_delivery': 'primary',
    'delivered': 'success',
    'canceled': 'error'
  }
  return colors[status] || 'grey'
}

const fetchOrderDetails = async () => {
  const orderId = route.params.id
  const email = route.query.email

  if (!orderId) {
    error.value = 'Order ID is required'
    isLoading.value = false
    return
  }

  try {
    const response = await axios.get(
      `/orders/${orderId}${email ? `?email=${encodeURIComponent(email)}` : ''}`
    )
    orderDetails.value = response.data
  } catch (err) {
    console.error('Failed to fetch order details:', err)
    error.value = err.response?.data?.error || 'Failed to load order details'
    if (err.response?.status === 404) {
      setTimeout(() => {
        router.push('/track-order')
      }, 3000)
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchOrderDetails()
})
</script>