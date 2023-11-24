function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}


// DropDown2

function myFunction2() {
  document.getElementById("myDropdown2").classList.toggle("show");
}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput2");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}



// form validation

const form = document.querySelector('#form');
const Resourcegroup = document.querySelector('#resourcegroup');
const ContainerName = document.querySelector('#containerName');
const radioButtons = document.querySelectorAll('input[name="admin"]')
const radioselects = document.querySelectorAll('input[name="zone"]')
const btn = document.querySelector('#button');

btn.addEventListener("click",()=>{
  let selectOption;
  for( const radiobutton of radioButtons){
    if(radiobutton.checked){
      selectOption = radiobutton.value;
      break;
    }
  }
  output.innerText = selectOption ? `` : `value is not selected`;
})

btn.addEventListener("click",()=>{
  let selectValue;
  for( const radioselect of radioselects){
    if(radioselect.checked){
      selectValue = radioselect.value;
      break;
    }
  }
  output1.innerText = selectValue ? `` : `value is not selected`;
})

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  symbol();
})

function validateInputs(){
  const resourcegroupVal = Resourcegroup.value.trim()
  const ContainerNameVal = ContainerName.value.trim()
  allConditionsTrue = true ;

  if(resourcegroupVal === ''){
    setError(Resourcegroup,'ResourceGroup ID is Invalid');
    allConditionsTrue = false ;
  }
  else if(symbol(resourcegroupVal)){
    setError(Resourcegroup,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Resourcegroup)
  }
  
  if(ContainerNameVal === ''){
    setError(ContainerName,'ContainerName is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(ContainerNameVal)) {
    setError(ContainerName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(ContainerNameVal)){
    setError(ContainerName,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (ContainerNameVal.match(/[A-Z]/)){
    setError(ContainerName,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(ContainerName)
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
    /[ `!@#$%^&*()+\_=\[\]{};':"\\|,.<>\/?~1234567890]/
  );
};

const symbol = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\_=\[\]{};':"\\|,.<>\/?~]/
  );
};

const FirstLetter = /^[ a-z]/