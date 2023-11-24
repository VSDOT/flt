// form validation

const form = document.querySelector('#form');
const eCSName = document.querySelector('#ECSName');
const namePrifix = document.querySelector('#NamePrifix');
const imageId = document.querySelector('#ImageId');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs() {
  const eCSNameVal = eCSName.value.trim()
  const namePrifixVal = namePrifix.value.trim()
  const imageIdVal = imageId.value.trim()
  allConditionsTrue = true ;


  if (eCSNameVal === '') {
    setError(eCSName, 'ECS Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(eCSNameVal)) {
    setError(eCSName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(eCSNameVal)){
    setError(eCSName,'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(eCSName)
  }

  if (namePrifixVal === '') {
    setError(namePrifix, 'Name Prefix is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(namePrifixVal)) {
    setError(namePrifix, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(namePrifixVal)){
    setError(namePrifix,'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(namePrifix)
  }

  if (imageIdVal === '') {
    setError(imageId, 'Image ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(imageIdVal)) {
    setError(imageId, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(imageIdVal)){
    setError(imageId,'space and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(imageId)
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


const validate = (text) => {
  return String(text)
    .toLowerCase()
    .match(
      /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~]/
    );
};

const FirstLetter = /^[ a-z]/ 















