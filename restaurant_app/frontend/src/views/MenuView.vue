<template>
  <div class="menu-view">
    <v-container>
      <!-- Search and Filter Section -->
      <v-row class="mb-6">
        <v-col cols="12" md="6">
          <v-text-field
            v-model="searchQuery"
            label="Search menu items"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            hide-details
          ></v-text-field>
        </v-col>
        
        <v-col cols="12" md="6" class="d-flex gap-4">
          <v-select
            v-model="selectedCategory"
            :items="categories"
            label="Category"
            variant="outlined"
            hide-details
          ></v-select>

          <v-select
            v-model="priceSort"
            :items="sortOptions"
            label="Sort by price"
            variant="outlined"
            hide-details
          ></v-select>
        </v-col>
      </v-row>

      <!-- Menu Component -->
      <Menu 
        :search-query="searchQuery"
        :selected-category="selectedCategory"
        :price-sort="priceSort"
      />
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Menu from '@/components/Menu.vue'  // Add this import

const searchQuery = ref('')
const selectedCategory = ref('all')
const priceSort = ref('default')
const categories = ['all', 'pizza', 'pasta', 'salads', 'beverages']
const sortOptions = [
  { title: 'Default', value: 'default' },
  { title: 'Price: Low to High', value: 'asc' },
  { title: 'Price: High to Low', value: 'desc' }
]
</script>

<style scoped>
.v-select {
  flex: 1;
}

.menu-view {
  width: 100%;
}
</style>