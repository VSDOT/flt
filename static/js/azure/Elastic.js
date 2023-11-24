// form validation

const form = document.querySelector('#form');
const Resourcegroup = document.querySelector('#resourcegroup');
const elasticName = document.querySelector('#ElasticName');
const SqlServer = document.querySelector('#sqlServer');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  symbol();
})

function validateInputs(){
  const resourcegroupVal = Resourcegroup.value.trim()
  const elasticNameVal = elasticName.value.trim()
  const SqlServerVal = SqlServer.value.trim()
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
  
  if(elasticNameVal === ''){
    setError(elasticName,'Elastic Poll Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(elasticNameVal)) {
    setError(elasticName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(elasticNameVal)){
    setError(elasticName,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (elasticNameVal.match(/[A-Z]/)){
    setError(elasticName,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(elasticName)
  }

  if(SqlServerVal === ''){
    setError(SqlServer,'SQL Server is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(SqlServerVal)) {
    setError(SqlServer, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(SqlServerVal)){
    setError(SqlServer,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (SqlServerVal.match(/[A-Z]/)){
    setError(SqlServer,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(SqlServer)
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