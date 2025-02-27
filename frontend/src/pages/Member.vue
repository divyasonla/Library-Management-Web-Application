<template>
  <div class="w-full p-6 shadow-lg rounded-lg">
    <h1 class="text-2xl font-bold text-white mb-4 text-center">Member List</h1>
    <div class="flex flex-col md:flex-row md:items-center md:justify-end mb-6">
  <!-- Search Input -->
  <div class="mb-4 md:mb-0 w-full lg:w-1/3 ml-auto">
    <input 
      v-model="searchQuery" 
      type="text" 
      placeholder="Search by Full Name, Email, or Phone" 
      class="p-2 w-full rounded-md bg-gray-800 border border-gray-700 placeholder-gray-400 text-white focus:outline-none focus:border-blue-500" 
    />
  </div>
</div>



    <div v-if="showForm" class="mb-4 p-4 bg-[#21295c] rounded-md">
      <h2 class="text-lg font-semibold mb-2">{{ isEditing ? 'Update' : 'Add' }} Member</h2>
      <input v-model="newBook.full_name" type="text" placeholder="FullName" class="p-2 border rounded-md w-full mb-2" />
      <input v-model="newBook.email" type="text" placeholder="Email" class="p-2 border rounded-md w-full mb-2" />
      <input v-model="newBook.phone" type="text" placeholder="Phone Number" class="p-2 border rounded-md w-full mb-2" />
      
      <button @click="saveBook" class="px-4 py-2 bg-green-500 text-white rounded-md">
        {{ isEditing ? 'Update' : 'Add' }} Member
      </button>
      <button @click="toggleForm" class="ml-2 px-4 py-2 bg-red-500 text-white rounded-md">Cancel</button>
    </div>

    <!-- Member Table -->
    <div v-if="filteredBooks.length" class="overflow-x-auto">
      <table class="min-w-full bg-[#21295c]">
        <thead>
          <tr class="bg-[#12094c] text-gray-100 uppercase text-sm leading-normal">
            <th class="py-3 px-4 text-left">FullName</th>
            <th class="py-3 px-4 text-left">Email</th>
            <th class="py-3 px-4 text-left">Phone Number</th>
            <th class="py-3 px-4 text-center">Actions</th>
          </tr>
        </thead>
        <tbody class="text-gray-400 text-sm">
          <tr v-for="book in paginatedBooks" :key="book.name" class="border-b border-gray-200 hover:bg-gray-100">
            <td class="py-3 px-4">{{ book.full_name }}</td>
            <td class="py-3 px-4">{{ book.email }}</td>
            <td class="py-3 px-4">{{ book.phone }}</td>
            <td class="py-3 px-4 text-center">
              <font-awesome-icon 
                @click="editBook(book)" 
                icon="pen" 
                class="text-green-600 cursor-pointer text-lg mr-4" 
              />
              <font-awesome-icon 
                @click="deleteBook(book.name)" 
                icon="trash" 
                class="text-red-600 cursor-pointer text-lg" 
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <p v-else class="text-gray-500 text-lg text-center">No results found.</p>

    <!-- Pagination -->
    <div class="flex justify-center mt-4" v-if="filteredBooks.length > itemsPerPage">
      <button 
        @click="prevPage" 
        :disabled="currentPage === 1" 
        class="px-4 py-2 border rounded mr-2 disabled:opacity-50"
      >
        Previous
      </button>
      <button 
        @click="nextPage" 
        :disabled="currentPage * itemsPerPage >= filteredBooks.length" 
        class="px-4 py-2 border rounded disabled:opacity-50"
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

// Fetch Member List from Frappe
const BookList = ref([]);
const fetchBooks = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: "Member",
      fields: ['name', 'full_name', 'email', 'phone']
    });
    BookList.value = response;
  } catch (error) {
    console.error("Error fetching members:", error);
  }
};
fetchBooks();

// Form & Toggle
const showForm = ref(false);
const toggleForm = () => { showForm.value = !showForm.value; };

// Form Data
const newBook = ref({ full_name: "", email: "", phone: "" });
const isEditing = ref(false);
const editingBookId = ref(null);

// Save (Add / Update) Member
const saveBook = async () => {
  try {
    if (isEditing.value) {
      await call('frappe.client.set_value', {
        doctype: "Member",
        name: editingBookId.value,
        fieldname: {
          full_name: newBook.value.full_name,
          email: newBook.value.email,
          phone: newBook.value.phone,
        }
      });
      alert("Member updated successfully!");
    } else {
      await call('frappe.client.insert', {
        doc: {
          doctype: "Member",
          full_name: newBook.value.full_name,
          email: newBook.value.email,   
          phone: newBook.value.phone,
        }
      });
      alert("Member added successfully!");
    }
    resetForm();
    fetchBooks();
    showForm.value = false;
  } catch (error) {
    console.error("Error saving member:", error);
    alert("Failed to save member.");
  }
};

// Edit Member
const editBook = (book) => {
  newBook.value = { ...book };
  isEditing.value = true;
  editingBookId.value = book.name;
  showForm.value = true;
};

// Delete Member
const deleteBook = async (bookId) => {
  try {
    if (confirm("Are you sure you want to delete this member?")) {
      await call('frappe.client.delete', { doctype: "Member", name: bookId });
      alert("Member deleted successfully!");
      fetchBooks();
    }
  } catch (error) {
    console.error("Error deleting member:", error);
    alert("Failed to delete member.");
  }
};

// Reset Form
const resetForm = () => {
  newBook.value = { full_name: "", email: "", phone: "" };
  isEditing.value = false;
  editingBookId.value = null;
};

// Search & Pagination
const searchQuery = ref("");
const currentPage = ref(1);
const itemsPerPage = 10;

const filteredBooks = computed(() => {
  if (!BookList.value || !Array.isArray(BookList.value)) return [];
  if (!searchQuery.value) return BookList.value;
  return BookList.value.filter(book =>
    book.full_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    book.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    book.phone.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const paginatedBooks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredBooks.value.slice(start, start + itemsPerPage);
});

watch(searchQuery, () => { currentPage.value = 1; });

const nextPage = () => { if (currentPage.value * itemsPerPage < filteredBooks.value.length) currentPage.value++; };
const prevPage = () => { if (currentPage.value > 1) currentPage.value--; };
</script>
