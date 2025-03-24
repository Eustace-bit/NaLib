document.getElementById("signup-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const password = document.getElementById("password").value;
    const repassword = document.getElementById("repassword").value;
    const passwordStrength = checkPasswordStrength(password);
    if (password !== repassword) {
        // alert("Password does not match");
        document.getElementById("error").innerText = "Password does not match";
        
        return;
    }

    if (passwordStrength < 5) {
        // alert(`Password strength is ${passwordStrength}.`);
        document.getElementById("error").innerText = `Password strength is ${passwordStrength}.`;
        return;
    }else{
        // document.getElementById("error").innerText = "Password is strong";
        const formData = {
            username: document.getElementById("username").value,
            password: document.getElementById("password").value,
            role: "User"
        };


        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });
    
        const result = await response.json();
        console.log(result);
        document.getElementById("error").innerText = JSON.stringify(result, null, 2);
    }

    function checkPasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) {
            strength++;
        }
        if (/[A-Z]/.test(password)) {
            strength++;
        }
        if (/[a-z]/.test(password)) {
            strength++;
        }
        if (/[0-9]/.test(password)) {
            strength++;
        }
        if (/[!@#$%^&*]/.test(password)) {
            strength++;
        }
        return strength;
    }

    // if (checkPasswordStrength(password) < 3) {
    //     document.getElementById("error").innerText = "Password strength is not enough";
    //     // return;
    // }

    
});