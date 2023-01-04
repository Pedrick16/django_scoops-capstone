$(document).ready(function(){
    $('#btn_compute').on('click', function () {
        var total_amount = parseInt($('#total_amount').val())
        var cash = parseInt($('#cash').val())
        var result =  cash - total_amount
        var msg = $('#msg')

        if(cash >= total_amount){
            $('#change').val(result)


        }else{
            $('#msg').css("color", "red")
            // $('#msg').css("fontSize", "20px")
            $('#msg').css("display", "block")
            msg.html('<i class="msg">Invalid Payment<i/>')
            setTimeout(function (){
                $('.msg').remove()
            },3000)
        }
        
    })
    
 

})





