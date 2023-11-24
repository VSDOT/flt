// form validation

const form = document.querySelector('#form');
const Resourcegroup = document.querySelector('#resourcegroup');
const Sqlserver = document.querySelector('#sqlserver');
const administratorName = document.querySelector('#AdministratorName');
const administratorPassword = document.querySelector('#AdministratorPassword');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
  Symbol();
})

function validateInputs(){
  const resourcegroupVal = Resourcegroup.value.trim()
  const SqlserverVal = Sqlserver.value.trim()
  const administratorNameVal = administratorName.value.trim()
  const administratorPasswordVal = administratorPassword.value.trim()
  allConditionsTrue = true ;



  if(resourcegroupVal === ''){
    setError(Resourcegroup,'ResourceGroup ID is Invalid');
    allConditionsTrue = false ;
  }
  else if(Symbol(resourcegroupVal)){
    setError(Resourcegroup,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Resourcegroup)
  }
  
  if(SqlserverVal === ''){
    setError(Sqlserver,'SQL Server Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(SqlserverVal)) {
    setError(Sqlserver, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(SqlserverVal)){
    setError(Sqlserver,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (SqlserverVal.match(/[A-Z]/)){
    setError(Sqlserver,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Sqlserver)
  }

  if(administratorNameVal === ''){
    setError(administratorName,'Addministrator Login Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!startCaps.test(administratorNameVal)) {
    setError(administratorName, 'First Letter must start with Capital Letter');
    allConditionsTrue = false ;
  }
  else if(validate(administratorNameVal)){
    setError(administratorName,'space and symbol dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(administratorName)
  }

  if(administratorPasswordVal === ''){
      setError(administratorPassword,'Password is Invalid');
      allConditionsTrue = false ;
    }
    else if(administratorPasswordVal.length<8){
      setError(administratorPassword,'Enter Atleast 8 char');
      allConditionsTrue = false ;
    }
    else{
      setSuccess(administratorPassword)
    }
    
    if(allConditionsTrue){
      form.submit()
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

const validateEmail = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~1234567890]/
  );
};

const validate = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\=-\[\]{};':"\\|,.<>\/?~]/
  );
};

const Symbol = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\=_\[\]{};':"\\|,.<>\/?~]/
  );
};

const FirstLetter = /^[ a-z]/

const startCaps = /^[ A-Z]/