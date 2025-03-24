async function fetchUsers() {
    try {
        const response = await fetch("http://127.0.0.1:8000/listusers", {
            headers: {
                "Authorization": `Bearer ${sessionStorage.getItem("access_token")}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch users");
        }

        const users = await response.json();
        displayUsers(users);
    } catch (error) {
        console.error("Error fetching users:", error);
        alert("Failed to fetch users. Please try again.");
    }
}

function displayUsers(users) {
    const userList = document.getElementById("user-list");
    userList.innerHTML = ""; // Clear existing content

    users.forEach(user => {
        const userCard = document.createElement("div");
        userCard.className = "user-card";
        userCard.innerHTML = `
            <h3>${user.fullname || "N/A"}</h3>
            <p><strong>Username:</strong> ${user.username || "N/A"}</p>
            <p><strong>Email:</strong> ${user.email || "N/A"}</p>
            <p><strong>Role:</strong> ${user.role || "N/A"}</p>
            <p><strong>Qualification:</strong> ${user.qualification || "N/A"}</p>
            <p><strong>Experience:</strong> ${user.experience || "N/A"}</p>
            <p><strong>Skill Set:</strong> ${user.skillSet || "N/A"}</p>
            <p><strong>Grade:</strong> ${user.grade || "N/A"}</p>
            <p><strong>Contact:</strong> ${user.contact || "N/A"}</p>
            <p><strong>Responsibility:</strong> ${user.responsibilities || "N/A"}</p>
            <div class="actions">
                <button onclick="showEditHistory('${user.userID}')">
                    <i class="fa-solid fa-history"></i> Show History
                </button>
                <button onclick="renameUser('${user.userID}')">
                    <i class="fa-solid fa-edit"></i> Change Role
                </button>
                <button onclick="deleteUser('${user.userID}')">
                    <i class="fa-solid fa-trash"></i> Delete
                </button>
            </div>
        `;
        userList.appendChild(userCard);
    });
}

function showEditHistory(userId) {
    alert(`Show history for user ID: ${userId}`);
}

function renameUser(userId) {
    alert(`Rename user ID: ${userId}`);
}

function deleteUser(userId) {
    alert(`Delete user ID: ${userId}`);
}

// Fetch and display users when the page loads
fetchUsers();