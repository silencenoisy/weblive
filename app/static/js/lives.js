document.write("<script type='text/javascript' src='../static/js/ajaxPost.js'></script>");

$(function () {
    var params = {
      "type_name":GetTypeName(location.href),
        "page":$("#page-data").attr("page-data"),
        "per_page":20,
    };
   var ret=ajaxPost(params,api_url+"/livers");

    if(!isEmpty(ret)){
        var data = ret['data'];
        var parent = $("#js-live-list");
        parent.empty();
        console.log(data);
        for(var i in data){
            var temp = typeHtml(data[i]);
            parent.append(temp);
        }
        LiverPageSet(ret['total']);
    }
});

function typeHtml(data) {
    var face = data['cover'];
    alert(face)
    if(isEmpty(face)){
        face = "default.png";
    }
    return "<li class=\"game-live-item\">\n" +
        "            <a href=\""+"/live/"+data['room_name']+"\" class=\"video-info \" target=\"_blank\">\n" +
        "                <img class=\"pic\"\n" +
        "                     src=\"../static/img/"+face+"\"\n" +
        "                     data-default-img=\"338x190\" alt=\""+data['liver']+"的直播\" title=\""+data['liver']+"的直播\">\n" +
        "\n" +
        "                <em class=\"tag tag-recommend\">推荐</em>\n" +
        "\n" +
        "                <i class=\"btn-link__hover_i\"></i>\n" +
        "            </a>\n" +
        "            <a href=\"/live/"+data['room_name']+"\" class=\"title\" title=\""+data['title']+"\" target=\"_blank\">"+data['title']+"</a>\n" +
        "            <span class=\"txt\">\n" +
        "        <span class=\"avatar fl\">\n" +
        "            <i class=\"nick\" title=\""+data['liver']+"\">"+data['liver']+"</i>\n" +
        "        </span>\n" +
        "    </span>"
}

function GetTypeName(url) {
    var arr1 = url.split("/");
    var arr2 = arr1[arr1.length-1].split("?");
    var arr3 = arr2[0].split("#");
    var str = arr3[0];
    // console.log(arr2+" "+arr3+" "+str);
    return str;
}

function LiverPageSet(total) {

}