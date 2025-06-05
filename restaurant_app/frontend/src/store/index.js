import { createStore } from 'vuex'

export default createStore({
  state: {
    cart: {
      items: []
    },
    isLoading: false,
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
    initializeStore(state) {
      if (localStorage.getItem('cart')) {
        state.cart = JSON.parse(localStorage.getItem('cart'))
      } else {
        localStorage.setItem('cart', JSON.stringify(state.cart))
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
        commit('setExchangeRate', 4.0) // Fallback rate
      }
    },
    switchCurrency({ commit, state }) {
      const newCurrency = state.currency.current === 'PLN' ? 'USD' : 'PLN'
      commit('setCurrency', newCurrency)
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
      // If currency is PLN, return original price
      if (state.currency.current === 'PLN') {
        return price
      }
      // Only convert to USD if we have an exchange rate
      if (state.currency.current === 'USD' && state.currency.rate) {
        return (parseFloat(price) / state.currency.rate).toFixed(2)
      }
      return price
    },
    formatPrice: (state, getters) => price => {
      const convertedPrice = getters.convertPrice(price)
      const symbol = state.currency.symbol[state.currency.current]
      
      // Format based on currency
      if (state.currency.current === 'PLN') {
        return `${convertedPrice} ${symbol}`
      } else {
        return `${symbol}${convertedPrice}`
      }
    }
  }
})
