<template>
  <div class="layout">
    <!-- Fixed Sidebar -->
    <div class="sidebar">
      <h2 class="sidebar-title">Library</h2>
      <h2 class="welcome-msg">
        Welcome {{ session.user }}!
      </h2>
      <img :src="session.userAvatar" alt="Profile" class="profile-img" />

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
      <component :is="currentComponent"></component>
    </div>
  </div>
</template>

<script>
import book from './Books.vue'
import member from './Member.vue'
import addmember from './AddMember.vue'
import transactions from './Transactions.vue'
import issue from './Issue.vue'
import login from './Login.vue'
import { session } from '../data/session'

export default {
  name: 'SidebarLayout',
  components: {
    book,
    member,
    addmember,
    transactions,
    issue,
    login
  },
  data() {
    return {
      menuItems: ['Books', 'Member List', 'Add New Member', 'Transactions', 'Issue', 'Login'],
      selectedMenu: 'Books',
      session: session
    };
  },
  computed: {
    currentComponent() {
      switch (this.selectedMenu) {
        case 'Books':
          return 'book';
        case 'Member List':
          return 'member';
        case 'Add New Member':
          return 'addmember';
        case 'Transactions':
          return 'transactions';
        case 'Issue':
          return 'issue';
        case 'Login':
          return 'login';
        default:
          return 'book';
      }
    }
  }
};
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 16rem;
  height: 100%;
  background-color: #21295c;
  color: white;
  padding: 1.25rem;
  overflow-y: auto;
}

.sidebar-title {
  font-size: 1.125rem;
  font-weight: bold;
  margin-bottom: 1.25rem;
}

.welcome-msg {
  font-weight: bold;
  font-size: 1.125rem;
  color: #f3f4f6;
  margin-bottom: 1rem;
}

.profile-img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1rem;
}

.menu-item {
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #374151;
}

.main-content {
  margin-left: 16rem;
  padding: 1.25rem;
  width: calc(100% - 16rem);
  height: 100vh;
  overflow-y: auto;
}
</style>
