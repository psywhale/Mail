

function displayEmail(messages, messageDiv){
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

    $.each(messages, function(index, message){
    //

    if (window.location.pathname.search('label') == -1) {
        console.log('not');
        // Not in a label, should not show archived messages
        if (!message.archived){
            // html = html + buildMessage(message, html);
            html = buildMessage(message, html);
         }
    } else {
        console.log('is');
        // In a label, go ahead and show archived
        console.log(message.archived);
        html = buildMessage(message, html);
    }

 });

messageDiv.html(html);

}

function buildMessage(message, html){
    var label = "home";
    if (window.location.pathname.search('label') >= 1) {
        label = window.location.pathname.split('/')[2];
    }
    }
    html = html + ' <a href="/reply/'+ message.id +'/' + message.userid + '/' + label + /" class="list-group-item message-ID-'+ message.id;
    if (message.read){
        html = html + ' read"';
    }
    else {
        html = html + ' unread-mail"';
    }
    html = html + 'title="MAIL FROM: ' + message.from.first_name + " " + message.from.last_name + 'in ' + message.section +'. SUBJECT: '+ message.subject +'.">';
    if (mail.archive){
        html = html + '<div class="micons archive-ICON glyphicon glyphicon-save-file" title="Mail is ARCHIVED to the course label."></div>';
    }
    else if (message.threaded){
	html = html + '<div class="micons threaded-ICON glyphicon glyphicon-tags" title="Mail has multiple conversations (THREADED)"></div>';
	}
    else if (message.read){
	html = html + '<div class="micons read-ICON glyphicon glyphicon-save" title="Mail has been READ."></div>';
	}
    else {
        html = html + '<div class="micons unread-ICON glyphicon glyphicon-tag" title="Mail is UNREAD."></div>';
    }
        html = html + '<span class="name">';
    if((message.from.first_name == "") || (message.from.last_name == "")){
        html = html + message.from.username;
    }
    else {
        html = html + message.from.first_name.charAt(0).toUpperCase() + message.from.first_name.substr(1,message.from.first_name.length) + " " + message.from.last_name.charAt(0).toUpperCase() + message.from.last_name.substr(1,message.from.last_name.length);
    }
    html = html + '</span><span class="section s'+ message.section +'">'+ message.section +'</span>';
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
        html = html + '<span class="glyphicon glyphicon-paperclip" title="This message has an Attachement!"></span>';
    }
    html = html + "</a>";

    return html;

}
