
// form validation

const form = document.querySelector('#form');
const FunctionName = document.querySelector('#functionName');
const VpcId = document.querySelector('#vpcId');
const radioButtons = document.querySelectorAll('input[name="publish"]')
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
})

function validateInputs() {
  const FunctionNameVal = FunctionName.value.trim()
  const VpcIdVal = VpcId.value.trim()
  allConditionsTrue = true ;



  if (FunctionNameVal === '') {
    setError(FunctionName, 'Function Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(FunctionNameVal)) {
    setError(FunctionName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validateEmail(FunctionNameVal)) {
    setError(FunctionName, 'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(FunctionName)
  }

  if (VpcIdVal === '') {
    setError(VpcId, 'VPC ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(VpcIdVal)) {
    setError(VpcId, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validateEmail(VpcIdVal)) {
    setError(VpcId, 'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
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
      /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~1234567890]/
    );
};

const FirstLetter = /^[ a-z]/