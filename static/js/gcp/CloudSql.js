
// form validation

const form = document.querySelector('#form');
const SqlInstanceName = document.querySelector('#sqlInstanceName');
const SqlUserName = document.querySelector('#sqlUserName');
const SqlPassword = document.querySelector('#sqlPassword');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs(){
  const SqlInstanceNameVal = SqlInstanceName.value.trim()
  const SqlUserNameVal = SqlUserName.value.trim()
  const SqlPasswordVal = SqlPassword.value.trim()
  allConditionsTrue = true ;

 

  if(SqlInstanceNameVal === ''){
    setError(SqlInstanceName,'SQL Instance Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(SqlInstanceNameVal)) {
    setError(SqlInstanceName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
   else if(validateEmail(SqlInstanceNameVal)){
    setError(SqlInstanceName,'Symbol and space is not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(SqlInstanceName)
  }

  if(SqlUserNameVal === ''){
    setError(SqlUserName,'SQL UserName is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(SqlUserNameVal)) {
    setError(SqlUserName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(SqlUserNameVal)){
    setError(SqlUserName,'Symbol,Number and space is not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(SqlUserName)
  }

  if(SqlPasswordVal === ''){
    setError(SqlPassword,'SQL Password is Invalid');
    allConditionsTrue = false ;
  }
  else if(SqlPasswordVal.length<8){
    setError(SqlPassword,'Enter Atleast 8 char');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(SqlPassword)
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
    /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~]/
  );
};

const validate = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~1234567890]/
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