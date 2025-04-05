<script setup>
import { ref } from "vue";

const username = ref("");
const password = ref("");
const token = ref(localStorage.getItem("token") || "");
const isAuthenticated = ref(!!token.value);
const message = ref("");

const login = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/v1/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username.value, password: password.value }),
    });

    const data = await response.json();
    if (response.ok) {
      token.value = data.access_token;
      localStorage.setItem("token", token.value);
      isAuthenticated.value = true;
    } else {
      alert(data.msg);
    }
  } catch (error) {
    console.error("Xatolik:", error);
  }
};

const getProtectedData = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/v1/protected", {
      method: "GET",
      headers: { Authorization: `Bearer ${token.value}` },
    });

    const data = await response.json();
    if (response.ok) {
      message.value = data.message;
    } else {
      alert(data.msg);
    }
  } catch (error) {
    console.error("Xatolik:", error);
  }
};

const logout = () => {
  token.value = "";
  localStorage.removeItem("token");
  isAuthenticated.value = false;
  message.value = "";
};
</script>

<template>
  <div class="app">
    <div class="auth-container">
      <h2>Vue.js + Flask JWT Auth</h2>

      <div v-if="!isAuthenticated" class="auth-form">
        <h3 class="form-title">Login</h3>
        <input
          type="text"
          v-model="username"
          class="input-field"
          placeholder="Username"
        />
        <input
          type="password"
          v-model="password"
          class="input-field"
          placeholder="Password"
        />
        <button @click="login" class="btn">Login</button>
      </div>

      <div v-if="isAuthenticated" class="protected-container">
        <h3 class="protected-title">Himoyalangan Sahifa</h3>
        <button @click="getProtectedData" class="btn">Get Protected Data</button>
        <p v-if="message" class="protected-message">{{ message }}</p>
        <button @click="logout" class="btn logout-btn">Logout</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* General layout */
.app {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa;
  font-family: 'Arial', sans-serif;
}

/* Auth container */
.auth-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

h3.form-title,
h3.protected-title {
  text-align: center;
  font-size: 20px;
  color: #2c3e50;
}

/* Input Fields */
.input-field {
  width: 94%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.input-field:focus {
  border-color: #3498db;
  outline: none;
}

/* Buttons */
.btn {
  width: 100%;
  padding: 12px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #2980b9;
}

/* Protected section */
.protected-container {
  margin-top: 20px;
}

.protected-message {
  font-size: 16px;
  color: #27ae60;
  margin-top: 10px;
}

/* Logout button */
.logout-btn {
  background-color: #e74c3c;
  margin-top: 20px;
}

.logout-btn:hover {
  background-color: #c0392b;
}

/* Mobile responsiveness */
@media (max-width: 480px) {
  .auth-container {
    width: 90%;
  }

  .btn {
    font-size: 14px;
  }

  .input-field {
    font-size: 14px;
  }
}
</style>
