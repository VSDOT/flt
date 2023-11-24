let passwordInput = document.getElementById('txtPassword'),
    toggle = document.getElementById('btnToggle'),
    icon =  document.getElementById('eyeIcon');

function togglePassword() {
  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    icon.classList.add("fa-eye-slash");
    //toggle.innerHTML = 'hide';
  } else {
    passwordInput.type = 'password';
    icon.classList.remove("fa-eye-slash");
    //toggle.innerHTML = 'show';
  }
}

function checkInput() {
  //if (passwordInput.value === '') {
  //toggle.style.display = 'none';
  //toggle.innerHTML = 'show';
  //  passwordInput.type = 'password';
  //} else {
  //  toggle.style.display = 'block';
  //}
}

toggle.addEventListener('click', togglePassword, false);
passwordInput.addEventListener('keyup', checkInput, false);



// password2


let passwordInput1 = document.getElementById('txtPassword1'),
    toggle1 = document.getElementById('btnToggle1'),
    icon1 =  document.getElementById('eyeIcon1');

function togglePassword1() {
  if (passwordInput1.type === 'password') {
    passwordInput1.type = 'text';
    icon1.classList.add("fa-eye-slash");
    //toggle.innerHTML = 'hide';
  } else {
    passwordInput1.type = 'password';
    icon1.classList.remove("fa-eye-slash");
    //toggle.innerHTML = 'show';
  }
}

function checkInput() {
  //if (passwordInput.value === '') {
  //toggle.style.display = 'none';
  //toggle.innerHTML = 'show';
  //  passwordInput.type = 'password';
  //} else {
  //  toggle.style.display = 'block';
  //}
}

toggle1.addEventListener('click', togglePassword1, false);
passwordInput1.addEventListener('keyup', checkInput, false);


// Button Color Change
// form validation

const form = document.querySelector('#form');
const UserName = document.querySelector('#UserName');
const userEmail = document.querySelector('#userEmail');
const Password = document.querySelector('#txtPassword');
const cpassword = document.querySelector('#txtPassword1');


form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
})

function validateInputs(){
  const usernameVal = UserName.value.trim();
  const emailVal = userEmail.value.trim();
  const passwordVal = Password.value.trim();
  const cpasswordVal = cpassword.value.trim();
  allConditionsTrue = true;
  // if(usernameVal !== '' && emailVal !== '' && passwordVal !== '' && cpasswordVal !== ''){
  //   window.location.href = '../LoginForm/LogIn.html'
  // }

  if(usernameVal === ''){
    setError(UserName,'UserName is Invalid');
    allConditionsTrue = false;
  }
  else{
    setSuccess(UserName)
  }

  if(emailVal === ''){
    setError(userEmail,'UserEmail is Invalid');
    allConditionsTrue = false;
  }
  else if(!validateEmail(emailVal)){
    setError(userEmail,'Please Enter Valid Email');
    allConditionsTrue = false;
  }
  else{
    setSuccess(userEmail)
  }
  
  if(passwordVal === ''){
    setError(Password,'Password is Invalid');
    allConditionsTrue = false;
  }
  else if(passwordVal.length<8){
    setError(Password,'Enter Atleast 8 char');
    allConditionsTrue = false;
  }
  else{
    setSuccess(Password)
  }

  if(cpasswordVal === ''){
    setError(cpassword,'ConfirmPassword is Invalid');
    allConditionsTrue = false;
  }
  else if(cpasswordVal !== passwordVal){
  setError(cpassword,'Password dose Not Matched');
  allConditionsTrue = false;
  }
  else{
    setSuccess(cpassword)
  }
   if(allConditionsTrue){
      form.submit();
   }
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

const validateEmail = (email) => {
  return String(email)
  .toLowerCase()
  .match(
    /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
  );
};