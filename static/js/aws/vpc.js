
// form validation

const form = document.querySelector('#form');
const NAme = document.querySelector('#name');
const vpcCidr = document.querySelector('#VpcCidr');
const SubnetCidr = document.querySelector('#subnetCidr');
const Routetable = document.querySelector('#routetable');
const IngressCidr = document.querySelector('#ingressCidr');
const UserforCidr = document.querySelector('#userforCidr');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs() {
  const NAmeVal = NAme.value.trim()
  const vpcCidrVal = vpcCidr.value.trim()
  const SubnetCidrVal = SubnetCidr.value.trim()
  const RoutetableVal = Routetable.value.trim()
  const IngressCidrVal = IngressCidr.value.trim()
  const UserforCidrVal = UserforCidr.value.trim()
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

  if (vpcCidrVal === '') {
    setError(vpcCidr, 'Vpc Cidr is Invalid');
    allConditionsTrue = false ;
  }
  else if (validate(vpcCidrVal)) {
    setError(vpcCidr, 'Letters,symbol dose not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(vpcCidr)
  }

  if (SubnetCidrVal === '') {
    setError(SubnetCidr, 'Subnet Cidr is Invalid');
    allConditionsTrue = false ;
  }
  else if (validate(SubnetCidrVal)) {
    setError(SubnetCidr, 'Letters,symbol dose not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(SubnetCidr)
  }

  if (RoutetableVal === '') {
    setError(Routetable, 'Route Table is Invalid');
    allConditionsTrue = false ;
  }
  else if (validate(RoutetableVal)) {
    setError(Routetable, 'Letters,symbol dose not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(Routetable)
  }

  if (IngressCidrVal === '') {
    setError(IngressCidr, 'Ingress Cidr is Invalid');
    allConditionsTrue = false ;
  }
  else if (validate(IngressCidrVal)) {
    setError(IngressCidr, 'Letters,symbol dose not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(IngressCidr)
  }


  if (UserforCidrVal === '') {
    setError(UserforCidr, 'User For Cidr is Invalid');
    allConditionsTrue = false ;
  }
  else if (validate(UserforCidrVal)) {
    setError(UserforCidr, 'Letters,symbol dose not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(UserforCidr)
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
      /[ `!@#$%^&*()+\-=\[\]{};':"\\|,<>\?~abcdefghijklmnopqrstuvwxyz]/
    );
};

const FirstLetter = /^[ a-z]/