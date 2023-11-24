// SearchBox
let inputBox = document.querySelector('.input-box'),
  searchIcon = document.querySelector('.search'),
  closeIcon = document.querySelector('.close-icon');
  let Azure = document.querySelector('.azure');
let Logo = document.querySelector('.logo');

// ---- ---- Open Input ---- ---- //
searchIcon.addEventListener('click', () => {
  inputBox.classList.add('open');
  Azure.style.display = "none";
  Logo.style.display = "block"
  document.getElementById('searchInput').style.background = 'white'
  document.getElementById('search-icon').style.color = 'black'
});
// ---- ---- Close Input ---- ---- //
closeIcon.addEventListener('click', () => {
  inputBox.classList.remove('open');
  Logo.style.display = "none";
  Azure.style.display = "block"
  document.getElementById('searchInput').style.background = 'none'
  document.getElementById('search-icon').style.color = 'white'
});


// Form Validation
// document.getElementById("myForm").addEventListener("submit", function (event) {
//   event.preventDefault(); // Prevent form submission

//   var Input1 = document.getElementById('formInput1').value;
//   var Input2 = document.getElementById('formInput2').value;
//   var Input3 = document.getElementById('formInput3').value;
//   var Input4 = document.getElementById('formInput4').value;

//   if (Input1 !== "" && Input2 !== "" && Input3 !== "" && Input4 !== "") {
//       // Both fields are filled, submit form or go to the next page
//       // Replace the following line with your desired action
//       window.location.href = "../Azure/index.html";
//   } else {
//       // Show alert message
//       alert("Please fill in all the required fields.");
//   }
// });

// SearchFilter
const searchBar = document.getElementById('searchInput');
searchBar.addEventListener('keyup', function(e) {
    const term = e.target.value.toLocaleLowerCase();
    const books = document.getElementsByTagName('h4');
    Array.from(books).forEach(function(book) {
        const title = book.textContent;
        if (title.toLowerCase().indexOf(term) != -1) {
            book.parentElement.parentElement.style.display = 'flex';
        } else {
            book.parentElement.parentElement.style.display = 'none';
        }
    })
})

//  Iframe Target Page

document
  .getElementById("anchor-button1")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button1");
  });

document
  .getElementById("anchor-button2")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button2");
  });

document
  .getElementById("anchor-button3")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button3");
  });

document
  .getElementById("anchor-button4")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button4");
  });

document
  .getElementById("anchor-button5")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button5");
  });

document
  .getElementById("anchor-button6")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button6");
  });

document
  .getElementById("anchor-button7")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button7");
  });

document
  .getElementById("anchor-button8")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button8");
  });

document
  .getElementById("anchor-button9")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button9");
  });
document
  .getElementById("anchor-button10")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button10");
  });
document
  .getElementById("anchor-button11")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button11");
  });
document
  .getElementById("anchor-button12")
  .addEventListener("click", function () {
    localStorage.setItem("anchorId", "button12");
  });


        // Add similar code for other anchor tags