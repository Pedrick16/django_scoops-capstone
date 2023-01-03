// pos sale
function BtnCompute(){
    const TotalAmount = document.querySelector('#total_amount').value
    const cash = document.querySelector('#cash').value
    const msg = document.querySelector('#msg')


    const change =  parseInt(cash) - parseInt(TotalAmount)
    if( TotalAmount.value > cash.value ){
       msg.style.color = "red"
       msg.innerHTML = "<p class='error'>invalid payment</p>"
       setTimeout(() => document.querySelector('.error').remove(),3000)
        //   alert('invalid payment')
    }else{
        document.querySelector('#change').value = change
    }
}



// displaying preffered date

function handleChange(selectElement) {
    const show = document.querySelector('#pdate')
    if (selectElement.value === "delivery") {
        show.style.display = 'block'
    } else if(selectElement.value === "pickup") {
        show.style.display = 'none'
    } else if(selectElement.value === "") {
        show.style.display = 'none'
    } 
  }



// const file = document.querySelector('#file')

// file.style.background = "blue"   





