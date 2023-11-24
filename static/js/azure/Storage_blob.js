
  // form validation

  const form = document.querySelector('#form');
  const Resourcegroup = document.querySelector('#resourcegroup');
  const StorageAccount = document.querySelector('#storageAccount');
  const radioButtons = document.querySelectorAll('input[name="anyone"]')
  const btn = document.querySelector('#button');

  btn.addEventListener("click",()=>{
    let selectOption;
    for( const radiobutton of radioButtons){
      if(radiobutton.checked){
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
    const resourcegroupVal = Resourcegroup.value.trim()
    const StorageAccountVal = StorageAccount.value.trim()
    allConditionsTrue = true ;
  
  
  
    if(resourcegroupVal === ''){
      setError(Resourcegroup,'ResourceGroup ID is Invalid');
      allConditionsTrue = false ;
    }
    // else if (!FirstLetter.test(resourcegroupVal)) {
    //   setError(Resourcegroup, 'First Letter must start with small Letter')
    // }
    else if(validate(resourcegroupVal)){
      setError(Resourcegroup,'space dose not valid');
      allConditionsTrue = false ;
    }
    else{
      setSuccess(Resourcegroup)
    }
    
    if(StorageAccountVal === ''){
      setError(StorageAccount,'Storage Account Name is Invalid');
      allConditionsTrue = false ;
    }
    else if (!FirstLetter.test(StorageAccountVal)) {
      setError(StorageAccount, 'First Letter must start with small Letter');
      allConditionsTrue = false ;
    }
    else if(validateEmail(StorageAccountVal)){
      setError(StorageAccount,'space and number dose not valid');
      allConditionsTrue = false ;
    }
    else if (StorageAccountVal.match(/[A-Z]/)){
      setError(StorageAccount,'capital Letter not valid');
      allConditionsTrue = false ;
    }
    else{
      setSuccess(StorageAccount)
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
      /[ `!@#$%^&*()+\_=\[\]{};':"\\|,.<>\/?~]/
    );
  };

  const FirstLetter = /^[ a-z]/
