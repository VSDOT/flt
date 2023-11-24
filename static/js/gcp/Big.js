
// form validation

const form = document.querySelector('#form');
const DatesetID = document.querySelector('#datesetID');
const FriendlyName = document.querySelector('#friendlyName');
const TableId = document.querySelector('#tableId');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs(){
  const DatesetIDVal = DatesetID.value.trim()
  const FriendlyNameVal = FriendlyName.value.trim()
  const TableIdVal = TableId.value.trim()
  allConditionsTrue = true ;

  if(DatesetIDVal === ''){
    setError(DatesetID,'DateSet ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(DatesetIDVal)) {
    setError(DatesetID, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
   else if(validateEmail(DatesetIDVal)){
    setError(DatesetID,'Number,Space and Symbol not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(DatesetID)
  }
  
  if(FriendlyNameVal === ''){
    setError(FriendlyName,'Friendly Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(FriendlyNameVal)) {
    setError(FriendlyName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(FriendlyNameVal)){
    setError(FriendlyName,'Number,Space and Symbol not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(FriendlyName)
  }
  if(TableIdVal === ''){
    setError(TableId,'Table ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!Firstletters.test(TableIdVal)) {
    setError(TableId, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(TableIdVal)){
    setError(TableId,'Space and Symbol not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(TableId)
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
    /[ `!@#$%^&*()+\=\[\]{};':"\\|,<>\/?~]/
  );
};

const FirstLetter = /^[ a-z]/

const Firstletters = /^[ a-z A-Z]/

// OPTION SCRIPT
$('.variant').change(function() {
  var size = $(".variant").get().map(function(el) {
    return el.value
  }).join(" / "); //get value of slected options and then join
  $("select#data >  option:contains(" + size + ")").prop('selected', true); //set selected value
});
