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
        <div class="navbar-start">

        </div>

        <div class="navbar-end">
          <router-link to="/" class="navbar-item">Home</router-link>
          <router-link to="/menu" class="navbar-item">Menu</router-link>
          <router-link to="/order" class="navbar-item">Track order</router-link>

          <div class="navbar-item">
            <div class="buttons">
              <router-link to="/cart" class="button is-success">
                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                <span>Cart ({{ cartCount }})</span>
              </router-link>
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

<script>
import axios from 'axios'
import { useStore } from 'vuex'
import { computed } from 'vue'

export default {
  setup() {
    const store = useStore()
    
    return {
      cartCount: computed(() => store.getters.cartItemCount)
    }
  },
  data() {
    return {
      showMobileMenu: false
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  }
}
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
</style>