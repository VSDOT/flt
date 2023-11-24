  // form validation

  const form = document.querySelector('#form');
  const inst_name = document.querySelector('#txt1');
  const SubnetID = document.querySelector('#subnetID');
  const AmiId = document.querySelector('#amiId');
  const VolumeSize = document.querySelector('#volumeSize');
  const KeyName = document.querySelector('#keyName');
  const UserData = document.querySelector('#chooseFile');
  
  form.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateInputs();
  })
  
  function validateInputs(){
    const inst_nameval = inst_name.value.trim()
    const SubnetIDVal = SubnetID.value.trim()
    const AmiIdVal = AmiId.value.trim()
    const VolumeSizeVal = VolumeSize.value.trim()
    const KeyNameVal = KeyName.value.trim()
    const UserDataVal = UserData.value.trim()
    allConditionsTrue = true ;
  
    if(inst_nameval === ''){
      setError(inst_name,'instance name is Invalid');
      allConditionsTrue = false ;
    }
    else{
      setSuccess(inst_name)
    }
  
    if(SubnetIDVal === ''){
      setError(SubnetID,'Subnet ID is Invalid');
      allConditionsTrue = false ;
    }
    else if (!FirstLetter.test(SubnetIDVal)) {
      setError(SubnetID, 'First Letter must start with small Letter');
      allConditionsTrue = false ;
    }
    else if(validateEmail(SubnetIDVal)){
      setError(SubnetID,'space and symbol not valid');
      allConditionsTrue = false ;
    }
    else{
      setSuccess(SubnetID)
    }
    
    if(AmiIdVal === ''){
      setError(AmiId,'Ami ID is Invalid');
      allConditionsTrue = false ;
    }
    else if (!FirstLetter.test(AmiIdVal)) {
      setError(AmiId, 'First Letter must start with small Letter');
      allConditionsTrue = false ;
    }
    else if(validateEmail(AmiIdVal)){
      setError(AmiId,'space and symbol not valid');
      allConditionsTrue = false ;
    }
    else{
      setSuccess(AmiId)
    }

    if(VolumeSizeVal === ''){
        setError(VolumeSize,'VolumeSize is Invalid');
        allConditionsTrue = false ;
      }
      else{
        setSuccess(VolumeSize)
      }
    
    if(KeyNameVal === ''){
      setError(KeyName,'KeyName is Invalid');
      allConditionsTrue = false ;
    }
    else if (!FirstLetter.test(KeyNameVal)) {
      setError(KeyName, 'First Letter must start with small Letter');
      allConditionsTrue = false ;
    }
    else if(validateEmail(KeyNameVal)){
      setError(KeyName,'space and symbol not valid');
      allConditionsTrue = false ;
    }
    else{
      setSuccess(KeyName)
    }

    if(UserDataVal === ''){
        setError(UserData,"it's invalid");
        allConditionsTrue = false ;
      }
      else{
        setSuccess(UserData)
      }
      
    if( allConditionsTrue ){
      form.submit()
    }

  
  
    // if(administratorPasswordVal === ''){
    //     setError(administratorPassword,'Password is Invalid')
    //   }
    //   else if(administratorPasswordVal.length<8){
    //     setError(administratorPassword,'Enter Atleast 8 char')
    //   }
    //   else{
    //     setSuccess(administratorPassword)
    //   }
  
  
    
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

// FILE VALIDATION

function fileValidation() {
  var fileInput =
      document.getElementById('chooseFile');
   
  var filePath = fileInput.value;

  // Allowing file type
  var allowedExtensions =
/(\.txt|\.sh)$/i;
   
  if (!allowedExtensions.exec(filePath)) {
      alert('Invalid file type');
      fileInput.value = '';
      return false;
  }
}
