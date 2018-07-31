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