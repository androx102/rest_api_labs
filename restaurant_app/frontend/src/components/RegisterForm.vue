<template>
  <v-card class="pa-4">
    <v-form @submit.prevent="handleSubmit" ref="form">
      <v-card-title class="text-h5 mb-4">Register</v-card-title>
      
      <v-text-field
        v-model="formData.name"
        label="Name"
        :rules="[rules.required, rules.username]"
        required
      ></v-text-field>

      <v-text-field
        v-model="formData.email"
        label="Email"
        type="email"
        :rules="[rules.required, rules.email]"
        required
      ></v-text-field>

      <v-text-field
        v-model="formData.password"
        label="Password"
        type="password"
        :rules="[rules.required, rules.password]"
        required
      ></v-text-field>

      <v-text-field
        v-model="formData.password2"
        label="Confirm Password"
        type="password"
        :rules="[rules.required, rules.passwordMatch]"
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
          Register
        </v-btn>
        
        <v-btn
          variant="text"
          class="mt-2"
          @click="$router.push('/login')"
        >
          Already have an account? Login
        </v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'

const store = useStore()
const router = useRouter()
const form = ref(null)
const error = ref('')
const isLoading = ref(false)

const formData = ref({
  name: '',
  email: '',
  password: '',
  password2: ''
})

const rules = {
  required: v => !!v || 'This field is required',
  username: v => /^[a-zA-Z0-9_]{3,20}$/.test(v) || 'Username must be 3-20 characters and contain only letters, numbers, and underscores',
  email: v => /.+@.+\..+/.test(v) || 'Email must be valid',
  password: v => v.length >= 8 || 'Password must be at least 8 characters',
  passwordMatch: v => v === formData.value.password || 'Passwords must match'
}

const handleSubmit = async () => {
  if (!form.value.validate()) return
  
  isLoading.value = true
  error.value = ''

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/register/', {
      name: formData.value.name,
      email: formData.value.email,
      password: formData.value.password,
    })
    


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
    error.value = Object.values(err.response?.data || {})[0]?.[0] || 'Registration failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>