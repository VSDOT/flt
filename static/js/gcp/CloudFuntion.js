
// form validation

const form = document.querySelector('#form');
const CloudFunctionName = document.querySelector('#cloudFunctionName');
const mbsize = document.querySelector('#MemorySize');
const StorageBucket = document.querySelector('#storageBucket');
const bucketurl = document.querySelector('#bucketurl');
const entryPoint = document.querySelector('#entryPoint');
// const iamrole = document.querySelector('#iamrole');


form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
  LettersOnly();
})

function validateInputs(){
  const CloudFunctionNameVal = CloudFunctionName.value.trim()
  const mbsizeval = mbsize.value.trim()
  const StorageBucketVal = StorageBucket.value.trim()
  const bucketurlval = bucketurl.value.trim()
  const entryPointVal = entryPoint.value.trim()
  // const iamroleval = iamrole.value.trim()
  allConditionsTrue = true ;
 

  if(CloudFunctionNameVal === ''){
    setError(CloudFunctionName,'Cloud Function Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(CloudFunctionNameVal)) {
    setError(CloudFunctionName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(CloudFunctionNameVal)){
    setError(CloudFunctionName,'Number and Space Not Valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(CloudFunctionName)
  }
  //mb size empty validation for Python def
  if(mbsizeval === ''){
    setError(mbsize, 'MB Size not defined')
    allConditionsTrue = false;
  }
  else if(isNaN(mbsizeval)){
    setError(mbsize, 'Enter Numeric Value only')
    allConditionsTrue = false;
  }
  else{
    setSuccess(mbsize)
  }
  // end mb size validation

  if(StorageBucketVal === ''){
    setError(StorageBucket,'Storage Bucket Object is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(StorageBucketVal)) {
    setError(StorageBucket, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(StorageBucketVal)){
    setError(StorageBucket,'Number and Space Not Valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(StorageBucket)
  }

  if(entryPointVal === ''){
    setError(entryPoint,'Entry Point is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(entryPointVal)) {
    setError(entryPoint, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(LettersOnly(entryPointVal)){
    setError(entryPoint,'Number and Space Not Valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(entryPoint)
  }
  // iam role validation for python def
  // if(iamroleval === ''){
  //   setError(iamrole, 'iam role not defined')
  //   allConditionsTrue = false;
  // }
  // else{
  //   setSuccess(iamrole)
  // }
  // end of the iam role validation

  // bucket url empty validation for python
  if(bucketurlval == ''){
    setError(bucketurl, 'bucket url not defined')
    allConditionsTrue = false;
  }
  else{
    setSuccess(bucketurl)
  }
  // end bucket url validation

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
    /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~1234567890]/
  );
};

const validate = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ A-Z`!@#$%^&*()+\-=\[\]{};':"\\|,<>\/?~1234567890]/
  );
};

const LettersOnly = (text) => {
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
