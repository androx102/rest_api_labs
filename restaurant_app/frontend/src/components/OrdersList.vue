<template>
  <div>
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

    <!-- Orders List -->
    <v-expansion-panels v-if="orders.length > 0">
      <v-expansion-panel
        v-for="order in orders"
        :key="order.order_number_uuid"
      >
        <v-expansion-panel-title>
          <v-row no-gutters>
            <v-col cols="4">
              Order #{{ order.order_number_uuid.slice(0,8) }}
            </v-col>
            <v-col cols="4" class="text-caption">
              {{ new Date(order.created_at).toLocaleString() }}
            </v-col>
            <v-col cols="4">
              <v-chip
                :color="getStatusColor(order.status)"
                size="small"
              >
                {{ order.status }}
              </v-chip>
            </v-col>
          </v-row>
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <!-- Order Details -->
          <v-list>
            <v-list-item v-for="item in order.items" :key="item.id">
              <v-list-item-title>
                {{ item.menu_item_name }} x {{ item.quantity }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ formatPrice(item.menu_item_price * item.quantity) }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <v-divider class="my-3"></v-divider>

          <!-- Order Total -->
          <div class="d-flex justify-end">
            <p class="text-h6">
              Total: {{ formatPrice(order.total_amount) }}
            </p>
          </div>

          <!-- Delivery Info -->
          <v-card class="mt-4" variant="outlined">
            <v-card-text>
              <p><strong>Delivery Address:</strong> {{ order.delivery_address }}</p>
              <p><strong>Phone:</strong> {{ order.customer_phone }}</p>
            </v-card-text>
          </v-card>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <!-- No Orders Message -->
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import axios from '@/utils/axios'

const store = useStore()
const orders = ref([])
const isLoading = ref(true)
const error = ref('')

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
  isLoading.value = true
  try {
    const response = await axios.get('/orders/')
    orders.value = response.data
  } catch (err) {
    error.value = 'Failed to load orders'
    console.error('Error fetching orders:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchOrders()
})
</script>