
    var d = new Date();
    var n = d.getTimezoneOffset();

// {#    ------- THIS IS MAIL (Reply, Compose, View) --------#}
    $('.main-mail-section').css("height", $(document).height());
    $(".mail-content a").attr("target","_blank");

    $( ".reply_editor" ).attr("placeholder", "Click here to Reply...");
    $( ".reply_editor" ).delay(800).click(function() {
        CKEDITOR.replace( 'id_content', {
            on:
                {'instanceReady':function(evt){
                    CKEDITOR.instances.id_content.focus();
                }
                }
        });
        $( ".sendmailbutton" ).show();
    });
    $( ".compose .reply_editor" ).attr("placeholder", "Click here to Compose...");
    $("#id_instructor").prop("selectedIndex", 0);


// {#    ------- THIS IS BUTTONTS & MAIL FUNCTIONS --------#}
    $("#checkAll").click(function () {
        $(".check").prop('checked', $(this).prop('checked'));
    });


// {#    ------- THIS IS FOOTABLES --------#}
    $(function () {
        $('.footable').footable();
        addRowToggle: false
    });

    $(function () {
        $('table').footable();
        $('table').trigger('footable_clear_filter');
        $('.toggle').click(function () {
            $('.toggle').toggle();
            $('table').trigger($(this).data('trigger')).trigger('footable_redraw');
        });
    });



// {#    ------- THIS IS CURRENT TIME CALC --------#}
function calculateCurrentTermCode(){
	var date = new Date();
	var month = date.getMonth() + 1;
	var day = date.getDate();

	if((month >= 1) && (month < 5)){
		var year = date.getYear() - 101;
        var semester = "3s";
     }
	if((month > 5) && (month < 8)){
		var year = date.getYear() - 100;
		var semester = "1s";
	}
	if((month == 5) && (day >= 20)){
		var year = date.getYear() - 100;
		var semester = "1s";
	}
	if((month >= 8) && (month <= 12)){
		var year = date.getYear() - 100;
		var semester = "2s";
	}

	return year+semester;
}


// {#    ------- THIS IS Check all checkboxes --------#}

//  $('#checkall').click(function(){
//      $('input[name=chkbx]').prop("checked", true);
//      $('#checkall').addClass('uncheck-all');
// });
//  $('#checkall:checked').click(function(){
//      $('input[name=chkbx]').prop("checked", false);
//      $('#checkall').removeClass('uncheck-all');
// });
   $("#checkall").change(function(){
     var checked = $(this).is(':checked');
     if(checked){
       $(".checkbox").each(function(){
         $(this).prop("checked",true);
       });
     }else{
       $(".checkbox").each(function(){
         $(this).prop("checked",false);
       });
     }
   });

  $(".checkbox").click(function(){

    if($(".checkbox").length == $(".checkbox:checked").length) {
      $("#checkall").prop("checked", true);
    } else {
      $("#checkall").removeAttr("checked");
    }

  });


