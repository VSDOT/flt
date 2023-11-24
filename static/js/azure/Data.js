// form validation

const form = document.querySelector('#form');
const Resourcegroup = document.querySelector('#resourcegroup');
const DataFactory = document.querySelector('#dataFactory');
const Repository = document.querySelector('#repository');
const BranchName = document.querySelector('#branchName');
const rootfolder = document.querySelector('#Rootfolder');
const AccessToken = document.querySelector('#accessToken');

form.addEventListener('submit',(e)=>{
  e.preventDefault();
  validateInputs();
  validate();
  Number();
  accessToken();
  symbol();
})

function validateInputs(){
  const resourcegroupVal = Resourcegroup.value.trim()
  const DataFactoryVal = DataFactory.value.trim()
  const RepositoryVal = Repository.value.trim()
  const BranchNameVal = BranchName.value.trim()
  const rootfolderVal = rootfolder.value.trim()
  const AccessTokenVal = AccessToken.value.trim()
  allConditionsTrue = true ;

  if(resourcegroupVal === ''){
    setError(Resourcegroup,'ResourceGroup ID is Invalid');
    allConditionsTrue = false ;
  }
  else if(symbol(resourcegroupVal)){
    setError(Resourcegroup,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Resourcegroup)
  }
  
  if(DataFactoryVal === ''){
    setError(DataFactory,'DataFactory Name is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(DataFactoryVal)) {
    setError(DataFactory, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validateEmail(DataFactoryVal)){
    setError(DataFactory,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else if (DataFactoryVal.match(/[A-Z]/)){
    setError(DataFactory,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(DataFactory)
  }

  if(RepositoryVal === ''){
    setError(Repository,'Repository Url is Invalid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(Repository)
  }

  if(BranchNameVal === ''){
    setError(BranchName,'BranchName is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(BranchNameVal)) {
    setError(BranchName, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(validate(BranchNameVal)){
    setError(BranchName,'space,number and symbols dose not valid');
    allConditionsTrue = false ;
  }
  else if (BranchNameVal.match(/[A-Z]/)){
    setError(BranchName,'capital Letter not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(BranchName)
  }

  if(rootfolderVal === ''){
    setError(rootfolder,'Root Folder Path is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(rootfolderVal)) {
    setError(rootfolder, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(Number(rootfolderVal)){
    setError(rootfolder,'space,number and symbols dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(rootfolder)
  }

  if(AccessTokenVal === ''){
    setError(AccessToken,'Access Token Key is Invalid');
    allConditionsTrue = false ;
  }
  else if (!FirstLetter.test(AccessTokenVal)) {
    setError(AccessToken, 'First Letter must start with small Letter');
    allConditionsTrue = false ;
  }
  else if(accessToken(AccessTokenVal)){
    setError(AccessToken,'space and number dose not valid');
    allConditionsTrue = false ;
  }
  else{
    setSuccess(AccessToken)
  }
  

  if(allConditionsTrue){
    form.submit()
  }
  
}

function setError(element,message){
  const inputGroup = element.parentElement;
  const errorElement = inputGroup.querySelector('.error')

  errorElement.innerText = message ;
  inputGroup.classList.add('error')
  inputGroup.classList.remove('success')

}

function setSuccess(element){
  const inputGroup = element.parentElement;
  const errorElement = inputGroup.querySelector('.error')

  errorElement.innerText = '' ;
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
    /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~1234567890]/
  );
};

const Number = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\?~1234567890]/
  );
};

const accessToken = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\?~]/
  );
};

const symbol = (text) => {
  return String(text)
  .toLowerCase()
  .match(
    /[ `!@#$%^&*()+\_=\[\]{};':"\\|,.<>\/?~]/
  );
};
const FirstLetter = /^[ a-z]/