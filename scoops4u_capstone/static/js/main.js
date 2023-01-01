function BtnCompute(){
    const TotalAmount = document.querySelector('#total_amount').value
    const cash = document.querySelector('#cash').value
   


    const change =  parseInt(cash) - parseInt(TotalAmount)
    if( TotalAmount > cash ) {
        alert('invalid payment')
    }else{
        document.querySelector('#change').value = change
    }
}
