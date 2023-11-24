
  // form validation

  const form = document.querySelector('#form');
  const Resourcegroup = document.querySelector('#resourcegroup');
  const VirtualNet = document.querySelector('#virtualNet');
  const virtualID = document.querySelector('#VirtualID');
  const adminUserName = document.querySelector('#AdminUserName');
  
  form.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateInputs();
    validate();
    symbol();
  })
  
  function validateInputs(){
    const resourcegroupVal = Resourcegroup.value.trim()
    const VirtualNetVal = VirtualNet.value.trim()
    const virtualIDVal = virtualID.value.trim()
    const adminUserNameVal = adminUserName.value.trim()
    allConditionsTrue = true ; 
  
  
  
    if(resourcegroupVal === ''){
      setError(Resourcegroup,'ResourceGroup ID is Invalid');
      allConditionsTrue = false ; 
    }
    else if(symbol(resourcegroupVal)){
      setError(Resourcegroup,'space dose not valid');
      allConditionsTrue = false ; 
    }
    else{
      setSuccess(Resourcegroup)
    }
    
    if(VirtualNetVal === ''){
      setError(VirtualNet,'Virtual Net is Invalid');
      allConditionsTrue = false ; 
    }
    else if (!FirstLetter.test(VirtualNetVal)) {
      setError(VirtualNet, 'First Letter must start with small Letter');
      allConditionsTrue = false ; 
    }
    else if(validateEmail(VirtualNetVal)){
      setError(VirtualNet,'space and number dose not valid');
      allConditionsTrue = false ; 
    }
    else if (VirtualNetVal.match(/[A-Z]/)){
      setError(VirtualNet,'capital Letter not valid');
      allConditionsTrue = false ; 
    }
    else{
      setSuccess(VirtualNet)
    }
    if(virtualIDVal === ''){
      setError(virtualID,'Virtual Network ID is Invalid');
      allConditionsTrue = false ; 
    }
    else if (!FirstLetter.test(virtualIDVal)) {
      setError(virtualID, 'First Letter must start with small Letter');
      allConditionsTrue = false ; 
    }
    else if(validateEmail(virtualIDVal)){
      setError(virtualID,'space and number dose not valid');
      allConditionsTrue = false ; 
    }
    else if (virtualIDVal.match(/[A-Z]/)){
      setError(virtualID,'capital Letter not valid');
      allConditionsTrue = false ; 
    }
    else{
      setSuccess(virtualID)
    }
    if(adminUserNameVal === ''){
      setError(adminUserName,'Admin User Name is Invalid');
      allConditionsTrue = false ; 
    }
    else if (!startCapital.test(adminUserNameVal)) {
      setError(adminUserName, 'First Letter must start with Capital Letter');
      allConditionsTrue = false ; 
    }
    else if(validate(adminUserNameVal)){
      setError(adminUserName,'space and symbol dose not valid');
      allConditionsTrue = false ; 
    }
    else{
      setSuccess(adminUserName)
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
      /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~1234567890]/
    );
  };

  const validate = (text) => {
    return String(text)
    .toLowerCase()
    .match(
      /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~]/
    );
  };

  const symbol = (text) => {
    return String(text)
    .toLowerCase()
    .match(
      /[ `!@#$%^&*()+\_=\[\]{};':"\\|,.<>\/?~]/
    );
  };

  const FirstLetter = /^[ a-z]/

  const startCapital = /^[ A-Z]/