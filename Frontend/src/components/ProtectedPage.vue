<template>
  <div class="protected-container">
    <div class="protected-box">
      <h2>Protected Page</h2>
      <p>{{ message }}</p>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const message = ref('');
const router = useRouter();
const token = localStorage.getItem('token');

const logout = () => {
  localStorage.removeItem('token');
  router.push('/'); // Redirect to login after logout
};

const getProtectedData = async () => {
  const response = await fetch("http://127.0.0.1:5000/api/v1/protected", {
    method: "GET",
    headers: { Authorization: `Bearer ${token}` }
  });

  const data = await response.json();
  if (response.ok) {
    message.value = data.message;
  } else {
    alert(data.msg);
    router.push('/'); // If token is invalid, redirect to login page
  }
};

onMounted(() => {
  if (!token) {
    router.push('/'); // If no token, redirect to login
  } else {
    getProtectedData();
  }
});
</script>

<style scoped>
.protected-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #ecf0f1;
}

.protected-box {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

p {
  font-size: 18px;
  color: #555;
  margin-bottom: 20px;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #c0392b;
}
</style>
