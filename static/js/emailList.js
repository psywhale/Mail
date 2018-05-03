

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
    //

var html = "";
    // loop through json
$.each(messages, function(index, message){

    console.log(message.read);
    html = html + ' <a href="/reply/'+ message.id +'/" class="list-group-item message-ID-'+ message.id;
    if (message.read){
        html = html + ' read"';
    }
    else {
        html = html + ' unread-mail"';
    }
    html = html + 'title="MAIL FROM: ' + message.from.first_name + " " + message.from.last_name + 'in ' + message.section +'. SUBJECT: '+ message.subject +'.">';
    html = html + '<div class="checkbox">\n' +
        '<label>\n' +
        '<input type="checkbox" class="check" id="message-id-'+ message.id +'">\n' +
        '</label>\n' +
        '</div>\n' +
        '<span class="name">';
    if((message.from.first_name == "") || (message.from.last_name == "")){
        html = html + message.from.username;
    }
    else {
        html = html + message.from.first_name.charAt(0).toUpperCase() + message.from.first_name.substr(1,message.first_name.length) + " " + message.from.last_name.charAt(0).toUpperCase() + message.from.last_name.substr(1,message.last_name.length);
    }
    html = html + '</span><span class="section s'+ message.section +'">'+ message.section +'</span>';
    html = html + '   <span class="subject text-muted"> &nbsp; '+ message.subject +'</span>\n' +
        '\n' +
        '<span class="date badge justthedateplease">'+ message.timestamp +'</span>';
    if (message.attachments) {
        html = html + '<span class="glyphicon glyphicon-paperclip" title="This message has an Attachement!"></span>';
    }
    html = html + "</a>"

});

    messageDiv.html(html);


}