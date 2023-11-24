
// form validation

const form = document.querySelector('#form');
const SpannerName = document.querySelector('#spannerName');
const SpannerDatabase = document.querySelector('#spannerDatabase');
const radioButtons = document.querySelectorAll('input[name="radio"]')
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

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs(){
  const SpannerNameVal = SpannerName.value.trim()
  const SpannerDatabaseVal = SpannerDatabase.value.trim()
  allConditionTrue = true ;
 

  if(SpannerNameVal === ''){
    setError(SpannerName,'Spanner Name is Invalid');
    allConditionTrue = false ;
  }
  else if (!FirstLetter.test(SpannerNameVal)) {
    setError(SpannerName, 'First Letter must start with small Letter');
    allConditionTrue = false ;
  }
  else if(validateEmail(SpannerNameVal)){
    setError(SpannerName,'Number,Space and Symbol not valid');
    allConditionTrue = false ;
  }
  else{
    setSuccess(SpannerName)
  }
  
  if(SpannerDatabaseVal === ''){
    setError(SpannerDatabase,'Spanner DataBase is Invalid');
    allConditionTrue = false ;
  }
  else if (!FirstLetter.test(SpannerDatabaseVal)) {
    setError(SpannerDatabase, 'First Letter must start with small Letter');
    allConditionTrue = false ;
  }
  else if(validate(SpannerDatabaseVal)){
    setError(SpannerDatabase,'Symbol and Space not Valid');
    allConditionTrue = false ;
  }
  else{
    setSuccess(SpannerDatabase)
  }
  if(allConditionTrue){
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
    /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~]/
  );
};

const validate = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~]/
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
