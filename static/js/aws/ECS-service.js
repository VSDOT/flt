// form validation

const form = document.querySelector('#form');
const ClusterName = document.querySelector('#clusterName');
const Family = document.querySelector('#family');
const svc_name = document.querySelector('#Name');
const CounterName = document.querySelector('#counterName');
const subnet = document.querySelector('#Subnet');
const SecurityGroups = document.querySelector('#securityGroups');
const radioButtons = document.querySelectorAll('input[name="essential"]')
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
  const nameval = svc_name.value.trim()
  const ClusterNameVal = ClusterName.value.trim()
  const FamilyVal = Family.value.trim()
  const CounterNameVal = CounterName.value.trim()
  const subnetVal = subnet.value.trim()
  const SecurityGroupsVal = SecurityGroups.value.trim()
  allConditionsTrue = true ;


  if (nameval === '') {
    setError(svc_name, 'Name is Invalid');
    allConditionsTrue = false ;
  }
  else if(validateEmail(nameval)){
    setError(svc_name,'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(svc_name)
  }

  if (ClusterNameVal === '') {
    setError(ClusterName, 'Cluster Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(ClusterNameVal)) {
    setError(ClusterName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(ClusterNameVal)){
    setError(ClusterName,'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(ClusterName)
  }

  if (FamilyVal === '') {
    setError(Family, 'Family is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(FamilyVal)) {
    setError(Family, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(FamilyVal)){
    setError(Family,'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(Family)
  }

  if (CounterNameVal === '') {
    setError(CounterName, 'Counter Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(CounterNameVal)) {
    setError(CounterName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(CounterNameVal)){
    setError(CounterName,'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(CounterName)
  }

  if (subnetVal === '') {
    setError(subnet, 'Subnet ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(subnetVal)) {
    setError(subnet, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(subnetVal)){
    setError(subnet,'space and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(subnet)
  }

  if (SecurityGroupsVal === '') {
    setError(SecurityGroups, 'Security Group is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(SecurityGroupsVal)) {
    setError(SecurityGroups, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(SecurityGroupsVal)){
    setError(SecurityGroups,'space and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(SecurityGroups)
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
