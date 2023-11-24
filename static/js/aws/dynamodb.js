// form validation

const form = document.querySelector('#form');
const NAme = document.querySelector('#Name');
const radioButtons = document.querySelectorAll('input[name="billing"]')
const radioselects = document.querySelectorAll('input[name="stream"]')
const radioOptions = document.querySelectorAll('input[name="enable"]')
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

btn.addEventListener("click", () => {
  let selectValue;
  for (const radioselect of radioselects) {
    if (radioselect.checked) {
      selectValue = radioselect.value;
      break;
    }
  }
  output1.innerText = selectValue ? `` : `value is not selected`;
})

btn.addEventListener("click", () => {
  let selectButton;
  for (const radioOption of radioOptions) {
    if (radioOption.checked) {
      selectButton = radioOption.value;
      break;
    }
  }
  output2.innerText = selectButton ? `` : `value is not selected`;
})

form.addEventListener('submit', (e) => {
  e.preventDefault();
  validateInputs();
})

function validateInputs() {
  const NAmeVal = NAme.value.trim()
  allConditionsTrue = true ;



  if (NAmeVal === '') {
    setError(NAme, 'Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(NAmeVal)) {
    setError(NAme, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validateEmail(NAmeVal)) {
    setError(NAme, 'space and symbol dose not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(NAme)
  }

  if(allConditionsTrue){
    form.submit();
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
      /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~]/
    );
};



const FirstLetter = /^[ a-z]/ 