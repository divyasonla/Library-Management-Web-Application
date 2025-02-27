<template>
  <div class="p-6  text-white min-h-screen">
    <h1 class="text-2xl font-bold mb-4">Transactions</h1>
    <div v-if="loading" class="text-center text-lg">Loading...</div>
    <table v-else class="w-full border-collapse border border-gray-700">
      <thead>
        <tr class="bg-[#110079]">
          <th class="p-3 border border-gray-700">ID</th>
          <th class="p-3 border border-gray-700">Book</th>
          <th class="p-3 border border-gray-700">Member</th>
          <th class="p-3 border border-gray-700">Issue Date</th>
          <th class="p-3 border border-gray-700">Return Date</th>
          <th class="p-3 border border-gray-700">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in transactions" :key="transaction.name" class="bg-[#21295c]">
          <td class="p-3 border border-gray-700">{{ transaction.name }}</td>
          <td class="p-3 border border-gray-700">{{ transaction.book }}</td>
          <td class="p-3 border border-gray-700">{{ transaction.member }}</td>
          <td class="p-3 border bo21295crder-gray-700">{{ transaction.issue_date }}</td>
          <td class="p-3 border border-gray-700">{{ transaction.return_date }}</td>
          <td class="p-3 border border-gray-700">{{ transaction.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { call } from "frappe-ui";

const transactions = ref([]);
const loading = ref(true);

const fetchTransactions = async () => {
  try {
    const response = await call("frappe.client.get_list", {
      doctype: "Transaction",
      fields: ["name", "book", "member", "issue_date", "return_date", "status"],
    });
    console.log("Response:", response);
    transactions.value = response;
  } catch (error) {
    console.error("Error fetching transactions:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchTransactions();
});
</script>
