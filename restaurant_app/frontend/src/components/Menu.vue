<template>
  <div class="menu-list">
    <v-container>
      <!-- Add loading and error states -->
      <v-row v-if="loading">
        <v-col cols="12" class="text-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-col>
      </v-row>
      
      <v-row v-else-if="error">
        <v-col cols="12">
          <v-alert type="error">{{ error }}</v-alert>
        </v-col>
      </v-row>

      <v-row v-else>
        <v-col 
          v-for="item in filteredItems" 
          :key="item.id" 
          cols="12" 
          md="6" 
          lg="4"
        >
          <v-card class="mx-auto menu-item" max-width="400">
            <v-card-title class="text-h5">{{ item.name }}</v-card-title>
            <v-card-text>
              <p class="text-body-1">{{ item.description }}</p>
              <p class="text-h6 mt-2">Price: ${{ item.price }}</p>
              <v-chip color="primary" class="mt-2">{{ item.category }}</v-chip>
            </v-card-text>
            <v-card-actions>
              <v-btn
                color="primary"
                variant="elevated"
                block
                :disabled="!item.is_available"
                @click="addToCart(item)"
              >
                {{ item.is_available ? 'Add to Cart' : 'Not Available' }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useStore } from 'vuex'  // Add this import
import axios from 'axios'

const store = useStore()  // Initialize store

const props = defineProps({
  searchQuery: {
    type: String,
    default: ''
  },
  selectedCategory: {
    type: String,
    default: 'all'
  },
  priceSort: {
    type: String,
    default: 'default'
  }
})

const menuItems = ref([])
const loading = ref(true)
const error = ref(null)

// Add API base URL
const API_URL = 'http://127.0.0.1:8000/api'

// Fetch menu items from backend
const fetchMenuItems = async () => {
  try {
    console.log('Try to reach backend')
    loading.value = true
    const response = await axios.get(`${API_URL}/menu/`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      withCredentials: false  // Changed from true to false
    })
    console.log('API Response:', response.data)
    menuItems.value = Array.isArray(response.data) ? response.data : response.data.results
  } catch (e) {
    error.value = `Error loading menu items: ${e.message}`
    console.error('API Error:', e.response?.data || e.message)
  } finally {
    loading.value = false
  }
}

// Filter and sort menu items based on backend model fields
const filteredItems = computed(() => {
  let items = [...menuItems.value]

  // Apply category filter matching backend CATEGORY_CHOICES
  if (props.selectedCategory !== 'all') {
    items = items.filter(item => item.category === props.selectedCategory) // Removed toLowerCase()
  }

  // Apply search filter
  if (props.searchQuery) {
    const query = props.searchQuery.toLowerCase()
    items = items.filter(item => 
      item.name.toLowerCase().includes(query) || 
      item.description.toLowerCase().includes(query)
    )
  }

  // Apply price sorting using decimal values
  if (props.priceSort !== 'default') {
    items.sort((a, b) => {
      const priceA = parseFloat(a.price)
      const priceB = parseFloat(b.price)
      return props.priceSort === 'asc' ? priceA - priceB : priceB - priceA
    })
  }

  return items
})

// Update addToCart function to use Vuex
const addToCart = (item) => {
  store.dispatch('addToCart', item)
}

// Watch for prop changes
watch([() => props.searchQuery, () => props.selectedCategory, () => props.priceSort], 
  () => {
    // Could add debounce for search if needed
    console.log('Filters changed')
  }
)

// Add immediate console log to verify mounting
onMounted(() => {
  console.log('Menu component mounted')
  fetchMenuItems()
})
</script>

<style scoped>
.menu-list {
  width: 100%;
}

.menu-item {
  transition: transform 0.3s ease;
}

.menu-item:hover {
  transform: translateY(-5px);
}
</style>