
// form validation

const form = document.querySelector('#form');
const ClusterName = document.querySelector('#clusterName');
const SubnetID = document.querySelector('#subnetID');
const SecurityGroup = document.querySelector('#securityGroup');
const NodeGroup = document.querySelector('#nodeGroup');
const DesiredCapacity = document.querySelector('#desiredCapacity');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  validateInputs();
  validate();
})

function validateInputs() {
  const ClusterNameVal = ClusterName.value.trim()
  const SubnetIDVal = SubnetID.value.trim()
  const SecurityGroupVal = SecurityGroup.value.trim()
  const NodeGroupVal = NodeGroup.value.trim()
  const DesiredCapacityVal = DesiredCapacity.value.trim()
  allConditionsTrue = true ;


  if (ClusterNameVal === '') {
    setError(ClusterName, 'Cluster Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(ClusterNameVal)) {
    setError(ClusterName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validateEmail(ClusterNameVal)) {
    setError(ClusterName, 'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(ClusterName)
  }

  if (SubnetIDVal === '') {
    setError(SubnetID, 'Subnet ID is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(SubnetIDVal)) {
    setError(SubnetID, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validate(SubnetIDVal)) {
    setError(SubnetID, 'space and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(SubnetID)
  }

  if (SecurityGroupVal === '') {
    setError(SecurityGroup, 'Security Group is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(SecurityGroupVal)) {
    setError(SecurityGroup, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validate(SecurityGroupVal)) {
    setError(SecurityGroup, 'space and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(SecurityGroup)
  }

  if (NodeGroupVal === '') {
    setError(NodeGroup, 'Node Group is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(NodeGroupVal)) {
    setError(NodeGroup, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if (validateEmail(NodeGroupVal)) {
    setError(NodeGroup, 'space,number and symbol not valid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(NodeGroup)
  }

  if (DesiredCapacityVal === '') {
    setError(DesiredCapacity, 'Desired Capacity is Invalid');
    allConditionsTrue = false ;
  }
  else {
    setSuccess(DesiredCapacity)
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

// const validateEmail = (text) => {
//   return String(text)
//   .toLowerCase()
//   .match(
//     /[ 1234567890]/
//   );
// };

const validate = (text) => {
  return String(text)
    .toLowerCase()
    .match(
      /[ `!@#$%^&*()+\=\[\]{};':"\\|,.<>\/?~]/
    );
};

const FirstLetter = /^[ a-z]/