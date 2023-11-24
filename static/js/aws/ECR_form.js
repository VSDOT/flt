

// form validation

const form = document.querySelector('#form');
const Name = document.querySelector('#Name');
const Repository = document.querySelector('#repository');
const radioButtons = document.querySelectorAll('input[name="mutability"]')
const radioselects = document.querySelectorAll('input[name="scan"]')
// const radioOptions = document.querySelectorAll('input[name="encryption"]')
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

// btn.addEventListener("click", () => {
//   let selectButton;
//   for (const radioOption of radioOptions) {
//     if (radioOption.checked) {
//       selectButton = radioOption.value;
//       break;
//     }
//   }
//   output2.innerText = selectButton ? `` : `value is not selected`;
// })

form.addEventListener('submit', (e) => {
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs() {
  const NameVal = Name.value.trim()
  // const RepositoryVal = Repository.value.trim()
  allConditionsTrue = true ;



  if (NameVal === '') {
    setError(Name, 'Subnet ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(NameVal)) {
    setError(Name, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(NameVal)){
    setError(Name,'space and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(Name)
  }

  // if (RepositoryVal === '') {
  //   setError(Repository, 'Ami ID is Invalid');
  //   allConditionsTrue = false ;
  // }
  // else if (!FirstLetter.test(RepositoryVal)) {
  //   setError(Repository, 'First Letter must start with small Letter');
  //   allConditionsTrue = false ;
  // }
  // else if(validate(RepositoryVal)){
  //   setError(Repository,'space,number and symbol not valid');
  //   allConditionsTrue = false ;
  // }
  // else {
  //   setSuccess(Repository)
  // }
  
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
      /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~]/
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















