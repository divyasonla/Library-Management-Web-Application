<template>
  <div class="text-white p-6 ">
    <div class="mb-6">
      <h1 class="text-3xl font-bold">Book</h1>
      <p class="text-[rgb(145,209,255)]">List of all available books</p>
    </div>

    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
      <div class="mb-4 w-full md:w-1/3 md:mb-0">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search by Title, Author, or ISBN" 
          class="p-2 w-full rounded-md bg-gray-800 border border-gray-700 placeholder-gray-400 text-white focus:outline-none focus:border-blue-500" 
        />
      </div>

      <button 
        @click="toggleForm" 
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md transition text-white"
      >
        + Add New Book
      </button>
    </div>

    <transition name="fade">
      <div v-if="showForm" class="mb-6 p-4 bg-[#21295c] rounded-md shadow-md">
        <h2 class="text-xl font-semibold mb-4">{{ isEditing ? 'Update' : 'Add' }} Book</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <input 
            v-model="newBook.title" 
            type="text" 
            placeholder="Title" 
            class="p-2 border border-gray-700 rounded-md bg-gray-700 text-white"
          />
          <input 
            v-model="newBook.author" 
            type="text" 
            placeholder="Author" 
            class="p-2 border border-gray-700 rounded-md bg-gray-700 text-white"
          />
          <input 
            v-model="newBook.isbn" 
            type="text" 
            placeholder="ISBN" 
            class="p-2 border border-gray-700 rounded-md bg-gray-700 text-white"
          />
          <input 
            v-model="newBook.stock" 
            type="number" 
            placeholder="Stock" 
            class="p-2 border border-gray-700 rounded-md bg-gray-700 text-white"
          />
          <input 
            v-model="newBook.status" 
            type="text" 
            placeholder="Status" 
            class="p-2 border border-gray-700 rounded-md bg-gray-700 text-white"
          />
        </div>

        <div class="mt-4">
          <button 
            @click="saveBook" 
            class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md"
          >
            {{ isEditing ? 'Update' : 'Add' }} Book
          </button>
          <button 
            @click="toggleForm" 
            class="ml-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md"
          >
            Cancel
          </button>
        </div>
      </div>
    </transition>

    <!-- Books Grid -->
    <div v-if="filteredBooks.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <div 
        v-for="book in paginatedBooks" 
        :key="book.name" 
        class="p-4 bg-[#21295c] rounded-md shadow-md flex flex-col justify-between transition transform hover:-translate-y-1 hover:shadow-lg"
      >
    

        <!-- Book Info -->
        <div>
          <h1 class="text-lg font-bold mb-1 text-blue-400">{{ book.name }}</h1>
          <div class="text-sm text-gray-300 mb-2">
              <h3>
                <strong>Title: </strong>
             {{ book.title }}
          </h3>
          <h3>
            Author: {{ book.author }}
          </h3>
            <h3>ISBN: {{ book.isbn }}</h3>
           <h3>Stock: {{ book.stock }}</h3> 
            <h3>Status: {{ book.status }}</h3>
          </div>
         
        </div>

        <!-- Actions -->
        <div class="flex items-center mt-4">
          <font-awesome-icon 
            @click="editBook(book)" 
            icon="pen" 
            class="text-green-400 cursor-pointer text-lg mr-4" 
            title="Edit"
          />
          <font-awesome-icon 
            @click="deleteBook(book.name)" 
            icon="trash" 
            class="text-red-400 cursor-pointer text-lg" 
            title="Delete"
          />
        </div>
      </div>
    </div>

    <!-- No Results -->
    <p v-else class="text-gray-500 text-lg text-center mt-10">No results found.</p>

    <div class="flex justify-center mt-6" v-if="filteredBooks.length > itemsPerPage">
      <button 
        @click="prevPage" 
        :disabled="currentPage === 1" 
        class="px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white mr-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Previous
      </button>
      <button 
        @click="nextPage" 
        :disabled="currentPage * itemsPerPage >= filteredBooks.length" 
        class="px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { call } from "frappe-ui";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPen, faTrash } from '@fortawesome/free-solid-svg-icons';

const BookList = ref([]);
const fetchBooks = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: "Books",
      fields: ['name', 'title', 'author', 'isbn', 'stock', 'status'],
      limit_page_length: 0 
    });
    BookList.value = response;
  } catch (error) {
    console.error("Error fetching books:", error);
  }
};
fetchBooks();

// Book Form & Toggle
const showForm = ref(false);
const toggleForm = () => { showForm.value = !showForm.value; };

// Book Form Data
const newBook = ref({ title: "", author: "", isbn: "", stock: "", status: "" });
const isEditing = ref(false);
const editingBookId = ref(null);

const saveBook = async () => {
  try {
    if (isEditing.value) {
      await call('frappe.client.set_value', {
        doctype: "Books",
        name: editingBookId.value,
        fieldname: {
          title: newBook.value.title,
          author: newBook.value.author,
          isbn: newBook.value.isbn,
          stock: newBook.value.stock,
          status: newBook.value.status
        }
      });
      alert("Book updated successfully!");
    } else {
      await call('frappe.client.insert', {
        doc: {
          doctype: "Books",
          title: newBook.value.title,
          author: newBook.value.author,
          isbn: newBook.value.isbn,
          stock: newBook.value.stock,
          status: newBook.value.status
        }
      });
      alert("Book added successfully!");
    }
    resetForm();
    fetchBooks();
    showForm.value = false;
  } catch (error) {
    console.error("Error saving book:", error);
    alert("Failed to save book.");
  }
};

// Edit Book
const editBook = (book) => {
  newBook.value = { ...book };
  isEditing.value = true;
  editingBookId.value = book.name;
  showForm.value = true;
};

// Delete Book
const deleteBook = async (bookId) => {
  try {
    if (confirm("Are you sure you want to delete this book?")) {
      await call('frappe.client.delete', { doctype: "Books", name: bookId });
      alert("Book deleted successfully!");
      fetchBooks();
    }
  } catch (error) {
    console.error("Error deleting book:", error);
    alert("Failed to delete book.");
  }
};

const resetForm = () => {
  newBook.value = { title: "", author: "", isbn: "", stock: "", status: "" };
  isEditing.value = false;
  editingBookId.value = null;
};

const searchQuery = ref("");
const currentPage = ref(1);
const itemsPerPage = 20;

const filteredBooks = computed(() => {
  if (!BookList.value || !Array.isArray(BookList.value)) return [];
  if (!searchQuery.value) return BookList.value;
  return BookList.value.filter(book =>
    book.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    book.author.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    book.isbn.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const paginatedBooks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredBooks.value.slice(start, start + itemsPerPage);
});

watch(searchQuery, () => { currentPage.value = 1; });

const nextPage = () => {
  if (currentPage.value * itemsPerPage < filteredBooks.value.length) {
    currentPage.value++;
  }
};
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
