
// form validation

const form = document.querySelector('#form');
const reponame = document.querySelector('#reponames');
const SourceBucket = document.querySelector('#sourceBucket');
const DestinationBucket = document.querySelector('#destinationBucket');
const MonthDate = document.querySelector('#monthDate');
const radioButtons = document.querySelectorAll('input[name="radio"]')
const radioSelects = document.querySelectorAll('input[name="sink"]')
const btn = document.querySelector('#button');

btn.addEventListener("click", () => {
  let selectOption;
  for (const radiobutton of radioButtons) {
    if (radiobutton.checked) {
      selectOption = radiobutton.value;
      break;
    }
  }
  output.innerText = selectOption ? `` : `value is not selected`;
})

btn.addEventListener("click", () => {
  let selectSelect;
  for (const radioSelect of radioSelects) {
    if (radioSelect.checked) {
      selectSelect = radioSelect.value;
      break;
    }
  }
  output1.innerText = selectSelect ? `` : `value is not selected`;
})

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
})

function validateInputs(){
  const reponameval = reponame.value.trim()
  const SourceBucketVal = SourceBucket.value.trim()
  const DestinationBucketVal = DestinationBucket.value.trim()
  const MonthDateVal = MonthDate.value.trim()
  allConditionstrue = true ;
  

  if(reponameval === ''){
    setError(reponame,'reponame is Invalid');
    allConditionstrue = false ;
  }
  else if(validateEmail(reponameval)){
    setError(reponame,'space and Symbol not valid');
    allConditionstrue = false ;
  }
  else{
    setSuccess(reponame)
  }

  if(SourceBucketVal === ''){
    setError(SourceBucket,'SourceBucket is Invalid');
    allConditionstrue = false ;
  }
  else if (!FirstLetter.test(SourceBucketVal)) {
    setError(SourceBucket, 'First Letter must start with small Letter');
    allConditionstrue = false ;
  }
  else if(validateEmail(SourceBucketVal)){
    setError(SourceBucket,'space and Symbol not valid');
    allConditionstrue = false ;
  }
  else{
    setSuccess(SourceBucket)
  }

  if(DestinationBucketVal === ''){
    setError(DestinationBucket,'Detination Bucket is Invalid');
    allConditionstrue = false ;
  }
  else if (!FirstLetter.test(DestinationBucketVal)) {
    setError(DestinationBucket, 'First Letter must start with small Letter');
    allConditionstrue = false ;
  }
  else if(validateEmail(DestinationBucketVal)){
    setError(DestinationBucket,'space and Symbol not valid');
    allConditionstrue = false ;
  }
  else{
    setSuccess(DestinationBucket)
  }  


  if(MonthDateVal === ''){
    setError(MonthDate,'Month/Date/year is Invalid');
    allConditionstrue = false ;
  }
  else{
    setSuccess(MonthDate)
  } 

  if(allConditionstrue){
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
    /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~]/
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
