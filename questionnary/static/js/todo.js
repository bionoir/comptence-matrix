$(document).ready(
    function(){
        $("#answer_text").change(function() {
            if ($('#answer_text option:selected').text() == 'Other...') {
                jQuery('.otherchoice').show();
            } else {
                jQuery('.otherchoice').hide();
            }
        });

        $('.selectpicker').selectpicker();
    }
);