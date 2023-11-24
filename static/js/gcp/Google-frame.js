// SearchFilter
const searchBar = document.getElementById('SearchButtons');
searchBar.addEventListener('keyup', function(e) {
    const term = e.target.value.toLocaleLowerCase();
    const books = document.getElementsByTagName('button');
    Array.from(books).forEach(function(book) {
        const title = book.textContent;
        if (title.toLowerCase().indexOf(term) != -1) {
            book.parentElement.parentElement.style.display = 'flex';
        } else {
            book.parentElement.parentElement.style.display = 'none';
        }
    })
})

// Search Filter

function toggleShow () {
    var el = document.getElementById("box");
    el.classList.toggle("show");
  }

  // Iframe Page TargerPage

document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll(".click-button");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            var buttonId = button.id;
            console.log("Button with ID " + buttonId + " clicked");
            // Perform any desired actions here for each button
        });
    });

    // Retrieve anchor tag ID from localStorage
    var anchorId = localStorage.getItem("anchorId");
    if (anchorId) {
        console.log("Anchor tag ID from localStorage: " + anchorId);
        document.getElementById(anchorId).click(); // Trigger the corresponding button click
    }
});
