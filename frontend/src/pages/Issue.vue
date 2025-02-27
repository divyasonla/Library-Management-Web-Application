<template>
  <div class="max-w-2xl mx-auto p-6 bg-[#21295c]">
    <h1 class="text-2xl text-white font-semibold mb-6">Transactions Form</h1>
    
    <form @submit.prevent="handleSubmit" class="space-y-4 ">
      <!-- Book Selection -->
      <div class="form-group">
        <label class="block text-sm font-medium mb-1 text-white">Book</label>
        <select 
          v-model="formData.book"
          class="w-full p-2 border rounded-md bg-white"
          required
        >
          <option value="" disabled>Select a book</option>
          <option v-for="book in books" :key="book.name" :value="book.name">
            {{ book.name }}
          </option>
        </select>
      </div>

      <!-- Show Selected Book Details -->
      <div v-if="selectedBook" class="form-group">
        <label class="block text-sm text-white font-medium mb-1">Selected Book Title</label>
        <input 
          type="text" 
          :value="selectedBook.title" 
          class="w-full p-2 border rounded-md bg-gray-100"
          readonly
        />
      </div>

      <!-- Member Selection -->
      <div class="form-group">
        <label class="block text-sm font-medium mb-1 text-white">Member</label>
        <select 
          v-model="formData.member"
          class="w-full p-2 border rounded-md bg-white"
          required
        >
          <option value="" disabled>Select a Member</option>
          <option v-for="member in members" :key="member.name" :value="member.name">
            {{ member.name }}
          </option>
        </select>
      </div>

      <!-- Show Selected Member Details -->
      <div v-if="selectedMember" class="form-group">
        <label class="block text-sm font-medium mb-1 text-white">Selected Member</label>
        <input 
          type="text" 
          :value="selectedMember.full_name" 
          class="w-full p-2 border rounded-md bg-gray-100"
          readonly
        />
      </div>

      <!-- Rent Fees -->
      <div class="form-group">
        <label class="block text-sm font-medium mb-1 text-white">Rent Fees</label>
        <input 
          type="number" 
          v-model="formData.rent_fees"
          class="w-full p-2 border rounded-md"
          step="0.01"
          min="0"
        />
      </div>

      <!-- Status -->
      <div class="form-group">
        <label class="block text-sm font-medium mb-1 text-white">Status</label>
        <select 
          v-model="formData.status"
          class="w-full p-2 border rounded-md bg-white"
          required
        >
          <option value="" disabled>Select status</option>
          <option v-for="status in statusOptions" :key="status" :value="status">
            {{ status }}
          </option>
        </select>
      </div>

      <div v-if="formData.status === 'Issued'" class="form-group">
        <label class="block text-sm font-medium mb-1 text-white">Issue Date</label>
        <input 
          type="date" 
          v-model="formData.issue_date"
          class="w-full p-2 border rounded-md"
          required
        />
      </div>
      <div v-if="formData.status === 'Returned'" class="form-group">
        <label class="block text-sm font-medium mb-1 text-white">Return Date</label>
        <input 
          type="date" 
          v-model="formData.return_date"
          class="w-full p-2 border rounded-md"
          required
        />
      </div>

      <div class="form-group">
        <label class="block text-sm font-medium mb-1 text-white">Transaction Date</label>
        <input 
          type="date" 
          v-model="formData.transaction_date"
          class="w-full p-2 border rounded-md"
          required
        />
      </div>

      <div class="form-group">
        <label class="block text-sm font-medium mb-1 text-white">Outstanding Dept</label>
        <input 
          type="number" 
          v-model="formData.outstanding_dept"
          class="w-full p-2 border rounded-md"
          step="0.01"
          min="0"
        />
      </div>

      <div class="flex justify-end space-x-3 mt-6">
        <button 
          type="button" 
          @click="resetForm"
          class="px-4 py-2 border rounded-md hover:bg-gray-100"
        >
          Discard
        </button>
        <button 
          type="submit"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-800"
        >
          Save
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { call } from 'frappe-ui'

const books = ref([])
const members = ref([])
const statusOptions = ['Issued', 'Returned',]

const formData = ref({
  book: '',
  member: '',
  rent_fees: 0.00,
  status: '',
  transaction_date: '',
  outstanding_dept: 0.00,
  issue_date: '',
  return_date: ''
})

const fetchBooks = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: "Books",  
      fields: ['name', 'title', 'author', 'isbn', 'stock', 'status']
    });
    books.value = response;
  } catch (error) {
    console.error("Error fetching books:", error);
  }
};

const fetchMembers = async () => {
  try {
    const response = await call('frappe.client.get_list', {
      doctype: "Member",  
      fields: ['name', 'full_name', 'email', 'phone']
    });
    members.value = response;
  } catch (error) {
    console.error("Error fetching members:", error);
  }
};

onMounted(() => {
  fetchBooks();
  fetchMembers();
});

const selectedBook = computed(() => {
  return books.value.find(b => b.name === formData.value.book);
});

const selectedMember = computed(() => {
  return members.value.find(m => m.name === formData.value.member);
});

const handleSubmit = async () => {
  if (formData.value.outstanding_dept > 500) {
    alert("Error: Outstanding Dept cannot be more than 500!");
    return;
  }
  try {
    await call('frappe.client.insert', {
      doc: {
        doctype: "Transaction", 
        book: formData.value.book,
        member: formData.value.member,
        rent_fees: formData.value.rent_fees,
        status: formData.value.status,
        transaction_date: formData.value.transaction_date,
        outstanding_dept: formData.value.outstanding_dept,
        issue_date: formData.value.issue_date,  
        return_date: formData.value.return_date  
      }
    });
    alert("Transaction added successfully!");
    resetForm();
  } catch (error) {
    console.error("Error saving transaction:", error);
    alert("Error saving transaction. Please try again.");
  }
};

const resetForm = () => {
  formData.value = {
    book: '',
    member: '',
    rent_fees: 0.00,
    status: '',
    transaction_date: '',
    outstanding_dept: 0.00,
    issue_date: '',
    return_date: ''
  };
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}

input:focus, select:focus {
  outline: none;
  border-color: #000;
}

input[type="number"] {
  -moz-appearance: textfield;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
