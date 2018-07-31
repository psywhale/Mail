

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
        if (!message.archived){
            // html = html + buildMessage(message, html);
            html = buildMessage(message, html);
         }
    } else {
        //console.log('is');
        // In a label, go ahead and show archived
        //console.log(message.archived);
        html = buildMessage(message, html);
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
    }else{
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
    html = html + "</a>";

    return html;

}
