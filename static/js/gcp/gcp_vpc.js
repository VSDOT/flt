
// form validation

const form = document.querySelector('#form');
const Name = document.querySelector('#NAme');
const SunbetName = document.querySelector('#sunbetName');
const SubnetCidr = document.querySelector('#subnetCidr');
const RouteDest = document.querySelector('#routeDest');
const radioButtons = document.querySelectorAll('input[name="radio"]')
const btn = document.querySelector('#button');

btn.addEventListener("click", () => {
  let selectOption;
  for (const radiobutton of radioButtons) {
    if (radiobutton.checked) {
      selectOption = radiobutton.value;
      break;
    }
  }
  output.innerText = selectOption ? `` : `value is not selected`;
})


form.addEventListener('submit', (e) => {
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs() {
  const NameVal = Name.value.trim()
  const SunbetNameVal = SunbetName.value.trim()
  const SubnetCidrVal = SubnetCidr.value.trim()
  const RouteDestVal = RouteDest.value.trim()
  allConditionTrue = true ;





  if (NameVal === '') {
    setError(Name, 'Name is Invalid');
    allConditionTrue = false ;
  }
  else if (!FirstLetter.test(NameVal)) {
    setError(Name, 'First Letter must start with small Letter');
    allConditionTrue = false ;
  }
  else if (validateEmail(NameVal)) {
    setError(Name, 'symbol and Space dose not valid');
    allConditionTrue = false ;
  }
  else {
    setSuccess(Name)
  }

  if (SunbetNameVal === '') {
    setError(SunbetName, 'SubnetName is Invalid');
    allConditionTrue = false ;
  }
  else if (!FirstLetter.test(SunbetNameVal)) {
    setError(SunbetName, 'First Letter must start with small Letter');
    allConditionTrue = false ;
  }
  else if (validateEmail(SunbetNameVal)) {
    setError(SunbetName, 'symbol and Space dose not valid');
    allConditionTrue = false ;
  }
  else {
    setSuccess(SunbetName)
  }

  if (SubnetCidrVal === '') {
    setError(SubnetCidr, 'Subnet Cidr is Invalid');
    allConditionTrue = false ;
  } 
  else if (!FirstNumber.test(SubnetCidrVal)) {
    setError(SubnetCidr, 'First Start with Number');
    allConditionTrue = false ;
  }
  else if (validate(SubnetCidrVal)) {
    setError(SubnetCidr, 'Text and Space dose not valid');
    allConditionTrue = false ;
  }
  else {
    setSuccess(SubnetCidr)
  }

  if (RouteDestVal === '') {
    setError(RouteDest, 'RouteDest Range is Invalid');
    allConditionTrue = false ;
  }
  else if (!FirstNumber.test(RouteDestVal)) {
    setError(RouteDest, 'First Start with Number');
    allConditionTrue = false ;
  }
  else if (validate(RouteDestVal)) {
    setError(RouteDest, 'Text and Space dose not valid');
    allConditionTrue = false ;
  }
  else {
    setSuccess(RouteDest)
  }

  if(allConditionTrue){
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

function setError(element, message) {
  const inputGroup = element.parentElement;
  const errorElement = inputGroup.querySelector('.error')

  errorElement.innerText = message;
  inputGroup.classList.add('error')
  inputGroup.classList.remove('success')

}

function setSuccess(element) {
  const inputGroup = element.parentElement;
  const errorElement = inputGroup.querySelector('.error')

  errorElement.innerText = '';
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
      /[ `!@#$%^&*()+\-=\[\]{};':"\\|,<>\?~a-z]/
    );
};

const FirstLetter = /^[ a-z]/

const FirstNumber = /^[1-10000000000000000000000]/

// OPTION SCRIPT
$('.variant').change(function() {
  var size = $(".variant").get().map(function(el) {
    return el.value
  }).join(" / "); //get value of slected options and then join
  $("select#data >  option:contains(" + size + ")").prop('selected', true); //set selected value
});
