
// form validation

const form = document.querySelector('#form');
const InstanceName = document.querySelector('#instanceName');
const UserData = document.querySelector('#chooseFile');
const svcemail = document.querySelector('#email');


form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
})

function validateInputs(){
  const InstanceNameVal = InstanceName.value.trim()
  const UserDataVal = UserData.value.trim()
  const svcemailval = svcemail.value.trim()
  allConditionsTrue = true ;
  

 

  if(InstanceNameVal === ''){
    setError(InstanceName,'Instance Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(InstanceNameVal)) {
    setError(InstanceName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(InstanceNameVal)){
    setError(InstanceName,'space and Symbol not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(InstanceName)
  }

  if(UserDataVal === ''){
    setError(UserData,"it's invalid");
    allConditionsTrue = false ;
  }
  else{
    setSuccess(UserData)
  }  

  if(svcemailval === ''){
    setError(svcemail,'Account Email is Invalid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(svcemail)
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
    /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~]/
  );
};

const FirstLetter = /^[ a-z]/

 // FILE UPLOAD CODE

 $('#chooseFile').bind('change', function () {
  var filename = $("#chooseFile").val();
  if (/^\s*$/.test(filename)) {
    $(".file-upload").removeClass('active');
    $("#noFile").text("No file chosen..."); 
  }
  else {
    $(".file-upload").addClass('active');
    $("#noFile").text(filename.replace("C:\\fakepath\\", "")); 
  }
});



// OPTION SCRIPT
$('.variant').change(function() {
  var size = $(".variant").get().map(function(el) {
    return el.value
  }).join(" / "); //get value of slected options and then join
  $("select#data >  option:contains(" + size + ")").prop('selected', true); //set selected value
});


// FILE VALIDATION

function fileValidation() {
  var fileInput =
      document.getElementById('chooseFile');
   
  var filePath = fileInput.value;

  // Allowing file type
  var allowedExtensions =
/(\.txt|\.sh)$/i;
   
  if (!allowedExtensions.exec(filePath)) {
      alert('Invalid file type, use shell script format only');
      fileInput.value = '';
      return false;
  }
}
