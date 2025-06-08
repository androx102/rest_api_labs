<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        
        <div class="navbar-item"><strong>Pizzeria Giuseppe</strong></div>

        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu }">
        <div class="navbar-end">
          <router-link to="/" class="navbar-item">Home</router-link>
          <router-link to="/menu" class="navbar-item">Menu</router-link>
          
          
          <template v-if="isAuthenticated">
            <router-link to="/my-orders" class="navbar-item">My Orders</router-link>
          </template>
          <template v-else>
            <router-link to="/track-order" class="navbar-item">Track Order</router-link>
          </template>

          
          <div class="navbar-item">
            <button 
              class="button is-small is-light"
              @click="toggleCurrency"
            >
              {{ currentCurrency }} ({{ currencySymbol }})
            </button>
          </div>

        <div class="navbar-item">
            <div class="buttons">
              <router-link to="/cart" class="button is-success">
                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                <span>Cart ({{ cartCount }})</span>
              </router-link>

              
              <template v-if="$store.state.isAuthenticated">
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn
                      class="button is-light"
                      v-bind="props"
                    >
                      My Account
                      <v-icon right>mdi-chevron-down</v-icon>
                    </v-btn>
                  </template>

                  <v-list>
                    <v-list-item
                      to="/my-account"
                      link
                    >
                      <v-list-item-title>
                        <v-icon left>mdi-account</v-icon>
                        My Data
                      </v-list-item-title>
                    </v-list-item>

                    <v-list-item
                      @click="handleLogout"
                    >
                      <v-list-item-title>
                        <v-icon left>mdi-logout</v-icon>
                        Logout
                      </v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>

              <template v-else>
                <router-link to="/login" class="button is-light">Log in</router-link>
              </template>


            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <router-view/>
    </section>

    <footer class="footer bg-grey-darken-3">
      <div class="content">
        <div class="columns">
          <div class="column">
            <h3 class="has-text-white mb-4">Connect With Us</h3>
            <div class="social-links">
              <a href="https://facebook.com" target="_blank" class="mr-4">
                <v-icon color="white">mdi-facebook</v-icon>
              </a>
              <a href="https://instagram.com" target="_blank" class="mr-4">
                <v-icon color="white">mdi-instagram</v-icon>
              </a>
              <a href="https://twitter.com" target="_blank">
                <v-icon color="white">mdi-twitter</v-icon>
              </a>
            </div>
          </div>
          
          <div class="column">
            <h3 class="has-text-white mb-4">Opening Hours</h3>
            <p class="has-text-white">Monday - Friday: 11:00 - 22:00</p>
            <p class="has-text-white">Saturday - Sunday: 12:00 - 23:00</p>
          </div>
          
          <div class="column">
            <h3 class="has-text-white mb-4">Contact</h3>
            <p class="has-text-white">Phone: +48 123 456 789</p>
            <p class="has-text-white">Email: contact@giuseppe.com</p>
          </div>
        </div>
        
        <div class="divider my-4"></div>
        
        <p class="has-text-centered has-text-white">Copyright Mikolaj Paluchowski(c) 2025</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const showMobileMenu = ref(false)
const currentCurrency = computed(() => store.getters.currentCurrency)
const currencySymbol = computed(() => store.getters.currencySymbol)
const cartCount = computed(() => store.getters.cartItemCount)
const isAuthenticated = computed(() => store.getters.isAuthenticated)

const toggleCurrency = () => {
  store.dispatch('switchCurrency')
}

const handleLogout = () => {
  store.dispatch('logout')
  router.push('/login')
}

onMounted(async () => {
  store.commit('initializeStore')

  const savedRate = localStorage.getItem('exchangeRate')
  if (savedRate) {
    const { rate, lastUpdate } = JSON.parse(savedRate)
    const lastUpdateDate = new Date(lastUpdate)
    const now = new Date()
    
    if (now - lastUpdateDate > 3600000) {
      await store.dispatch('fetchExchangeRate')
    } else {
      store.commit('setExchangeRate', rate)
    }
  } else {
    await store.dispatch('fetchExchangeRate')
  }

  
  const savedCurrency = localStorage.getItem('currency')
  if (savedCurrency) {
    store.commit('setCurrency', savedCurrency)
  }
})
</script>

<style lang="scss">
@import '../node_modules/bulma';

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;

  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

.footer {
  padding: 3rem 1.5rem;
  background-color: #363636;
  
  .social-links {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    
    a {
      transition: opacity 0.3s ease;
      
      &:hover {
        opacity: 0.7;
      }
    }
  }
  
  .divider {
    height: 1px;
    background-color: rgba(255, 255, 255, 0.1);
    margin: 2rem 0;
  }
  
  h3 {
    font-size: 1.2rem;
    font-weight: bold;
  }
}

.button.is-small {
  margin: 0 0.5rem;
  min-width: 60px;
}
</style>

<style scoped>
.v-menu {
  display: inline-block;
}

.v-list-item {
  min-width: 150px;
}

.v-icon {
  margin-right: 8px;
}
</style>