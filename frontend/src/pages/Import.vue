<template>
  <div class="container">
    <h2>Import Books</h2>
    <div class="form-group">
      <label for="bookCount" class="text-white">Number of Books:</label>
      <input type="number" v-model="bookCount" min="1" class="form-control" />
    </div>
    <div class="form-group">
      <label for="bookTitle" class="text-white">Book Title (Optional):</label>
      <input type="text" v-model="bookTitle" class="form-control" />
    </div>
    <button @click="importBooks" class="btn btn-primary text-white">Import Books</button>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bookCount: 10, 
      bookTitle: "",
      message: ""
    };
  },
  methods: {
    async importBooks() {
      try {
        const response = await fetch("http://localhost:8080/api/method/library.library.api.import_books", {

          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "token c60e280acae152b:6a183b002df47f6" // ✅ Add API authentication
          },
          body: JSON.stringify({
            count: this.bookCount,
            title: this.bookTitle
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`); // ✅ Handle errors properly
        }

        const result = await response.json();
        this.message = result.message || "Books imported successfully!";
      } catch (error) {
        console.error("Error importing books:", error);
        this.message = `Error: ${error.message}`;
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.btn {
  width: 100%;
  margin-top: 10px;
}

.message {
  margin-top: 10px;
  color: green;
  font-weight: bold;
}
</style>
