

function displayEmail(response, messageDiv){
    //
    // Json String need to have the following info:
    //      message.id
    //      message.read
    //      message.from
    //      message.from.first_name
    //      message.from.last_name
    //      message.from.username
    //      message.timestamp
    //      message.attachments  [true/false]
    //      message.section
    //      message.subject
    //      message.archived
    //

var html = "";
    // loop through json

    $.each(response.messages, function(index, message){
    //

    if (window.location.pathname.search('label') == -1) {
        //console.log('not');
        // Not in a label, should not show archived messages
        //if (!message.archived){
            // html = html + buildMessage(message, html);
            html = buildMessage(message, html);
        // }
    } else {
        //console.log('is');
        // In a label, go ahead and show archived
        //console.log(message.archived);
        html = buildMessage(message, html);
    }


 });

console.log("-- Checked for new mail --");




if (response.pages > 0){

var pagination = '<ul class=\"pagination\">';

    if (response.has_previous == false) {
        pagination += 
	    '<li class="has_previous disabled"><span class="fas fa-step-backward"></span></a></li>'
	    + '<li class="has_first disabled"><span class="fas fa-caret-left"></span></a></li>';
    }
    else {
        pagination += 
	    '<li class="has_previous"><a href="?num_per_page='+ response.num_per_page +'&page=1"><span class="fas fa-fast-backward"></span></a></li>'
	    + '<li class="has_first"><a href="?num_per_page='+ response.num_per_page +'&page='+ response.previous_page_number +'"><span class="fas fa-step-backward"></span></a></li>';
    }
/*
    foo = 1;
    while(foo <= response.last_page){
	if (response.page_num == foo){
        	pagination += '<li class="active" title="Current Page"><span>'+ foo +' <span class="sr-only">(current)</span></span></li>';
	}
	else {
		pagination += '<li><a href="?num_per_page='+ response.num_per_page +'&page='+ foo +'">'+ foo +'</a></li>';
	}
	foo++;
    }
*/
    pagination += '<li title="Enter a page number and press the Enter Key."><span class=pag-txt>Page</span> <span class=pag-txt style="padding:6px 0px !important"><input type=text id="pagination-input" placeholder="' + response.page_num + '" /></span> <span class=pag-txt> of ' + response.last_page + '</span></li>';

    if (response.has_next == false) {
        pagination += 
	    	'<li class="has_next disabled"><span class="fas fa-step-forward"></span></li>'
	        + '<li class="has_last disabled"><span class="fas fa-fast-forward"></span></li>';
    }
    else {
        pagination += 
	     '<li class="has_next"><a href="?num_per_page='+ response.num_per_page +'&page='+ response.next_page_number +'"><span class="fas fa-step-forward"></span></a></li>'
	     + '<li class="has_last"><a href="?num_per_page='+ response.num_per_page +'&page='+ response.last_page +'"><span class="fas fa-fast-forward"></span></a></li>';
    }

pagination += '</ul>';
pagination += '<div id="pagination-error" style="display:none">Please enter a number between 1 and '+ response.last_page +'.</div>';

	$('#email-pagination').html(pagination);
}

$("#pagination-input").keypress(function(event) {
    if (event.which == 13) {
        event.preventDefault();
	if ($("#pagination-input").val() > response.last_page | $("#pagination-input").val() == 0){
		$('#pagination-error').show();
	}
	else {
		window.location.href = '?num_per_page='+ response.num_per_page +'&page='+ $("#pagination-input").val();
		$('#pagination-error').hide();
	}
    }
});	



messageDiv.html(html);
colorize();
}

function buildMessage(message, html){

    var label = "00000-000S";
    if (window.location.pathname.search('label') >= 1) {
        label = window.location.pathname.split('/')[2];
    }
    html = html + ' <a href="/reply/'+ message.id +'/' + message.userid + '/' + label + '/" class="list-group-item message-ID-'+ message.id;
    if (message.read){
        html = html + ' read"';
    }
    else {
        html = html + ' unread-mail"';
    }
    html = html + 'title="ID: '+ message.id +' -- COURSE #: ' + message.section +' --  SUBJECT: '+ message.subject +'.">';
	if (message.read){
	    html = html + '<div class="micons read-ICON far fa-envelope-open" title="Mail has been READ."></div>';
        }
        else {
            html = html + '<div class="micons unread-ICON fas fa-envelope" title="Mail is UNREAD."></div>';
        }
        html = html + '<span class="name">';
    if((message.from.first_name == "") || (message.from.last_name == "")){
        html = html + message.from.username;
    }
    else {
        html = html + message.from.first_name.charAt(0).toUpperCase() + message.from.first_name.substr(1,message.from.first_name.length) + " " + message.from.last_name.charAt(0).toUpperCase() + message.from.last_name.substr(1,message.from.last_name.length);
    }
    var sections = window.location.pathname.split("/");
    if (sections[1] == "label"){
        if (message.archived){
	    html = html + '</span><span class="section s'+ message.section +'">'+ message.section +'</span>';
	}else {
	    html = html + '</span><span class="section s'+ message.section +' section-inbox"><strong>Inbox</strong></span>';
	}
    }
    else {
	html = html + '</span><span class="section s'+ message.section +'">'+ message.section +'</span>';
    }
    html = html + '   <span class="subject text-muted"> &nbsp; ';
    if (message.subject){
        html = html + message.subject;
    }
    else {
        html = html + '(no subject)';
    }
    html = html + '</span>\n' +
        '\n' +
        '<span class="date badge justthedateplease">'+ message.timestamp +'</span>';
    if (message.attachments) {
        html = html + '<span class="pull-right"><span class="fas fa-paperclip" title="This message has an Attachement!"></span></span>';
    }
    html = html + '</a>';


/*
  // PAGINATION
  html = html + '<div class="email_pagination" style="text-align: center; margin-top: -25px;">';
  if (message.pages > 1){
    html = html + '<ul class="pagination">';
    if (message.has_previous == "true"){
      html = html + '<li><a href="' + message.previous_page_number + '?perpage=' + message.num_per_page + '">&laquo;</a></li>';
    }
    else {
      html = html + '<li class="disabled"><span>&laquo;</span></li>';
    }
    for (var i in message) {
      if (i.page_num == i){
        html = html + '<li class="active" title="Current Page"><span>{{ i }} <span class="sr-only">(current)</span></span></li>';
      }
      else {
	html = html + '<li><a href="' + i +'?perpage=' + message.num_per_page + '">' + i + '</a></li>';
      }
    }
    
    if (message.has_next == "true"){
      html = html + '<li><a href="' + message.next_page_number + '?perpage=' + message.num_per_page + '">&laquo;</a></li>';
    }
    else {
      html = html + '<li class="disabled"><span>&laquo;</span></li>';
    }
    html = html + '</div><!--/end email_pagination -->';
  }
console.log('________________');
console.log(message.pages);
console.log('________________');
*/
    return html;

}

