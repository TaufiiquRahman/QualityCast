// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
  };
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Register button event
document.getElementById('register').addEventListener('click', async function(event) {
  event.preventDefault();

  const name = document.getElementById('full-name').value;
  const phoneNumber = document.getElementById('phone-number').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  if (name === "" || phoneNumber === "" || email === "" || password === "") {
    alert("Please fill all the fields");
    return;
  }

  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    alert("Account created successfully");
    document.getElementById('reg-log').checked = false;  // Switch back to login view
    document.getElementById('login-email').value = "";
    document.getElementById('login-password').value = "";
  } catch (error) {
    console.error("Error:", error.message);
    alert(`Error: ${error.message}`);
  }
});

// Login button event
document.querySelector('.btn.mt-4').addEventListener('click', async function(event) {
  event.preventDefault();

  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    alert("Login successful");
    window.location.href = "http://localhost:8501";  // Redirect to Streamlit app
  } catch (error) {
    console.error("Error:", error.message);
    alert(`Error: ${error.message}`);
  }
});
