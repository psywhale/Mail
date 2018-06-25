

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
    html = html + ' <a href="/reply/'+ message.id +'/' + message.userid + '/" class="list-group-item message-ID-'+ message.id;
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
        html = html + message.from.first_name.charAt(0).toUpperCase() + message.from.first_name.substr(1,message.from.first_name.length) + " " + message.from.last_name.charAt(0).toUpperCase() + message.from.last_name.substr(1,message.from.last_name.length);
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

colorize();
}

function colorize(){
// colorizes section labels
        var thing = document.getElementsByClassName("section");

        var x = 0;
        for (x = 0; x < thing.length; x++) {
            var color = "0"+thing[x].innerHTML;
            var colorArray = [];
            // adding a 0x to string then parseInt turns it into hex
            colorArray[0] = parseInt("0x"+color.substr(0,2));
            colorArray[1] = parseInt("0x"+color.substr(2,2));
            colorArray[2] = parseInt("0x"+color.substr(4,2));

            var newcolorArray = rando(colorArray);
            //console.log("color: " + " "+colorArray[0]+" "+ colorArray[1] +" "+ colorArray[2]);
           // console.log("newcolor: " +newcolorArray[0]+" "+ newcolorArray[1] +" "+ newcolorArray[2]);
            thing[x].style.background = "rgb("+newcolorArray[0]+","+ newcolorArray[1] +","+ newcolorArray[2]+")";
            thing[x].style.color = "white";
        }
}
function rando(array) {
        var da = array;
        //console.log("da is a "+ typeof da + " contents of "+ da + " length of "+da.length);
        var l = 0;
        var last = array.pop();
        var da = array.push(last);
        for(l = 0; l < array.length; l++) {
           // console.log("l is:"+l+" a[l] is " + array[l]);

            var y = array[l];
            if (y <= 10) { array[l] = y + last;}
            if (y >= 180) { array[l] = y - last*2;}
            var x = array[l] % 3;
            if (x = 0) {
          //      console.log("reeverse");
                var pop = array.shift();
                da = array.push(pop);
                da = array.reverse();
                break;

            }


        }
        return array;
}
