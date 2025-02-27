<template>
  <div :class="{ dark: isDarkMode }" class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Top Bar -->
    <header class="flex items-center justify-between bg-white dark:bg-gray-800 p-4 shadow">
      <div class="flex items-center">
        <!-- Sidebar Toggle Icon -->
        <button @click="toggleSidebar" class="mr-4 text-gray-600 dark:text-gray-300 focus:outline-none">
          <font-awesome-icon :icon="sidebarVisible ? ['fas', 'times'] : ['fas', 'bars']" class="text-2xl" />
        </button>
        <h1 class="text-xl font-bold text-gray-800 dark:text-gray-100">Dashboard</h1>
      </div>
      <div class="flex items-center space-x-4">
        <!-- Single Dark/Light Mode Toggle Icon -->
        <button @click="toggleDarkMode" class="text-gray-600 dark:text-gray-300 focus:outline-none">
          <font-awesome-icon :icon="isDarkMode ? ['fas', 'sun'] : ['fas', 'moon']" class="text-xl" />
        </button>
        <!-- Logout Button -->
        <button @click="logout" class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 focus:outline-none">
          Logout
        </button>
      </div>
    </header>

    <div class="flex">
      <!-- Sidebar -->
      <aside
        v-show="sidebarVisible"
        class="w-64 bg-gray-800 text-white p-5 space-y-4 transition-all duration-300"
      >
        <!-- Optional: User Info -->
        <div class="flex items-center space-x-3">
          <img
            :src="session.userImg"
            alt="User Image"
            class="w-10 h-10 rounded-full object-cover"
          />
          <div>
            <h2 class="text-lg font-bold">{{ session.user }}</h2>
          </div>
        </div>
        <!-- Sidebar Menu with Icons -->
        <ul class="space-y-2">
          <li
            v-for="(item, index) in menuItems"
            :key="index"
            @click="selectedMenu = item.name"
            class="flex items-center p-2 cursor-pointer hover:bg-gray-700 rounded"
            :class="{ 'bg-gray-700': selectedMenu === item.name }"
          >
            <font-awesome-icon :icon="['fas', item.icon]" class="mr-3" />
            <span>{{ item.name }}</span>
          </li>
        </ul>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-5">
        <div v-if="selectedMenu === 'Books'">
          <book />
        </div>
        <div v-if="selectedMenu === 'Member List'">
          <member />
        </div>
        <div v-if="selectedMenu === 'Add New Member'">
          <h2 class="text-xl font-bold mb-4">Add New Member</h2>
          <addmember />
        </div>
        <div v-if="selectedMenu === 'Transactions'">
          <transactions />
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import book from './Books.vue';
import member from './Member.vue';
import addmember from './AddMember.vue';
import transactions from './Transactions.vue';
import { session } from '../data/session'; // Ensure this file exports session data

export default {
  name: 'DashboardLayout',
  components: {
    book,
    member,
    addmember,
    transactions,
    FontAwesomeIcon,
  },
  setup() {
    // Sidebar visibility toggle
    const sidebarVisible = ref(true);
    const toggleSidebar = () => {
      sidebarVisible.value = !sidebarVisible.value;
    };

    // Single Dark/Light mode toggle
    const isDarkMode = ref(false);
    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value;
    };

    // Logout (dummy logic)
    const logout = () => {
      console.log("Logging out...");
      // Add your logout logic here
    };

    // Define the menu items with icon names (only icon names here, full array used in template)
    const menuItems = ref([
      { name: 'Books', icon: 'book' },
      { name: 'Member List', icon: 'user' },
      { name: 'Add New Member', icon: 'user-plus' },
      { name: 'Transactions', icon: 'exchange-alt' },
    ]);

    const selectedMenu = ref('Books');

    return {
      sidebarVisible,
      toggleSidebar,
      isDarkMode,
      toggleDarkMode,
      logout,
      menuItems,
      selectedMenu,
      session,
    };
  },
};
</script>

<style scoped>
/* Example styles; adjust as needed */
html.dark {
  background-color: #1a202c;
}
</style>
