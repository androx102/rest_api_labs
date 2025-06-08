<template>
  <div class="my-orders">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h3 mb-6">My Orders</h1>
        </v-col>
      </v-row>

      
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

      
      <v-list v-if="orders.length > 0">
        <v-list-item
          v-for="order in orders"
          :key="order.order_number_uuid"
          :value="order"
        >
          <template v-slot:prepend>
            <v-chip
              :color="getStatusColor(order.status)"
              size="small"
              class="mr-4"
            >
              {{ order.status }}
            </v-chip>
          </template>

          <v-list-item-title>
            Order #{{ order.order_number_uuid.slice(0,8) }}
          </v-list-item-title>

          <v-list-item-subtitle>
            {{ new Date(order.created_at).toLocaleString() }} - 
            Total: {{ formatPrice(order.total_amount) }}
          </v-list-item-subtitle>

          <template v-slot:append>
            <v-btn
              color="primary"
              variant="text"
              :to="{ name: 'order-details', params: { id: order.order_number_uuid }}"
            >
              View Details
            </v-btn>
          </template>
        </v-list-item>
      </v-list>

      
      <v-card v-else-if="!isLoading" class="text-center pa-4">
        <v-icon size="64" color="grey">mdi-receipt</v-icon>
        <p class="text-h6 mt-4">No orders found</p>
        <v-btn
          color="primary"
          class="mt-4"
          to="/menu"
        >
          Browse Menu
        </v-btn>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import axios from '@/utils/axios'

const store = useStore()
const orders = ref([])
const isLoading = ref(true)

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

const fetchOrders = async () => {
  try {
    const response = await axios.get('/orders/')
    orders.value = response.data
  } catch (err) {
    console.error('Failed to fetch orders:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchOrders()
})
</script>