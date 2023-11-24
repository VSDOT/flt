
  // form validation

  const form = document.querySelector('#form');
  const Resourcegroup = document.querySelector('#resourcegroup');
  const virtuallName = document.querySelector('#VirtuallName');
  const AddressPrefix = document.querySelector('#addressPrefix');
  const allowSSh = document.querySelector('#AllowSSh');
  const SourceAddress = document.querySelector('#sourceAddress');
  
  form.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateInputs();
    validate();
    symbol();
  })
  
  function validateInputs(){
    const resourcegroupVal = Resourcegroup.value.trim()
    const virtuallNameVal = virtuallName.value.trim()
    const AddressPrefixVal = AddressPrefix.value.trim()
    const allowSShVal = allowSSh.value.trim()
    const SourceAddressVal = SourceAddress.value.trim()
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
    
    if(virtuallNameVal === ''){
      setError(virtuallName,'Virtual Net Name is Invalid');
      allConditionsTrue = false ;      
    }
    else if (!FirstLetter.test(virtuallNameVal)) {
      setError(virtuallName, 'First Letter must start with small Letter');
      allConditionsTrue = false ;      
    }
    else if(validateEmail(virtuallNameVal)){
      setError(virtuallName,'space and number dose not valid');
      allConditionsTrue = false ;      
    }
    else if (virtuallNameVal.match(/[A-Z]/)){
      setError(virtuallName,'capital Letter not valid');
      allConditionsTrue = false ;      
    }
    else{
      setSuccess(virtuallName)
    }
    if(AddressPrefixVal === ''){
      setError(AddressPrefix,'Address Prefixs is Invalid');
      allConditionsTrue = false ;      
    }
    else if (!FirstNumber.test(AddressPrefixVal)) {
      setError(AddressPrefix, 'First start with Number');
      allConditionsTrue = false ;      
    }
    else if(validate(AddressPrefixVal)){
      setError(AddressPrefix,'Letters dose not valid');
      allConditionsTrue = false ;      
    }
    else{
      setSuccess(AddressPrefix)
    }
    if(allowSShVal === ''){
      setError(allowSSh,'Allow SSH is Invalid');
      allConditionsTrue = false ;      
    }
    else if(validate(allowSShVal)){
      setError(allowSSh,'Letters dose not valid');
      allConditionsTrue = false ;      
    }
    else if (!FirstNumber.test(allowSShVal)) {
      setError(allowSSh, 'First start with Number');
      allConditionsTrue = false ;      
    }
    else{
      setSuccess(allowSSh)
    }
    if(SourceAddressVal === ''){
      setError(SourceAddress,'Source Address is Invalid');
      allConditionsTrue = false ;      
    }
    else if(validate(SourceAddressVal)){
      setError(SourceAddress,'Letters dose not valid');
      allConditionsTrue = false ;      
    }
    else if (!FirstNumber.test(SourceAddressVal)) {
      setError(SourceAddress, 'First start with Number');
      allConditionsTrue = false ;      
    }
    else{
      setSuccess(SourceAddress)
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
      /[ !@#$%^&*()+\=\[\]{};':"\\|,<>\?~abcdefghijklmnopqrstuvwxyz]/
    );
  };  
  
  const symbol = (text) => {
    return String(text)
    .toLowerCase()
    .match(
      /[ !@#$%^&*()+\_=\[\]{};':"\\|,<>\?~]/
    );
  };

  const FirstLetter = /^[ a-z]/

  const FirstNumber = /^[1-10000000000000000000000]/