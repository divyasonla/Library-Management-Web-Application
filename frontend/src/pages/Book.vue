<template>
  <div class="text-white p-6">
    <div class="mb-6">
      <h1 class="text-3xl font-bold">Book</h1>
      <p class="text-[rgb(145,209,255)]">List of all available books</p>
    </div>

    <!-- Search & Add Book -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
      <div class="mb-4 w-full md:w-1/3 md:mb-0">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search by Title, Author, or ISBN" 
          class="p-2 w-full rounded-md bg-gray-800 border border-gray-700 placeholder-gray-400 text-white"
        />
      </div>

      <button @click="toggleForm" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md">
        + Add New Book
      </button>
    </div>

    <!-- Add / Update Book Form -->
    <transition name="fade">
      <div v-if="showForm" class="mb-6 p-4 bg-[#21295c] rounded-md">
        <h2 class="text-xl font-semibold mb-4">{{ isEditing ? 'Update' : 'Add' }} Book</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <input v-model="newBook.title" type="text" placeholder="Title" class="p-2 border rounded-md bg-gray-700 text-white"/>
          <input v-model="newBook.author" type="text" placeholder="Author" class="p-2 border rounded-md bg-gray-700 text-white"/>
          <input v-model="newBook.isbn" type="text" placeholder="ISBN" class="p-2 border rounded-md bg-gray-700 text-white"/>
          <input v-model="newBook.stock" type="number" placeholder="Stock" class="p-2 border rounded-md bg-gray-700 text-white"/>
          <input v-model="newBook.status" type="text" placeholder="Status" class="p-2 border rounded-md bg-gray-700 text-white"/>
        </div>

        <div class="mt-4">
          <button @click="saveBook" class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md">
            {{ isEditing ? 'Update' : 'Add' }} Book
          </button>
          <button @click="toggleForm" class="ml-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md">
            Cancel
          </button>
        </div>
      </div>
    </transition>

    <!-- Books Grid -->
    <div v-if="filteredBooks.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <div v-for="book in paginatedBooks" :key="book.name" class="p-4 bg-[#21295c] rounded-md">
        <div class="mb-3">
          <img v-if="book.book_img" :src="book.book_img" alt="Book Cover" class="w-full h-40 object-cover rounded"/>
          <div v-else class="w-full h-40 bg-gray-600 rounded flex items-center justify-center text-gray-300">
            No Image
          </div>
        </div>

        <div>
          <h1 class="text-lg font-bold text-blue-400">{{ book.title }}</h1>
          <h3 class="text-sm text-gray-300">Author: {{ book.author }}</h3>
          <h3>ISBN: {{ book.isbn }}</h3>
          <h3>Stock: {{ book.stock }}</h3> 
          <h3>Status: {{ book.status }}</h3>
        </div>

        <div class="flex items-center mt-4">
          <button @click="editBook(book)" class="text-green-400 cursor-pointer mr-4">✏️ Edit</button>
          <button @click="deleteBook(book.name)" class="text-red-400 cursor-pointer">🗑️ Delete</button>
        </div>
      </div>
    </div>

    <p v-else class="text-gray-500 text-lg text-center mt-10">No results found.</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { createListResource, createDocumentResource } from 'frappe-ui';

// Book List Fetch
const books = createListResource({
  doctype: 'Book',
  fields: ['name', 'title', 'author', 'isbn', 'stock', 'status', 'book_img'],
  filters: [],
  limit: 10,
  order_by: 'modified desc',
});

// Form States
const showForm = ref(false);
const isEditing = ref(false);
const newBook = ref({
  title: '',
  author: '',
  isbn: '',
  stock: '',
  status: '',
});

// Search
const searchQuery = ref('');
const filteredBooks = computed(() => {
  return books.data.filter((book) =>
    book.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    book.author.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    book.isbn.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Pagination
const itemsPerPage = 5;
const currentPage = ref(1);
const paginatedBooks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredBooks.value.slice(start, start + itemsPerPage);
});

// Add / Edit Book
const selectedBook = ref(null);

function toggleForm() {
  showForm.value = !showForm.value;
  if (!showForm.value) resetForm();
}

function editBook(book) {
  isEditing.value = true;
  showForm.value = true;
  selectedBook.value = book;
  newBook.value = { ...book };
}

function saveBook() {
  if (isEditing.value) {
    // Update existing book
    createDocumentResource({ doctype: 'Book', name: selectedBook.value.name }).update(newBook.value);
  } else {
    // Add new book
    books.insert(newBook.value);
  }
  toggleForm();
}

// Delete Book
function deleteBook(bookName) {
  books.remove(bookName);
}

// Reset Form
function resetForm() {
  newBook.value = { title: '', author: '', isbn: '', stock: '', status: '' };
  isEditing.value = false;
  selectedBook.value = null;
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
