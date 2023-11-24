// SearchBox
let inputBox = document.querySelector('.input-box'),
  searchIcon = document.querySelector('.search'),
  closeIcon = document.querySelector('.close-icon');
  let Google = document.querySelector('.google');
  let Logo = document.querySelector('.logo');

// ---- ---- Open Input ---- ---- //
searchIcon.addEventListener('click', () => {
  inputBox.classList.add('open');
  Google.style.display = "none";
  Logo.style.display = "block"
  document.getElementById('searchInput').style.background = 'white'
});
// ---- ---- Close Input ---- ---- //
closeIcon.addEventListener('click', () => {
  inputBox.classList.remove('open');
  Logo.style.display = "none";
  Google.style.display = "block"
  document.getElementById('searchInput').style.background = 'none'
});




var loader = document.getElementById('PreLoader');
function LoadFunction() {
    loader.style.display = "none";
}


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
// fileUploader
// $('#chooseFile').bind('change', function () {
//   var filename = $("#chooseFile").val();
//   if (/^\s*$/.test(filename)) {
//     $(".file-upload").removeClass('active');
//     $("#noFile").text("No file chosen...");
//   }
//   else {
//     $(".file-upload").addClass('active');
//     $("#noFile").text(filename.replace("C:\\fakepath\\", ""));
//   }
// });
// fileUploader

