

 // form validation

 const form = document.querySelector('#form');
 const inst_name = document.querySelector('#InstanceName');
 const UserName = document.querySelector('#userName');
 const Password = document.querySelector('#password');
 const DbName = document.querySelector('#dbName');
 const VpcId = document.querySelector('#vpcId');
 
 form.addEventListener('submit',(e)=>{
   e.preventDefault();
   validateInputs();
   validate();
 })
 
 function validateInputs(){
  const InstNameVal = inst_name.value.trim()
   const UserNameVal = UserName.value.trim()
   const PasswordVal = Password.value.trim()
   const DbNameVal = DbName.value.trim()
   const VpcIdVal = VpcId.value.trim()
   allConditionsTrue = true ;
  
   if(InstNameVal === ''){
    setError(inst_name,'Instance Name is Invalid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(inst_name)
  }
 
   if(UserNameVal === ''){
     setError(UserName,'User Name is Invalid');
     allConditionsTrue = false ;
   }
   else if (!FirstLetter.test(UserNameVal)) {
    setError(UserName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validate(UserNameVal)) {
    setError(UserName, 'space,number and symbol dose not valid');
    allConditionsTrue = false ;
  }
   else{
     setSuccess(UserName)
   }

     
  if(PasswordVal === ''){
    setError(Password,'Password is Invalid');
    allConditionsTrue = false ;
  }
  else if(PasswordVal.length<8){
    setError(Password,'Enter Atleast 8 char');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Password)
  }
   
   if(DbNameVal === ''){
     setError(DbName,'DB Name is Invalid');
     allConditionsTrue = false ;
   }
   else if (!FirstLetter.test(DbNameVal)) {
    setError(DbName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validate(DbNameVal)) {
    setError(DbName, 'space,number and symbol dose not valid');
    allConditionsTrue = false ;
  }
   else{
     setSuccess(DbName)
   }

   if(VpcIdVal === ''){
    setError(VpcId,'Vpc ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(VpcIdVal)) {
    setError(VpcId, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validate(VpcIdVal)) {
    setError(VpcId, 'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(VpcId)
  }

  if(allConditionsTrue){
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
    /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~]/
  );
};

const validate = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~1234567890]/
  );
};

const FirstLetter = /^[ a-z]/