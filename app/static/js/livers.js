document.write("<script type='text/javascript' src='../static/js/ajaxPost.js'></script>");

function UploadCover() {
    var animateimg = $(".InputCover").val(); //获取上传的图片名 带//
    var imgarr = animateimg.split('\\'); //分割
    var myimg = imgarr[imgarr.length - 1]; //去掉 // 获取图片名
    var houzui = myimg.lastIndexOf('.'); //获取 . 出现的位置
    var ext = myimg.substring(houzui, myimg.length).toUpperCase();  //切割 . 获取文件后缀

    var file = $('#InputCover').get(0).files[0]; //获取上传的文件
    var fileSize = file.size;           //获取上传的文件大小
    var maxSize = 1048576;              //最大1MB
    if (ext != '.PNG' && ext != '.GIF' && ext != '.JPG' && ext != '.JPEG' && ext != '.BMP') {
        parent.layer.msg('文件类型错误,请上传图片类型');
        return false;
    } else if (parseInt(fileSize) >= parseInt(maxSize)) {
        parent.layer.msg('上传的文件不能超过1MB');
        return false;
    } else {
        var data = new FormData();
        //获取文件内容
        data.append('images', $('#InputCover')[0].files[0]);
        var ret = ajaxPostLoginedFile(data,api_url+"/changeCover");
        if(!isEmpty(ret)){
           document.getElementById('live_cover_pic').src = "../"+ret["data"]['url'];
            return true
        }
        return false;
    }
}


function ClickInputCover() {
    return $("#InputCover").click();

}


$(function () {

    var typelst = $("#live-type-input");
    var types = ajaxGET(api_url+"/room_all_type");
    if(!isEmpty(types)){
        var type_data = types['data'];
        for(var i in type_data){
            typelst.append("<option value=\""+type_data[i]['id']+"\">"+type_data[i]['name']+"</option>");
        }
    }

   var usr_data = ajaxPostLogined({},api_url+"/liver");
   if(!isEmpty(usr_data)){
       var data = usr_data['data'];
       var cover = data['cover'];
       if(isEmpty(cover)){
           cover = "default.png";
       }
       $(".live-cover").attr("src","../static/img/"+cover);
       $(".live-title-show").html(data['title']);
       $(".live-roomname-show").html("/live/"+data['liver']);
       var opt = $("#live-type-input").find('option');
       opt[data['type_id']-1].selected=true;

   }
   MyLiveRoom();

});


function ChangeCover() {
    var params = {
        "url": document.getElementById('live_cover_pic').src
    };

    var ret = ajaxPostLogined(params,api_url+"/changeCovered");
    if(!isEmpty(ret)){
        window.location.reload();
    }
}

function MyLiveRoom() {
    var roomname = $("#live-roomname-show").html();
    if(!isEmpty(roomname)){
        $("#jump-btn-live-room").attr('href',roomname);
    }


}


function FetchKey() {
    var ret = ajaxPostLogined({},api_url+"/get_live_key")
    if(!isEmpty(ret)){
        if(!ret['code']){
            $(".live-pushkey-show").html(CreatePushKey(ret['data']['pushkey']));
            $(".live-pullkey-show").html(ret['data']['pullkey']);
        }
    }
}

function CreatePushKey(key) {
    return "rtmp://106.53.132.162:1935/http_flv?key="+key;
}

function ChangeTitle() {
        var params={
        "title":document.getElementById("live-title-input").value,
    };
    var ret = ajaxPostLogined(params,api_url+"/title_change");
    if(!isEmpty(ret)){
        if(!ret['code']){
            location.reload();
        }
        else{
            alert(ret['msg']);
        }
    }
}

function ChangeType() {
    var params={
        "type_id":document.getElementById("live-type-input").value,
    };
    var ret = ajaxPostLogined(params,api_url+"/type_change");
    if(!isEmpty(ret)){
        if(!ret['code']){
            location.reload();
        }
        else{
            alert(ret['msg']);
        }
    }
}
