
// form validation

const form = document.querySelector('#form');
const Name = document.querySelector('#NAme');
const ImageName = document.querySelector('#imageName');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs(){
  const NameVal = Name.value.trim()
  const ImageNameVal = ImageName.value.trim()
  allConditionsTrue = true ;

 

  if(NameVal === ''){
    setError(Name,'Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(NameVal)) {
    setError(Name, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(NameVal)){
    setError(Name,'symbol,Number and Space not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Name)
  }

  if(ImageNameVal === ''){
    setError(ImageName,'ImageName is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(ImageNameVal)) {
    setError(ImageName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(ImageNameVal)){
    setError(ImageName,'Number and Space not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(ImageName)
  }
  if(allConditionsTrue){
    form.submit()
  }
  

  // if(emailVal === ''){
  //   setError(userEmail,'UserEmail is Invalid')
  // }
  // else if(!validateEmail(emailVal)){
  //   setError(userEmail,'Please Enter Valid Email')
  // }
  // else{
  //   setSuccess(userEmail)
  // }
  
  // if(passwordVal === ''){
  //   setError(Password,'Password is Invalid')
  // }
  // else if(passwordVal.length<8){
  //   setError(Password,'Enter Atleast 8 char')
  // }
  // else{
  //   setSuccess(Password)
  // }

  // if(cpasswordVal === ''){
  //   setError(cpassword,'ConfirmPassword is Invalid')
  // }
  // else if(cpasswordVal !== passwordVal){
  // setError(cpassword,'Password dose Not Matched')
  // }
  // else{
  //   setSuccess(cpassword)
  // }
}

function setError(element,message){
  const inputGroup = element.parentElement;
  const errorElement = inputGroup.querySelector('.error')

  errorElement.innerText = message ;
  inputGroup.classList.add('error')
  inputGroup.classList.remove('success')

}

function setSuccess(element){
  const inputGroup = element.parentElement;
  const errorElement = inputGroup.querySelector('.error')

  errorElement.innerText = '' ;
  inputGroup.classList.add('success')
  inputGroup.classList.remove('error')

}

const validateEmail = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~1234567890]/
  );
};

const validate = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\=\[\]{};':"\\|,<>\?~1234567890]/
  );
};

const FirstLetter = /^[ a-z]/

// OPTION SCRIPT
$('.variant').change(function() {
  var size = $(".variant").get().map(function(el) {
    return el.value
  }).join(" / "); //get value of slected options and then join
  $("select#data >  option:contains(" + size + ")").prop('selected', true); //set selected value
});

// LOADING ANIMATION

// static/script.js
document.addEventListener("DOMContentLoaded", function () {
  // Listen for the DOMContentLoaded event, which indicates that the page has loaded
  // This ensures that the JavaScript runs after the page elements are ready

  const myForm = document.getElementById("form");

  myForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the form from actually submitting

      // Show the loading animation
      document.getElementById("loading").style.display = "block";
      document.getElementById("button").disabled = true; // Disable the submit button

      // Simulate a delay (you can replace this with your actual form submission logic)
      setTimeout(function () {
          // Hide the loading animation
          document.getElementById("loading").style.display = "none";
          document.getElementById("button").disabled = false; // Enable the submit button

          // Submit the form
          myForm.submit();
      }, 68000); // Replace 3000ms with your desired delay time
  });
});


