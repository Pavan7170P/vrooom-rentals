async function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })  // ✅ Send JSON Data
        });

        const data = await response.json();
        console.log("Server Response:", data);

        if (response.ok) {
            localStorage.setItem("user_id", data.user_id);
            alert("Login successful!");
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong!");
    }
}
