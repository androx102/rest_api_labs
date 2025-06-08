<template>
  <v-container fluid class="pa-0">
    <v-row>
      <v-col cols="12">
        <v-sheet
          class="bg-grey-darken-3 px-6 py-12 text-center hero-section"
          height="300"
        >
          <h1 class="text-h2 font-weight-bold mb-6 primary--text">Welcome to Pizzeria Giuseppe</h1>
          <p class="text-h4 font-weight-light">The best pizza in town, delivered to your door!</p>
        </v-sheet>
      </v-col>
    </v-row>

    
    <v-row class="promotions-section">
      <v-col cols="12">
        <v-sheet class="bg-grey-darken-3 px-6 py-8 text-center" height="300">
          <h2 class="text-h3 font-weight-bold mb-8 text-white">Current Promotions</h2>
          <v-row justify="center" class="px-4">
            <v-col cols="12" md="4">
              <v-card class="mx-auto promotion-card" max-width="400" elevation="0">
                <v-card-title class="text-h5 font-weight-bold text-white">Family Monday</v-card-title>
                <v-card-text class="text-center">
                  <p class="text-h6 mb-6 text-white">20% OFF on all family-size pizzas</p>
                  <v-icon size="x-large" color="primary">mdi-pizza</v-icon>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" md="4">
              <v-card class="mx-auto promotion-card" max-width="400" elevation="0">
                <v-card-title class="text-h5 font-weight-bold text-white">Happy Hours</v-card-title>
                <v-card-text class="text-center">
                  <p class="text-h6 mb-6 text-white">15% OFF between 14:00-17:00</p>
                  <v-icon size="x-large" color="primary">mdi-clock-outline</v-icon>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" md="4">
              <v-card class="mx-auto promotion-card" max-width="400" elevation="0">
                <v-card-title class="text-h5 font-weight-bold text-white">Student Deal</v-card-title>
                <v-card-text class="text-center">
                  <p class="text-h6 mb-6 text-white">10% OFF with student ID</p>
                  <v-icon size="x-large" color="primary">mdi-school</v-icon>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-sheet>
      </v-col>
    </v-row>

    
    <v-row class="contact-section">
      <v-col cols="12" md="6">
        <v-sheet
          class="bg-grey-darken-3 px-8 py-12 d-flex flex-column justify-center contact-sheet"
          height="600"
        >
          <div class="text-center">
            <h2 class="text-h3 font-weight-bold mb-8 primary--text">Contact Us</h2>
            <v-list bg-color="transparent" class="mx-auto contact-list" max-width="500">
              <v-list-item class="mb-4">
                <template v-slot:prepend>
                  <v-icon size="large" color="primary">mdi-phone</v-icon>
                </template>
                <v-list-item-title class="text-h6">+48 123 456 789</v-list-item-title>
              </v-list-item>
              
              <v-list-item class="mb-4">
                <template v-slot:prepend>
                  <v-icon size="large" color="primary">mdi-email</v-icon>
                </template>
                <v-list-item-title class="text-h6">contact@giuseppe.com</v-list-item-title>
              </v-list-item>

              <v-divider class="my-6"></v-divider>
              
              <v-list-item class="mb-4">
                <template v-slot:prepend>
                  <v-icon size="large" color="primary">mdi-map-marker</v-icon>
                </template>
                <v-list-item-title class="text-h6">123 Pizza Street, Warsaw</v-list-item-title>
              </v-list-item>

              <v-list-item>
                <template v-slot:prepend>
                  <v-icon size="large" color="primary">mdi-clock</v-icon>
                </template>
                <v-list-item-title class="text-h6">
                  Mon-Fri: 11:00 - 22:00
                  <br>
                  Sat-Sun: 12:00 - 23:00
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </div>
        </v-sheet>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-sheet height="600" class="map-sheet">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2443.7977603881913!2d21.0119!3d52.2297!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zM3XEhMKwMTUnMDAuMCJOIDIxwrAwMCcwMC4wIkU!5e0!3m2!1sen!2spl!4v1234567890!5m2!1sen!2spl"
            width="100%"
            height="600"
            style="border:0;"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
          ></iframe>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
</script>

<style scoped>
.v-sheet {
  border-radius: 0;
}

.contact-list .v-list-item {
  min-height: 64px;
}

.hero-section {
  background: linear-gradient(rgba(33, 33, 33, 0.9), rgba(33, 33, 33, 0.9))
}

.contact-sheet {
  transition: all 0.3s ease;
}

.contact-sheet:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.map-sheet {
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

.promotions-section {
  min-height: 400px;
  padding: 1rem 0;
}

.promotion-card {
  height: 100%;
  transition: transform 0.3s ease;
  background-color: rgba(33, 33, 33, 0.9);
  border: 2px solid transparent;
  max-height: 300px;
}

.promotion-card:hover {
  transform: translateY(-10px);
  border-color: var(--v-primary-base);
}
</style>


