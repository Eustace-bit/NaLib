
async function fetchMembers() {
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
            throw new Error("Failed to fetch data");
        }
        const members = await response.json();
        return members;
        // return members;
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
}

async function fetchResources() {
    try {

        const accessToken = sessionStorage.getItem("access_token");
        
        // console.log(accessToken);
        if (!accessToken) {
            // throw new Error("No access token found. Please log in.");
            window.location.href = "login.html";

        }

        const cleanedToken = accessToken.replace(/^"(.*)"$/, '$1');
        
        const response = await fetch("http://127.0.0.1:8000/listbooks", {
            headers: {
                "Authorization": `Bearer ${cleanedToken}`
            }
        });
        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }
        const resources = await response.json();
        return resources;
        // return members;
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
}