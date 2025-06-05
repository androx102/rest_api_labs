<template>
  <v-card class="pa-4">
    <v-form @submit.prevent="handleSubmit" ref="form">
      <v-card-title class="text-h5 mb-4">Login</v-card-title>
      
      <v-text-field
        v-model="formData.email"
        label="Email"
        :rules="[rules.required]"
        required
      ></v-text-field>

      <v-text-field
        v-model="formData.password"
        label="Password"
        type="password"
        :rules="[rules.required]"
        required
      ></v-text-field>

      <v-alert
        v-if="error"
        type="error"
        class="mb-4"
      >
        {{ error }}
      </v-alert>

      <v-card-actions class="d-flex flex-column">
        <v-btn
          color="primary"
          type="submit"
          block
          :loading="isLoading"
          :disabled="isLoading"
        >
          Login
        </v-btn>
        
        <v-btn
          variant="text"
          class="mt-2"
          @click="$router.push('/register')"
        >
          Don't have an account? Register
        </v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()
const form = ref(null)
const error = ref('')
const isLoading = ref(false)

const formData = ref({
  email: '',
  password: ''
})

const rules = {
  required: v => !!v || 'This field is required'
}

const handleSubmit = async () => {
  if (!form.value.validate()) return
  
  isLoading.value = true
  error.value = ''

  try {
    const success = await store.dispatch('login', {
      email: formData.value.email,
      password: formData.value.password
    })

    if (success) {
      router.push('/')
    } else {
      error.value = 'Login failed'
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed'
  } finally {
    isLoading.value = false
  }
}
</script>