// form validation

const form = document.querySelector('#form');
const Resourcegroup = document.querySelector('#resourcegroup');
const functionApp = document.querySelector('#FunctionApp');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  symbol();
})

function validateInputs(){
  const resourcegroupVal = Resourcegroup.value.trim()
  const functionAppVal = functionApp.value.trim()
  allConditionsTrue  = true ;



  if(resourcegroupVal === ''){
    setError(Resourcegroup,'ResourceGroup ID is Invalid');
    allConditionsTrue  = false ;
  }
  else if(symbol(resourcegroupVal)){
    setError(Resourcegroup,'space dose not valid');
    allConditionsTrue  = false ;
  }
  else{
    setSuccess(Resourcegroup)
  }
  
  if(functionAppVal === ''){
    setError(functionApp,'Function App Name is Invalid');
    allConditionsTrue  = false ;
  }
  else if (!FirstLetter.test(functionAppVal)) {
    setError(functionApp, 'First Letter must start with small Letter');
    allConditionsTrue  = false ;
  }
  else if(validateEmail(functionAppVal)){
    setError(functionApp,'space and number dose not valid');
    allConditionsTrue  = false ;
  }
  else if (functionAppVal.match(/[A-Z]/)){
    setError(functionApp,'capital Letter not valid');
    allConditionsTrue  = false ;
  }
  else{
    setSuccess(functionApp)
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

// OPTION SCRIPT
$('.variant').change(function() {
  var size = $(".variant").get().map(function(el) {
    return el.value
  }).join(" / "); //get value of slected options and then join
  $("select#data >  option:contains(" + size + ")").prop('selected', true); //set selected value
});
