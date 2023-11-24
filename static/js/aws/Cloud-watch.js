
  // form validation

  const form = document.querySelector('#form');
  const alarmName = document.querySelector('#AlarmName');
  const evaluationPeriod = document.querySelector('#EvaluationPeriod');
  const metricName = document.querySelector('#MetricName');
  const threshold = document.querySelector('#Threshold');
  const period = document.querySelector('#Period');
  
  form.addEventListener('submit',(e)=>{
    e.preventDefault();
    validateInputs();
    validate();
  })
  
  function validateInputs(){
    const alarmNameVal = alarmName.value.trim()
    const evaluationPeriodVal = evaluationPeriod.value.trim()
    const metricNameVal = metricName.value.trim()
    const thresholdVal = threshold.value.trim()
    const periodVal = period.value.trim()
    allConditionsTrue = true ;
  
  
    if(alarmNameVal === ''){
      setError(alarmName,'AlarmName is Invalid')
      allConditionsTrue = true ;
    }
    else if (validate(alarmNameVal)) {
      setError(alarmName, 'space,symbol and number dose not valid')
      allConditionsTrue = true ;
    }
    else{
      setSuccess(alarmName)
    }
    
    if(evaluationPeriodVal === ''){
      setError(evaluationPeriod,'Evaluation Period is Invalid')
      allConditionsTrue = true ;
    }
    else{
      setSuccess(evaluationPeriod)
    }
    if(metricNameVal === ''){
        setError(metricName,'Metric Name is Invalid')
        allConditionsTrue = true ;
      }
      else if (validate(metricNameVal)) {
        setError(metricName, 'space,symbol and number dose not valid')
        allConditionsTrue = true ;
      }
      else{
        setSuccess(metricName)
      }
    
    if(thresholdVal === ''){
      setError(threshold,'Threshold is Invalid')
      allConditionsTrue = true ;
    }
    else{
      setSuccess(threshold)
    }
    if(periodVal === ''){
        setError(period,'Period is Invalid')
        allConditionsTrue = true ;
      }
      else{
        setSuccess(period)
      }
    
    if( allConditionsTrue ){
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