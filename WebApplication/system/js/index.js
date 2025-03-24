async function addMember(event) {
    event.preventDefault();

    console.log("Adding a new member...");
    const formData = {
        fullname: document.getElementById("fullname").value,
        membershipID: document.getElementById("membershipID").value,
        phone: document.getElementById("phone").value,
        address: document.getElementById("address").value,
        postCode: document.getElementById("postCode").value,
        behaviour: document.getElementById("behaviour").value,
        enrolledDate: document.getElementById("enrolledDate").value
    };

    const response = await fetch("/addmember", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    });

    const result = await response.json();
    console.log(result);
    document.getElementById("result").innerText = JSON.stringify(result, null, 2);
}

function editBook(bookId) {
    const book = books.find(book => book.id === bookId);
    if (book) {
        // Populate the form with the book's details
        document.getElementById("title").value = book.title;
        document.getElementById("author").value = book.author;
        document.getElementById("genre").value = book.genre;
        document.getElementById("format").value = book.format;

        // Change the form to update mode
        const form = document.getElementById("add-book-form");
        form.onsubmit = (event) => {
            event.preventDefault();

            // Update the book's details
            book.title = document.getElementById("title").value;
            book.author = document.getElementById("author").value;
            book.genre = document.getElementById("genre").value;
            book.format = document.getElementById("format").value;

            renderBookList(); // Refresh the book list
            form.reset(); // Clear the form
            form.onsubmit = null; // Reset the form to add mode
        };
    }
}

// Function to delete a book
function deleteBook(bookId) {
    books = books.filter(book => book.id !== bookId); // Remove the book from the list
    renderBookList(); // Refresh the book list
}

// Render the initial book list
// renderBookList();

// function to add member

