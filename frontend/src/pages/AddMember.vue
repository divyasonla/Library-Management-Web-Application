<template>
  <div class="p-6  text-white">
    <h1 class="text-3xl font-bold mb-6">ADD MEMBER</h1>

    <div class="mb-6 p-6 bg-gray-800 rounded-lg shadow-lg">
      <h2 class="text-lg font-semibold mb-4">{{ isEditing ? 'Update' : 'Add' }} Member</h2>

      <input 
        v-model="newMember.full_name" 
        type="text" 
        placeholder="Full Name" 
        class="p-3 border border-gray-700 rounded-md w-full bg-gray-700 text-white mb-3" 
      />
      <input 
        v-model="newMember.email" 
        type="email" 
        placeholder="Email" 
        class="p-3 border border-gray-700 rounded-md w-full bg-gray-700 text-white mb-3" 
      />
      <input 
        v-model="newMember.phone" 
        type="text" 
        placeholder="Phone Number" 
        class="p-3 border border-gray-700 rounded-md w-full bg-gray-700 text-white mb-3" 
      />

      <button 
        @click="saveMember" 
        class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md w-full"
      >
        {{ isEditing ? 'Update' : 'Add' }} Member
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { call } from "frappe-ui";

const newMember = ref({ full_name: "", email: "", phone: "" });
const isEditing = ref(false);

const saveMember = async () => {
  try {
    await call('frappe.client.insert', {
      doc: {
        doctype: "Member",
        full_name: newMember.value.full_name,
        email: newMember.value.email,
        phone: newMember.value.phone,
      }
    });
    alert("Member added successfully!");
    newMember.value = { full_name: "", email: "", phone: "" };
  } catch (error) {
    console.error("Error adding member:", error);
    alert("Failed to add member.");
  }
};
</script>

<style>
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 4px;
}
</style>
