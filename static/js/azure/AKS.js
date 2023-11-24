// form validation

const form = document.querySelector('#form');
const resourcegroup = document.querySelector('#Resourcegroup');
const Kcs = document.querySelector('#KCS');
const Vmsize = document.querySelector('#vmsize');
const Vnetid = document.querySelector('#vnetid');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
  symbol();
})

function validateInputs(){
  const resourceVal = resourcegroup.value.trim()
  const KcsVal = Kcs.value.trim()
  const vmVal = Vmsize.value.trim()
  const vnetVal = Vnetid.value.trim()
  allConditionsTrue = true ;

  if(resourceVal === ''){
    setError(resourcegroup,'ResourceValue is Invalid');
    allConditionsTrue = false ;
  }
  else if(symbol(resourceVal)){
    setError(resourcegroup,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(resourcegroup)
  }
  
  if(KcsVal === ''){
    setError(Kcs,'kubernetes Cluster Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(KcsVal)) {
    setError(Kcs, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(KcsVal)){
    setError(Kcs,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (KcsVal.match(/[A-Z]/)){
    setError(Kcs,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Kcs)
  }
  if(vmVal === ''){
    setError(Vmsize,'VmSize is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(vmVal)) {
    setError(Vmsize, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(vmVal)){
    setError(Vmsize,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Vmsize)
  }
  if(vnetVal === ''){
    setError(Vnetid,'Vnet ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(vnetVal)) {
    setError(Vnetid, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(vnetVal)){
    setError(Vnetid,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (vnetVal.match(/[A-Z]/)){
    setError(Vnetid,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Vnetid)
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
    /[ `!@#$%^&*()+\_=\[\]{};':"\\|,.<>\/?~]/
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