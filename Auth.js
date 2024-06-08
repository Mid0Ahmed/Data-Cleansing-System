let container = document.getElementById('container')

toggle = () => {
	container.classList.toggle('sign-in')
	container.classList.toggle('sign-up')
}

setTimeout(() => {
	container.classList.add('sign-in')
}, 200)


function validateSignUp() {
	const name = document.getElementById("nameInput").value;
	const username = document.getElementById("usernameInput").value;
	const email = document.getElementById("emailInput").value;
	const password = document.getElementById("passwordInput").value;
	const confirmPassword = document.getElementById("confirmPasswordInput").value;

	const nameRegex = /^[A-Za-z]{3,}$/;
	const usernameRegex = /^[A-Za-z][A-Za-z0-9]*$/;
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	const passwordRegex = /^.{6,}$/;

	let errorMessage = "";

	if (!nameRegex.test(name)) {
		document.getElementById("nameError").innerText = "Name must be at least 3 characters long.";
	} else {
		document.getElementById("nameError").innerText = "";
	}
	if (!usernameRegex.test(username)) {
		document.getElementById("usernameError").innerText = "Username must not start with a number and must contain only letters and numbers.";
	} else {
		document.getElementById("usernameError").innerText = "";
	}
	if (!emailRegex.test(email)) {
		document.getElementById("emailError").innerText = "Invalid email address format.";
	} else {
		document.getElementById("emailError").innerText = "";
	}
	if (!passwordRegex.test(password)) {
		document.getElementById("passwordError").innerText = "Password must be at least 6 characters long.";
	} else {
		document.getElementById("passwordError").innerText = "";
	}
	if (password !== confirmPassword) {
		document.getElementById("confirmPasswordError").innerText = "Passwords do not match.";
	} else {
		document.getElementById("confirmPasswordError").innerText = "";
	}
}

function submitSignUp() {
	// Retrieve existing user data or initialize an empty array
	let users = JSON.parse(localStorage.getItem('users')) || [];

	// Validate inputs
	const name = document.getElementById("nameInput").value;
	const username = document.getElementById("usernameInput").value;
	const email = document.getElementById("emailInput").value;
	const password = document.getElementById("passwordInput").value;
	const confirmPassword = document.getElementById("confirmPasswordInput").value;

	const nameRegex = /^[A-Za-z]{3,}$/;
	const usernameRegex = /^[A-Za-z][A-Za-z0-9]*$/;
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	const passwordRegex = /^.{6,}$/;

	let errorMessage = "";

	if (!nameRegex.test(name)) {
		document.getElementById("nameError").innerText = "Name must be at least 3 characters long.";
		return; // Prevent further execution if validation fails
	} else {
		document.getElementById("nameError").innerText = "";
	}
	if (!usernameRegex.test(username)) {
		document.getElementById("usernameError").innerText = "Username must not start with a number and must contain only letters and numbers.";
		return; // Prevent further execution if validation fails
	} else {
		document.getElementById("usernameError").innerText = "";
	}
	if (!emailRegex.test(email)) {
		document.getElementById("emailError").innerText = "Invalid email address format.";
		return; // Prevent further execution if validation fails
	} else {
		document.getElementById("emailError").innerText = "";
	}
	if (!passwordRegex.test(password)) {
		document.getElementById("passwordError").innerText = "Password must be at least 6 characters long.";
		return; // Prevent further execution if validation fails
	} else {
		document.getElementById("passwordError").innerText = "";
	}
	if (password !== confirmPassword) {
		document.getElementById("confirmPasswordError").innerText = "Passwords do not match.";
		return; // Prevent further execution if validation fails
	} else {
		document.getElementById("confirmPasswordError").innerText = "";
	}

	// Check if the email already exists
	const emailExists = users.some(user => user.email === email);
	if (emailExists) {
		document.getElementById("emailError").innerText = "Email already exists.";
		return; // Prevent further execution if email exists
	}

	// Create a new user object
	const newUser = {
		name: name,
		username: username,
		email: email,
		password: password
	};

	// Add the new user to the array of users
	users.push(newUser);

	// Save the updated user data to local storage
	localStorage.setItem('users', JSON.stringify(users));

	// Show success message
	document.getElementById("errorMessage").classList.remove("danger");
	document.getElementById("errorMessage").classList.add("success");
	document.getElementById("errorMessage").innerText = "Success! User is saved.";

	// Clear input fields
	document.getElementById("nameInput").value = "";
	document.getElementById("usernameInput").value = "";
	document.getElementById("emailInput").value = "";
	document.getElementById("passwordInput").value = "";
	document.getElementById("confirmPasswordInput").value = "";
}

function validateSignIn() {
	const signInEmail = document.getElementById("signInEmailInput").value;
	const signInPassword = document.getElementById("signInPasswordInput").value;

	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	const passwordRegex = /^.{6,}$/;

	if (!emailRegex.test(signInEmail)) {
		document.getElementById("signInEmailError").innerText = "Invalid email address format.";
	} else {
		document.getElementById("signInEmailError").innerText = "";
	}

	if (!passwordRegex.test(signInPassword)) {
		document.getElementById("signInPasswordError").innerText = "Password must be at least 6 characters long.";
	} else {
		document.getElementById("signInPasswordError").innerText = "";
	}
}

function submitSignIn() {
	const signInEmail = document.getElementById("signInEmailInput").value;
	const signInPassword = document.getElementById("signInPasswordInput").value;

	// Retrieve user data from local storage
	const users = JSON.parse(localStorage.getItem('users'));

	if (!users) {
		// If no users found, display error message
		document.getElementById("errorMessage").classList.remove("success");
		document.getElementById("errorMessage").classList.add("danger");
		document.getElementById("errorMessage").innerText = "No users found.";
		return;
	}

	// Find the user with matching email and password
	const matchedUser = users.find(user => user.email === signInEmail && user.password === signInPassword);

	if (matchedUser) {
		// If a user is found, display success message
		document.getElementById("errorMessag").classList.remove("danger");
		document.getElementById("errorMessag").classList.add("success");
		document.getElementById("errorMessag").innerText = "Success! Logged in.";
		console.log("loggedin")
	} else {
		// If no matching user found, display error message
		document.getElementById("errorMessag").classList.remove("success");
		document.getElementById("errorMessag").classList.add("danger");
		document.getElementById("errorMessag").innerText = "Incorrect email or password.";
		console.log("not logged in")
	}
}