
// form validation

const form = document.querySelector('#form');
const Name = document.querySelector('#NAme');
const Network = document.querySelector('#network');
const NodeSubnet = document.querySelector('#nodeSubnet');
const NodePoolName = document.querySelector('#nodePoolName');


form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs(){
  const NameVal = Name.value.trim()
  const NetworkVal = Network.value.trim()
  const NodeSubnetVal = NodeSubnet.value.trim()
  const NodePoolNameVal = NodePoolName.value.trim()
  allConditionsTrue = true ;
  

 

  if(NameVal === ''){
    setError(Name,'Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(NameVal)) {
    setError(Name, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(NameVal)){
    setError(Name,'space and Symbol not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Name)
  }

  if(NetworkVal === ''){
    setError(Network,'Network is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(NetworkVal)) {
    setError(Network, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(NetworkVal)){
    setError(Network,'Symbol and Space not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Network)
  }  

  if(NodeSubnetVal === ''){
    setError(NodeSubnet,'Node Subnet is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(NodeSubnetVal)) {
    setError(NodeSubnet, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(NodeSubnetVal)){
    setError(NodeSubnet,'Symbol and Space not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(NodeSubnet)
  } 

  if(NodePoolNameVal === ''){
    setError(NodePoolName,'Node Pool Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(NodePoolNameVal)) {
    setError(NodePoolName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(NodePoolNameVal)){
    setError(NodePoolName,'Symbol and Space not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(NodePoolName)
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

