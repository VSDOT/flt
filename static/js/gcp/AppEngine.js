
// form validation

const form = document.querySelector('#form');
const Service = document.querySelector('#service');
const Shell = document.querySelector('#shell');
const ZipSource = document.querySelector('#zipSource');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs(){
  const ServiceVal = Service.value.trim()
  const ShellVal = Shell.value.trim()
  const ZipSourceVal = ZipSource.value.trim()
  allConditionsTrue = true ;

  if(ServiceVal === ''){
    setError(Service,'Service is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(ServiceVal)) {
    setError(Service, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(ServiceVal)){
    setError(Service,'Symbol,Numbar and Space not Valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Service)
  }
  
  if(ShellVal === ''){
    setError(Shell,'Shell is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(ShellVal)) {
    setError(Shell, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(ShellVal)){
    setError(Shell,'Symbol,Numbar and Space not Valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Shell)
  }
  if(ZipSourceVal === ''){
    setError(ZipSource,'Zip Source is Invalid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(ZipSource)
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
    /[`!@#$%^&*()+\-=\[\]{};':"\\|,<>\/?~1234567890]/
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
