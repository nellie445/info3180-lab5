<template>

  <h2 class="viewing-title">Movies</h2>
  
  <div class="movie-view" id="movie-view">
    <div class="movie-card" v-for="movie in movies" :key="movie.id">
      
      <!-- Dynamically generate the poster URL using the movie's poster filename -->
      <img :src="getPosterUrl(movie.poster)" class="movie-poster" :alt="movie.title">

      <div class="movie-details">
        <h4 class="details-title">{{ movie.title }}</h4>
        <p class="details-description">{{ movie.description }}</p>
      </div>
    </div>
  </div>
</template>
  
<script setup>
  import { ref, onMounted } from "vue";
  let movies = ref([]);
  
  // Fetch movies data from the API when the component is mounted
  onMounted(async () => {
    try {
      const response = await fetch("/api/v1/movies");
      if (!response.ok) {
        throw new Error("Failed to fetch movies");
      }
      const data = await response.json();
      movies.value = data.movies;
    } catch (error) {
      console.error("Error fetching movies:", error);
    }
  });

  // Method to construct the poster URL
  function getPosterUrl(filename) {
    return `/api/v1/posters/${filename}`;
  }
</script>

<style scoped>

  .viewing-title {
    margin: 15px 50px 10px 50px;
    font-size: 24px;
    font-weight: bold;
  }

  .movie-view {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* Two columns with equal width */
    row-gap: 10px; /* Gap between grid items */
    column-gap: 70px;
    margin: 15px 50px 10px 50px;
  }

  .movie-card {
    width: auto; /* Make the card width dynamic based on content (image) */
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden; /* Ensure poster image stays within card bounds */
    display: grid;
    grid-template-columns: 200px 400px; /* Two columns with equal width */
    gap: 20px; /* Gap between grid items */
    height: 300px
  }

  .movie-poster {
    width: 100%; /* Ensure the image fills the container */
    height: 100%; /* Maintain aspect ratio */
    object-fit: cover; /* Scale the image to cover the entire container */
    border-radius: 10px 0 0 10px; /* Rounded corners at the top-left and bottom-left */
  }

  .movie-details {
    padding: 30px 30px 30px 10px; /* 20px top, 20px right, 20px bottom, 0 left */
    flex-grow: 1; /* Expand to fill remaining space */
  }


  .details-title {
    margin-bottom: 10px;
    font-size: 20px;
    font-weight: bold;
  }

  .details-description {
    font-size: 16px;
    line-height: 1.5;
  }
</style>

