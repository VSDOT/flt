
// form validation

const form = document.querySelector('#form');
const bucket = document.querySelector('#BUCKET');
const radioButtons = document.querySelectorAll('input[name="acl"]')
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
  const bucketVal = bucket.value.trim()
  allConditionsTrue = true ;




  if (bucketVal === '') {
    setError(bucket, 'Bucket is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(bucketVal)) {
    setError(bucket, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validateEmail(bucketVal)) {
    setError(bucket, 'space and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(bucket)
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
      /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~]/
    );
};

const FirstLetter = /^[ a-z]/