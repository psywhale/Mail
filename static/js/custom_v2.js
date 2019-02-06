

// {#    ------- THIS IS BUTTONTS & MAIL FUNCTIONS --------#}
//    $("#checkAll").click(function () {
//        $(".check").prop('checked', $(this).prop('checked'));
//    });


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

	if(month == 5){
	    if  (day >= 20){
		    var year = date.getYear() - 100;
		    var semester = "1s";
	    }
	    else {
	        var year = date.getYear() - 101;
	        var semester = "3s";
        }
    }

	if((month >= 8) && (month <= 12)){
		var year = date.getYear() - 100;
		var semester = "2s";
	}
    console.log(year.toString()+semester.toString());
	return year+semester;

}


// {#    ------- THIS IS CURRENT TIME --------#}
function calculateCurrentTime(){
	var date = new Date();
    var offset = date.getTimezoneOffset();

    alert(offset);
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

function getCourses(path){
    $.ajax({
        url: 'https://moodle.wosc.edu/wosc/rest.php',
        data: {rest_key: 'HkHO25shu0i3Tq24iCknrB1mnpOY', action: 'get_my_courses'},
        jsonp: 'callback',
        dataType: 'jsonp',
        success: function (response) {
            console.log("Course List");
            if (response.length != 0){
                jQuery.each(response, function (id, course) {
                $('#all-courses').html($('#all-courses').html() + course.fullname);
                var termCode = calculateCurrentTermCode();
                var info = course.shortname.split("-");
                try {
                    myTC = info[1];
                    if (termCode == info[1].toLowerCase()) {
                        $('#current-courses').html($('#current-courses').html() + '<li class="current-course-list ' + course.shortname + '" id="' + course.shortname + '" title="' + course.fullname + ' (Course ID: ' + course.shortname + ')"><a href="/label/' + course.shortname + '/"> ' + course.fullname + ' (Course ID: ' + course.shortname + ')</a></li>');
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
            }
            else{
                window.location = "https://moodle.wosc.edu/mod/lti/view.php?id=26984&next=" + path;
            }


            getUnreadBadges();
            addActiveCourse();
        }
    });
}



<!-- ##### Refreshing sidebar images ##### -->
var theImages = new Array();

  theImages[0] = '/static/images/mail/1.jpg';
  theImages[1] = '/static/images/mail/2.jpg';
  theImages[2] = '/static/images/mail/3.jpg';
  theImages[3] = '/static/images/mail/4.jpg';
  theImages[4] = '/static/images/mail/5.jpg';
  theImages[5] = '/static/images/mail/6.jpg';
  theImages[6] = '/static/images/mail/7.jpg';
  theImages[7] = '/static/images/mail/8.jpg';
  theImages[8] = '/static/images/mail/9.jpg';
  theImages[9] = '/static/images/mail/10.jpg';
  theImages[10] = '/static/images/mail/11.jpg';

var j = 0;
var p = theImages.length - 1;
var preBuffer = new Array();
for (i = 0; i < p; i++){
   preBuffer[i] = new Image();
   preBuffer[i].src = theImages[i];
}
var whichImage = Math.floor((Math.random()* p) + 1);
  console.log("Image #:" + p);

function showImage(){
document.write('<img style="max-width:98%; border-radius:8px; border: 2px outset #888; width:100%; max-width:300px" alt="No Mail Fun!" class="rotateimages" src="'+theImages[whichImage]+'">');
}
