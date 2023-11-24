// form validation

const form = document.querySelector('#form');
const Resourcegroup = document.querySelector('#resourcegroup');
const Appserverplan = document.querySelector('#appserverplan');
const Storagetype = document.querySelector('#storagetype');
const radioButtons = document.querySelectorAll('input[name="os_type"]')
const btn = document.querySelector('#button');

btn.addEventListener("click",()=>{
  var selectOption;
  for( const radiobutton of radioButtons){
    if(radiobutton.checked){
      selectOption = radiobutton.value;
      break;
    }
  }
  output.innerText = selectOption ? `` : `value is not selected`;
})

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
  symbol();
})

function validateInputs(){
  const resourcegroupVal = Resourcegroup.value.trim()
  const appserverplanVal = Appserverplan.value.trim()
  const storagetypeVal = Storagetype.value.trim()
  allConditionsTrue = true ;

  if(resourcegroupVal === ''){
    setError(Resourcegroup,'ResourceGroup is Invalid');
    allConditionsTrue = false ;
  }
  else if(symbol(resourcegroupVal)){
    setError(Resourcegroup,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Resourcegroup)
  }
  
  if(appserverplanVal === ''){
    setError(Appserverplan,'App Server Plan is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(appserverplanVal)) {
    setError(Appserverplan, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(appserverplanVal)){
    setError(Appserverplan,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (appserverplanVal.match(/[A-Z]/)){
    setError(Appserverplan,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Appserverplan)
  }
  if(storagetypeVal === ''){
    setError(Storagetype,'StorageType is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstCapital.test(storagetypeVal)) {
    setError(Storagetype, 'First Letter must start with capital Letter');
    allConditionsTrue = false ;
  }
  else if(validate(storagetypeVal)){
    setError(Storagetype,'space and dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Storagetype)
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


const validate = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~]/
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

const FirstCapital = /^[ A-Z]/