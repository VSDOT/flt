
  // form validation

  const form = document.querySelector('#form');
  const NAme = document.querySelector('#Name');
  const uri = document.querySelector('#Uri');
  const StatusCode1 = document.querySelector('#statusCode1');
  const StatusCode2 = document.querySelector('#statusCode2');
  const StatusCode3 = document.querySelector('#statusCode3');
  const StatusCode4 = document.querySelector('#statusCode4');
  const storageName = document.querySelector('#StorageName');
  
  form.addEventListener('submit',(e)=>{
    console.log('submited')
    e.preventDefault();
    validateInputs();
    validate();
  })
  
  function validateInputs(){
    const nameVal = NAme.value.trim()
    const uriVal = uri.value.trim()
    // const StatusCode1Val = StatusCode1.value.trim()
    // const StatusCode2Val = StatusCode2.value.trim()
    // const StatusCode3Val = StatusCode3.value.trim()
    // const StatusCode4Val = StatusCode4.value.trim()
    const storageNameVal = storageName.value.trim()
    allConditionTrue = true ;
  
  
  
    if(nameVal === ''){
      setError(NAme,'Name is Invalid');
      allConditionTrue = false ;
    }
    else if (!FirstLetter.test(nameVal)) {
      setError(NAme, 'First Letter must start with small Letter');
      allConditionTrue = false ;
    }
    else if (validateEmail(nameVal)) {
      setError(NAme, 'space and symbol dose not valid');
      allConditionTrue = false ;
    }
    else{
      setSuccess(NAme)
    }
    
    if(uriVal === ''){
      setError(uri,'URI is Invalid');
      allConditionTrue = false ;
    }
    else if (!FirstLetter.test(uriVal)) {
      setError(uri, 'First Letter must start with small Letter');
      allConditionTrue = false ;
    }
    else{
      setSuccess(uri)
    }
    if(storageNameVal === ''){
        setError(storageName,'Storage Name is Invalid');
        allConditionTrue = false ;
      }
      else if (!FirstLetter.test(storageNameVal)) {
        setError(storageName, 'First Letter must start with small Letter');
        allConditionTrue = false ;
      }
      else if (validate(storageNameVal)) {
        setError(storageName, 'space,number and symbol dose not valid');
        allConditionTrue = false ;
      }
      else{
        setSuccess(storageName)
      }
    
    // if(StatusCode1Val === ''){
    //   setError(StatusCode1,'Status Code BOx Is Empty is Invalid')
    // }
    // else{
    //   setSuccess(StatusCode1)
    // }
    // if(StatusCode2Val === ''){
    //     setError(StatusCode2,'Status Code BOx Is Empty is Invalid')
    //   }
    //   else{
    //     setSuccess(StatusCode2)
    //   }
    //   if(StatusCode3Val === ''){
    //     setError(StatusCode3,'Status Code BOx Is Empty is Invalid')
    //   }
    //   else{
    //     setSuccess(StatusCode3)
    //   }
    //   if(StatusCode4Val === ''){
    //     setError(StatusCode4,'Status Code BOx Is Empty is Invalid')
    //   }
    //   else{
    //     setSuccess(StatusCode4)
    //   }
  
    // if(administratorPasswordVal === ''){
    //     setError(administratorPassword,'Password is Invalid')
    //   }
    //   else if(administratorPasswordVal.length<8){
    //     setError(administratorPassword,'Enter Atleast 8 char')
    //   }
    //   else{
    //     setSuccess(administratorPassword)
    //   }
    if( allConditionTrue){
    form.submit();
    }
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
      /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~1234567890]/
    );
  };


  const FirstLetter = /^[ a-z]/ 