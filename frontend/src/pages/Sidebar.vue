<template>
  <div class="layout">
    <!-- Fixed Sidebar -->
    <div class="sidebar">
      <h2 class="sidebar-title">Library Sidebar</h2>
      <h2 class="welcome-msg">
        Welcome {{ session.user }}!
      </h2>
      <img src="" alt="Profile">
      <ul>
        <li
          v-for="(item, index) in menuItems"
          :key="index"
          @click="selectedMenu = item"
          class="menu-item"
        >
          {{ item }}
        </li>
      </ul>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div v-if="selectedMenu === 'Books'">
        <book />
      </div>
      <div v-if="selectedMenu === 'Member List'">
        <member />
      </div>
      <div v-if="selectedMenu === 'Add New Member'">
        <h2>Add New Member</h2>
        <addmember />
      </div>
      <div v-if="selectedMenu === 'Transactions'">
        <transactions />
      </div>
      <div v-if="selectedMenu === 'Issue'">
        <issue />
      </div>
    </div>
  </div>
</template>

<script>
import book from './Books.vue'
import member from './Member.vue'
import addmember from './AddMember.vue'
import transactions from './Transactions.vue'
import issue from './Issue.vue'
import { session } from '../data/session'

export default {
  name: 'SidebarLayout',
  components: {
    book,
    member,
    addmember,
    transactions,
    issue
  },
  data() {
    return {
      menuItems: ['Books', 'Member List', 'Add New Member', 'Transactions', 'Issue'],
      selectedMenu: 'Books',
      session: session
    };
  }
};
</script>

<style scoped>
/* Layout container to handle sidebar and main content */
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Fixed Sidebar styles */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 16rem; /* 64px equivalent to Tailwind w-64 */
  height: 100%;
  background-color: #21295c;
  color: white;
  padding: 1.25rem; /* p-5 */
  overflow-y: auto; /* Agar sidebar me bhi scroll karna pade */
}

.sidebar-title {
  font-size: 1.125rem; /* text-lg */
  font-weight: bold;
  margin-bottom: 1.25rem; /* mb-5 */
}

.welcome-msg {
  font-weight: bold;
  font-size: 1.125rem;
  color: #4b5563; /* text-gray-600 */
  margin-bottom: 1rem; /* mb-4 */
}

.menu-item {
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 0.375rem; /* rounded */
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #374151; /* hover:bg-gray-700 */
}

/* Main content styles */
.main-content {
  margin-left: 16rem; /* Same as sidebar width */
  padding: 1.25rem;
  width: calc(100% - 16rem);
  height: 100vh;
  overflow-y: auto;
}
</style>
