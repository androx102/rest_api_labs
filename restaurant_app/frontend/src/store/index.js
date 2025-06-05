import { createStore } from 'vuex'

export default createStore({
  state: {
    cart: {
      items: []
    },
    isLoading: false,
    token: ''
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
    }
  },
  getters: {
    cartTotal: state => {
      return state.cart.items.reduce((total, item) => {
        return total + (item.price * item.quantity)
      }, 0)
    },
    cartItemCount: state => {
      return state.cart.items.reduce((count, item) => {
        return count + item.quantity
      }, 0)
    }
  }
})
