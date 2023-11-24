  // form validation

const form = document.querySelector('#form');
const Resourcegroup = document.querySelector('#resourcegroup');
const sqldatabase = document.querySelector('#Sqldatabase');
const sqlserver = document.querySelector('#Sqlserver');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs(){
  const resourcegroupVal = Resourcegroup.value.trim()
  const sqldatabaseVal = sqldatabase.value.trim()
  const sqlserverVal = sqlserver.value.trim()
  allConditionsTrue = true ;



  if(resourcegroupVal === ''){
    setError(Resourcegroup,'ResourceGroup ID is Invalid');
    allConditionsTrue = false ;
  }
  else if(validate(resourcegroupVal)){
    setError(Resourcegroup,'space dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Resourcegroup)
  }
  
  if(sqldatabaseVal === ''){
    setError(sqldatabase,'Sql DatBase Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(sqldatabaseVal)) {
    setError(sqldatabase, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(sqldatabaseVal)){
    setError(sqldatabase,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (sqldatabaseVal.match(/[A-Z]/)){
    setError(sqldatabase,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(sqldatabase)
  }

  if(sqlserverVal === ''){
    setError(sqlserver,'Sql Server ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(sqlserverVal)) {
    setError(sqlserver, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(sqlserverVal)){
    setError(sqlserver,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (sqlserverVal.match(/[A-Z]/)){
    setError(sqlserver,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(sqlserver)
  }

  if(allConditionsTrue){
    form.submit()
  }

  // if(administratorPasswordVal === ''){
  //     setError(administratorPassword,'Password is Invalid')
  //   }
  //   else if(administratorPasswordVal.length<8){
  //     setError(administratorPassword,'Enter Atleast 8 char')
  //   }
  //   else{
  //     setSuccess(administratorPassword)
  //   }


  
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
    /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~1234567890A-Z]/
  );
};

const validate = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\_=\[\]{};':"\\|,.<>\/?~]/
  );
};

const FirstLetter = /^[ a-z]/