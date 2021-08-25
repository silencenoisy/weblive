document.write("<script type='text/javascript' src='../static/js/ajaxPost.js'></script>");

$(function () {
   var ret=ajaxGET(api_url+"/room_all_type")

    if(!isEmpty(ret)){
        var data = ret['data'];
        var parent = $("#js-game-list");
        for(var i in data){
            var temp = typeHtml(data[i]);
            parent.append(temp);
        }
    }
});

function typeHtml(data) {
    return "<li class=\"g-gameCard-item\" title=\""+data['name']+"\">\n" +
        "        <a class=\"g-gameCard-link\" href=\"/g/"+data['mname']+"\" target=\"_blank\">\n" +
        "        <img class=\"g-gameCard-img\" src=\"../static/img/"+data['avarter']+"\" alt=\""+data['name']+"\" data-default-img=\"84x84\">\n" +
        "        <p class=\"g-gameCard-fullName\">"+data['name']+"</p>\n" +
        "    </a>\n" +
        "    </li>"
}