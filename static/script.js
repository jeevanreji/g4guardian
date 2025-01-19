// Select elements for UI interactions
const createUserBtn = document.getElementById('createUserBtn');
const loginBtn = document.getElementById('loginBtn');
const userForm = document.getElementById('userForm');
const loginForm = document.getElementById('loginForm');

// Show the user form for registration
createUserBtn.addEventListener('click', () => {
    userForm.style.display = 'block';
    loginForm.style.display = 'none';
    document.querySelector('.hero').style.backgroundColor = '#66bb6a';
});

// Show the login form
loginBtn.addEventListener('click', () => {
    loginForm.style.display = 'block';
    userForm.style.display = 'none';
    document.querySelector('.hero').style.backgroundColor = '#388e3c';
});

// Handle user registration form submission
document.getElementById('createUserForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const role = document.getElementById('role').value;

    const response = await fetch('http://127.0.0.1:5000/users/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, role })
    });

    const data = await response.json();
    if (response.ok) {
        alert("User created successfully!");
        userForm.style.display = 'none';
    } else {
        alert("Error: " + data.error);
    }
});

// Handle user login form submission
document.getElementById('loginUserForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const userId = document.getElementById('userId').value;

    const response = await fetch(`http://127.0.0.1:5000/users/${userId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    const data = await response.json();
    if (response.ok) {
        alert("Login successful!");
        window.location.href = '/dashboard';  // Redirect to the dashboard
    } else {
        alert("Error: " + data.error);
    }
});
