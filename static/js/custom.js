
    var d = new Date();
    var n = d.getTimezoneOffset();




// {#    ------- THIS IS BUTTONTS & MAIL FUNCTIONS --------#}
    $("#checkAll").click(function () {
        $(".check").prop('checked', $(this).prop('checked'));
    });


// {#    ------- THIS IS FOOTABLES --------#}
//     $(function () {
//         $('.footable').footable();
//         addRowToggle: false
//     });
//
//     $(function () {
//         $('table').footable();
//         $('table').trigger('footable_clear_filter');
//         $('.toggle').click(function () {
//             $('.toggle').toggle();
//             $('table').trigger($(this).data('trigger')).trigger('footable_redraw');
//         });
//     });



// {#    ------- THIS IS CURRENT TERMCODE --------#}
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

function getCourses(){
    $.ajax({
        url: 'https://moodle.wosc.edu/wosc/rest.php',
        data: {rest_key: 'HkHO25shu0i3Tq24iCknrB1mnpOY', action: 'get_my_courses'},
        jsonp: 'callback',
        dataType: 'jsonp',
        success: function (response) {
            jQuery.each(response, function (id, course) {
                $('#all-courses').html($('#all-courses').html() + course.fullname);
                var termCode = calculateCurrentTermCode();
                var info = course.shortname.split("-");
                try {
                    myTC = info[1];
                    if (termCode == info[1].toLowerCase()) {
                        $('#current-courses').html($('#current-courses').html() + '<li class="current-course-list ' + course.shortname + '" id="' + course.shortname + '" title="' + course.fullname + '"><a href="/label/' + course.shortname + '/"> ' + course.fullname + '</a></li>');
                    }
                    else {
                        $('#past-course-dropdown').show();
                        $('#past-courses').html($('#past-courses').html() + '<li class="past-course-list"><a href="/label/' + course.shortname + '/"> ' + course.fullname + '</a></li>');
                        $('#past-courses-compose').html($('#past-courses-compose').html() + '<li class="past-course-compose-list"><a href="/compose/' + course.shortname + '/"> ' + course.fullname + '</a></li>');
                    }
                    var colors = ['red', 'green', 'blue', 'yellow'];
                    var sectionNum = course.shortname;
                }
                catch (e) {
                }
            });
            getUnreadBadges();
            addActiveCourse();
        }
    });
}
