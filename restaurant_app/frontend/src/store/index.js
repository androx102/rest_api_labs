import { createStore } from 'vuex'
import axios from 'axios'
import Cookies from 'js-cookie'

export default createStore({
  state: {
    cart: {
      items: []
    },
    isLoading: false,
    isAuthenticated: false,
    token: '',
    currency: {
      current: 'PLN',
      rate: null,
      lastUpdate: null,
      symbol: {
        PLN: 'zł',
        USD: '$'
      }
    }
  },
  mutations: {
    setIsAuthenticated(state, value) {
      state.isAuthenticated = value
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = !!token
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    },
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    },
    initializeStore(state) {
      if (localStorage.getItem('cart')) {
        state.cart = JSON.parse(localStorage.getItem('cart'))
      } else {
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }
      const accessToken = Cookies.get('access_token')
      if (accessToken) {
        state.isAuthenticated = true
        axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
      } else {
        state.isAuthenticated = false
        delete axios.defaults.headers.common['Authorization']
      }
    },
    addToCart(state, item) {
      const exists = state.cart.items.find(i => i.id === item.id)
      
      if (exists) {
        exists.quantity++
      } else {
        state.cart.items.push({
          ...item,
          quantity: 1
        })
      }
      
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    updateCartItemQuantity(state, { id, quantity }) {
      const item = state.cart.items.find(i => i.id === id)
      if (item) {
        item.quantity = quantity
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }
    },
    removeFromCart(state, id) {
      state.cart.items = state.cart.items.filter(i => i.id !== id)
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    clearCart(state) {
      state.cart.items = []
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    setCurrency(state, currency) {
      state.currency.current = currency
      localStorage.setItem('currency', currency)
    },
    setExchangeRate(state, rate) {
      state.currency.rate = rate
      state.currency.lastUpdate = new Date().toISOString()
      localStorage.setItem('exchangeRate', JSON.stringify({
        rate: rate,
        lastUpdate: state.currency.lastUpdate
      }))
    },
    setAuth(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated
    },
    
    clearAuth(state) {
      state.isAuthenticated = false
      Cookies.remove('access_token')
      Cookies.remove('refresh_token')
      delete axios.defaults.headers.common['Authorization']
    }
  },
  actions: {
    addToCart({ commit }, item) {
      commit('addToCart', item)
    },
    updateCartItemQuantity({ commit }, payload) {
      commit('updateCartItemQuantity', payload)
    },
    removeFromCart({ commit }, id) {
      commit('removeFromCart', id)
    },
    async fetchExchangeRate({ commit }) {
      try {
        const response = await fetch('https://api.nbp.pl/api/exchangerates/rates/c/usd/today/')
        const data = await response.json()
        commit('setExchangeRate', data.rates[0].ask)
      } catch (error) {
        console.error('Failed to fetch exchange rate:', error)
        commit('setExchangeRate', 4.0) 
      }
    },
    switchCurrency({ commit, state }) {
      const newCurrency = state.currency.current === 'PLN' ? 'USD' : 'PLN'
      commit('setCurrency', newCurrency)
    },
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/login/', credentials)
        const { access, refresh } = response.data
        Cookies.set('access_token', access, { secure: true, sameSite: 'strict' })
        Cookies.set('refresh_token', refresh, { secure: true, sameSite: 'strict' })
  
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
        
        commit('setAuth', true)
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },

    logout({ commit }) {
      commit('clearAuth')
    }
  },
  getters: {
    cartTotal: state => {
      const total = state.cart.items.reduce((total, item) => {
        return total + (item.price * item.quantity)
      }, 0)
      return total
    },
    cartItemCount: state => {
      return state.cart.items.reduce((count, item) => {
        return count + item.quantity
      }, 0)
    },
    currentCurrency: state => state.currency.current,
    currencySymbol: state => state.currency.symbol[state.currency.current],
    convertPrice: state => price => {
      if (state.currency.current === 'PLN') {
        return price
      }
      if (state.currency.current === 'USD' && state.currency.rate) {
        return (parseFloat(price) / state.currency.rate).toFixed(2)
      }
      return price
    },
    formatPrice: (state, getters) => price => {
      const convertedPrice = getters.convertPrice(price)
      const symbol = state.currency.symbol[state.currency.current]
      if (state.currency.current === 'PLN') {
        return `${convertedPrice} ${symbol}`
      } else {
        return `${symbol}${convertedPrice}`
      }
    },
    isAuthenticated: state => state.isAuthenticated
  }
})
