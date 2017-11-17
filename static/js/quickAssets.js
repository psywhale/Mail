

        // bind change event to select
        $('#dynamic_select').on('change', function () {
          var url = $(this).val(); // get selected value
          if (url) { // require a URL
              window.location = url; // redirect
          }
          return false;
        });

        //var quickTextLength = $('.msg_container').text().length;
        //$('#textarea_feedback').html(quickTextLength + ' Characters');
        $('#id_auth_code').attr("placeholder", "Authorization Code");
        $('#id_reason').attr("placeholder", "Reason");
        $("#id_close_time").attr("placeholder", "Time");
        $("#id_close_time").attr("autocomplete", "off");

        var text_max = 109;
        $('#textarea_feedback').html(text_max + ' characters remaining');

        $('#id_message').keyup(function() {
            var text_length = $('#id_message').val().length;
            var text_remaining = text_max - text_length;
            var text = $('#id_message').val();
            $('.previewTextGeneric').html(text);

            $('#textarea_feedback').html(text_remaining + ' characters remaining');
        });
        $('#id_close_time').keyup(function() {
            // var text_length = $('.totalmessage').length;
            // var text_remaining = text_max - text_length;
            var text = $('#id_close_time').val();
            $('.previewTextTime').html(text);

            // $('.totalmessagecount').html(text_length + ' characters remaining');
        });
        $('#id_reason').change(function() {
            // var text_length = $('.totalmessage').val().length;
            // var text_remaining = text_max - text_length;
            var text = $('#id_reason').val();
            $('.previewTextReason').html(text);

            // $('.totalmessagecount').html(text_remaining + ' characters remaining');
        });
