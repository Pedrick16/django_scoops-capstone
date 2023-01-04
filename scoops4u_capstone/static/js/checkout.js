$(document).ready(function(){
 
    $('#option').on('change', function () {
        var select_value = this.value
        if (select_value == "delivery") {
            // $('#pdate').css("display", "block")
         
            $('#h3_date').text('Preferred Delivery date')
            $('#pdate').fadeIn(1000)
            $('#no_specific').fadeIn(1000)
        } else if (select_value == "pickup") {
        
            $('#h3_date').text('Pickup Date')
            $('#pdate').fadeIn(1000)
            $('#no_specific').fadeOut()
            // $('#pdate').css("display", "none")
        } else if (select_value == "") {
            $('#pdate').fadeOut(1000)
            // $('#pdate').css("display", "none")
        }

    })

    $('#input_date').on('click', function () {
        $('#no_specific').fadeToggle(1000)
    })

    $('#checkbox_no_date').on('click', function () {
        $('#date_deliver').fadeToggle(1000)
        $('#input_date').val('')
    })



})