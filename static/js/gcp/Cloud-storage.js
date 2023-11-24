
// form validation

const form = document.querySelector('#form');
const BucketName = document.querySelector('#bucketName');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
})

function validateInputs(){
  const BucketNameVal = BucketName.value.trim()
  allConditionsTrue = true ;
 

  if(BucketNameVal === ''){
    setError(BucketName,'Bucket Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(BucketNameVal)) {
    setError(BucketName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(BucketNameVal)){
    setError(BucketName,'Number,Space and Symbol not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(BucketName)
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

const validateEmail = (email) => {
  return String(email)
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