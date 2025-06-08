<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="8" md="6" class="mx-auto">
        <v-card>
          <v-card-title class="text-h5 mb-4">
            My Account
          </v-card-title>

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

          <v-card-text>
            <v-form ref="form" @submit.prevent="handleSubmit" v-if="!isLoading">
              
              <v-text-field
                v-model="userData.email"
                label="Email"
                disabled
                readonly
              ></v-text-field>

              
              <v-text-field
                v-model="userData.name"
                label="Name"
                clearable
              ></v-text-field>

              
              <v-text-field
                v-model="userData.phone_number"
                label="Phone Number (optional)"
                :rules="[rules.phone]"
                placeholder="Enter your phone number"
                clearable
              ></v-text-field>

              
              <v-textarea
                v-model="userData.delivery_address"
                label="Delivery Address (optional)"
                placeholder="Enter your delivery address"
                clearable
                auto-grow
                rows="3"
              ></v-textarea>

              
              <v-alert
                v-if="error"
                type="error"
                class="mb-4"
              >
                {{ error }}
              </v-alert>

              <v-alert
                v-if="success"
                type="success"
                class="mb-4"
              >
                Data updated successfully!
              </v-alert>

              
              <v-card-actions class="d-flex flex-column">
                <v-btn
                  color="primary"
                  type="submit"
                  block
                  :loading="isLoading"
                  :disabled="isLoading"
                >
                  Save Changes
                </v-btn>

                <v-btn
                  color="error"
                  variant="outlined"
                  block
                  class="mt-4"
                  @click="confirmDeleteAccount"
                  :loading="isDeleting"
                  :disabled="isDeleting"
                >
                  Delete Account
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h5">
          Delete Account
        </v-card-title>
        <v-card-text>
          Are you sure you want to delete your account? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="showDeleteDialog = false">
            Cancel
          </v-btn>
          <v-btn color="error" @click="deleteAccount">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'

const store = useStore()
const router = useRouter()
const form = ref(null)


const userData = ref({
  email: '',
  name: '',
  phone_number: '',
  delivery_address: ''
})

const isLoading = ref(true)
const isDeleting = ref(false)
const error = ref('')
const success = ref(false)
const showDeleteDialog = ref(false)

const rules = {
  phone: v => !v || /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/.test(v) || 'Please enter a valid phone number'
}

const fetchUserData = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await axios.get('/user/')
    userData.value = {
      email: response.data.email || '',
      name: response.data.name || '',
      phone_number: response.data.phone_number || '',
      delivery_address: response.data.delivery_address || ''
    }
  } catch (err) {
    if (err.response?.status === 401) {
      store.dispatch('logout')
      router.push('/login')
    } else {
      error.value = 'Failed to load user data. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!form.value.validate()) return

  isLoading.value = true
  error.value = ''
  success.value = false

  try {
    await axios.put('/user/', {
      name: userData.value.name,
      phone_number: userData.value.phone_number,
      delivery_address: userData.value.delivery_address
    })
    success.value = true
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to update data'
  } finally {
    isLoading.value = false
  }
}

const confirmDeleteAccount = () => {
  showDeleteDialog.value = true
}

const deleteAccount = async () => {
  isDeleting.value = true
  try {
    await axios.delete('/user/')
    store.dispatch('logout')
    router.push('/')
  } catch (err) {
    error.value = 'Failed to delete account'
  } finally {
    isDeleting.value = false
    showDeleteDialog.value = false
  }
}

onMounted(() => {
  fetchUserData()
})
</script>