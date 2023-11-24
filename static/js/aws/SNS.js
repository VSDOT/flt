
// form validation

const form = document.querySelector('#form');
const NAme = document.querySelector('#name');
const TopicArn = document.querySelector('#topicArn');
const EndPoint = document.querySelector('#endPoint');
const radioButtons = document.querySelectorAll('input[name="fifo"]')
const radioselects = document.querySelectorAll('input[name="content"]')
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

form.addEventListener('submit', (e) => {
  e.preventDefault();
  validateInputs();
})

function validateInputs() {
  const NAmeVal = NAme.value.trim()
  const TopicArnVal = TopicArn.value.trim()
  const EndPointVal = EndPoint.value.trim()
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
    setError(NAme, 'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(NAme)
  }

  if (TopicArnVal === '') {
    setError(TopicArn, 'Topic Arn is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(TopicArnVal)) {
    setError(TopicArn, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validateEmail(TopicArnVal)) {
    setError(TopicArn, 'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(TopicArn)
  }

  if (EndPointVal === '') {
    setError(EndPoint, 'EndPoint is Invalid');
    allConditionsTrue = false ;
  }
   else if (!FirstLetter.test(EndPointVal)) {
    setError(EndPoint, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(EndPoint)
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