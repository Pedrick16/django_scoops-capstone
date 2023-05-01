
$(document).ready(function(){
    // var form = $('#form')
    // form.on('submit', function (e) {
    //     e.preventDefault();

       
    // })



    $('#btn_compute').on('click', function (e) {
        e.preventDefault();
        var total_amount = parseInt($('#total_amount').val())
        var cash = parseInt($('#cash').val())

        var result =  cash - total_amount
;
        // var formattedNumber = new result.toLocaleString('en-PH', options);
        var currency = parseFloat(result).toLocaleString('en-PH', { style: 'currency', currency: 'PHP' });
        var msg = $('#msg')
        var pos_id = $('#pos_id').val()


      


        if(cash >= total_amount){
            $('#get_id').val(pos_id)
            $('#vchange').val(currency)
            $('#change').val(result)
            $('#btn-receipt').show()
          
            
            // $('#form').submit()


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

    $('#btn-receipt').on('click', function(e){
        e.preventDefault()
        var cash = $('#cash').val()
        // var change = $('#change').val()
        
        if(cash == "" ){
            alert('all field required')
        }else if(cash.length > 12){
            alert('invalid cash')
        }else{
            $('#form').submit()
        }


    })

 
    $('#return').change(function() {
        var defaultCash = 0
        var sumAmount= $('#sum_amount').val()
        if(this.checked) {
            $('#total_amount').val(0)
            $('#cash').val(defaultCash)
            $('#vchange').val("0.00")
            $('#change').val(0)
            $('#btn-receipt').show()
            $('#btn_compute').hide(1000)
          
        } else {
            $('#total_amount').val(sumAmount)
            $('#btn-receipt').fadeOut(1000)
            $('#btn_compute').show()
            $('#cash').val("")
            $('#vchange').val("")

            
        }

        // if($(this).is(':checked')) {
        //     $('#cash').val(defaultCash)
        //     $('#btn-receipt').fadeIn(1000)
            
        // } else {
        //     $('#cash').val("")
        //     $('#btn-receipt').fadeOut(1000)
        // }
    });

  

    

   




})





