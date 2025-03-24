async function fetchAndDisplayMembers() {
    try {

        const accessToken = sessionStorage.getItem("access_token");
        
        // console.log(accessToken);
        if (!accessToken) {
            // throw new Error("No access token found. Please log in.");
            window.location.href = "login.html";

        }

        const cleanedToken = accessToken.replace(/^"(.*)"$/, '$1');

        
        const response = await fetch("http://127.0.0.1:8000/listmembers", {
            headers: {
                "Authorization": `Bearer ${cleanedToken}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch members");
        }

        const members = await response.json();
        displayMembers(members);
    } catch (error) {
        console.error("Error fetching members:", error);
        alert("Failed to fetch members. Please try again.");
    }
}

function displayMembers(members) {
    const memberList = document.getElementById("member-list");
    memberList.innerHTML = ""; // Clear existing content

    members.forEach(member => {
        const memberCard = document.createElement("div");
        memberCard.className = "member-card";
        memberCard.innerHTML = `
            <h3>${member.fullname || "N/A"}</h3>
            <p><strong>Phone:</strong> ${member.phone || "N/A"}</p>
            <p><strong>Address:</strong> ${member.address || "N/A"}</p>
            <p><strong>Post Code:</strong> ${member.postCode || "N/A"}</p>
            <p><strong>Status:</strong> ${member.status || "N/A"}</p>
            <p><strong>Enrolled Date:</strong> ${new Intl.DateTimeFormat("en-US", {
                month: "long",
                day: "numeric",
                year: "numeric",
            }).format(new Date(member.dateEnrolled))}</p>
            <div class="actions">
                <button onclick="showEditHistory('${member.membershipID}')">
                    <i class="fa-solid fa-history"></i> Show History
                </button>
                <button onclick="renameMember('${member.membershipID}')">
                    <i class="fa-solid fa-edit"></i> Rename
                </button>
                <button onclick="deleteMember('${member.membershipID}')">
                    <i class="fa-solid fa-trash"></i> Delete
                </button>
            </div>
        `;
        memberList.appendChild(memberCard);
    });
}

async function exportMemberData() {
    try {
        const accessToken = sessionStorage.getItem("access_token");

        // console.log(accessToken);
        if (!accessToken) {
            // throw new Error("No access token found. Please log in.");
            window.location.href = "login.html";

        }

        const cleanedToken = accessToken.replace(/^"(.*)"$/, '$1');


        const response = await fetch("http://127.0.0.1:8000/listmembers", {
            headers: {
                "Authorization": `Bearer ${cleanedToken}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch members for export");
        }

        const members = await response.json();

        // Convert members data to CSV format
        const csvContent = "data:text/csv;charset=utf-8," +
            "Full Name,Membership ID,Phone,Address,Post Code,Status,Enrolled Date\n" +
            members.map(member => 
                `"${member.fullname || ""}","${member.membershipID || ""}","${member.phone || ""}","${member.address || ""}","${member.postCode || ""}","${member.status || ""}","${new Intl.DateTimeFormat("en-US", {
                    month: "long",
                    day: "numeric",
                    year: "numeric",
                }).format(new Date(member.dateEnrolled))}"`
            ).join("\n");

        // Create a download link
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "members_data.csv");
        document.body.appendChild(link);
        link.click(); // Trigger the download
        document.body.removeChild(link); // Clean up
    } catch (error) {
        console.error("Error exporting member data:", error);
        alert("Failed to export member data. Please try again.");
    }
}

// Fetch and display members when the page loads

function showEditHistory(membershipID) {
    alert(`Show history for member ID: ${membershipID}`);
}

function renameMember(membershipID) {
    alert(`Rename member ID: ${membershipID}`);
}

function deleteMember(membershipID) {
    alert(`Delete member ID: ${membershipID}`);
}

// Fetch and display members when the page loads
fetchAndDisplayMembers();