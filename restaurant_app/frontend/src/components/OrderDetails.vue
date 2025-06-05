<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between align-center">
      <span>Order #{{ order.order_number_uuid }}</span>
      <v-chip :color="getStatusColor">{{ order.status }}</v-chip>
    </v-card-title>

    <v-card-text>
      <v-row>
        <!-- Customer Details -->
        <v-col cols="12" md="6">
          <h3 class="text-h6 mb-4">Customer Details</h3>
          <v-list density="compact">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-account</v-icon>
              </template>
              <v-list-item-title>{{ order.customer_name }}</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-email</v-icon>
              </template>
              <v-list-item-title>{{ order.customer_email }}</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-phone</v-icon>
              </template>
              <v-list-item-title>{{ order.customer_phone }}</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-map-marker</v-icon>
              </template>
              <v-list-item-title>{{ order.delivery_address }}</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-clock</v-icon>
              </template>
              <v-list-item-title>{{ formatDate(order.created_at) }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-col>

        <!-- Order Items -->
        <v-col cols="12" md="6">
          <h3 class="text-h6 mb-4">Order Items</h3>
          <v-list>
            <v-list-item v-for="item in order.items" :key="item.menu_item">
              <v-list-item-title>
                {{ item.menu_item_name }} x {{ item.quantity }}
              </v-list-item-title>
              <v-list-item-subtitle>
                Price: {{ formatPrice(item.menu_item_price) }}
                <br>
                Subtotal: {{ formatPrice(item.subtotal) }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <v-divider class="my-4"></v-divider>
          
          <div class="d-flex justify-end">
            <p class="text-h6">Total: {{ formatPrice(order.total_amount) }}</p>
          </div>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions>
      <v-btn
        color="primary"
        variant="text"
        @click="$emit('back')"
      >
        Back to Search
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

// Add currency-related computed properties
const currentCurrency = computed(() => store.getters.currentCurrency)
const currencySymbol = computed(() => store.getters.currencySymbol)

// Add price formatting function
const formatPrice = (price) => {
  return store.getters.formatPrice(price)
}

const getStatusColor = computed(() => {
  switch (props.order.status) {
    case 'pending':
      return 'warning'
    case 'confirmed':
      return 'info'
    case 'preparing':
      return 'primary'
    case 'out_for_delivery':
      return 'purple'
    case 'delivered':
      return 'success'
    case 'cancelled':
      return 'error'
    default:
      return 'grey'
  }
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

defineEmits(['back'])
</script>