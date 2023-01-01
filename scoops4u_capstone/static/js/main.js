//pos sale
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

// alert("pogi ko")

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


// if (select.value == "pickup") {
//    show.style.display = 'block'
// }
// // alert('invalid payment')