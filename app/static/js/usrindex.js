document.write("<script type='text/javascript' src='../static/js/ajaxPost.js'></script>");

function upload_head() {
    var animateimg = $(".InputHead").val(); //获取上传的图片名 带//
    var imgarr = animateimg.split('\\'); //分割
    var myimg = imgarr[imgarr.length - 1]; //去掉 // 获取图片名
    var houzui = myimg.lastIndexOf('.'); //获取 . 出现的位置
    var ext = myimg.substring(houzui, myimg.length).toUpperCase();  //切割 . 获取文件后缀

    var file = $('#InputHead').get(0).files[0]; //获取上传的文件
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
        data.append('images', $('#InputHead')[0].files[0]);
        var ret = ajaxPostLoginedFile(data,api_url+"/changeHead");
        if(!isEmpty(ret)){
           document.getElementById('user_head_pic').src = "../"+ret["data"]['url'];
            return true
        }
        return false;
    }
}


function ClickInputHead() {
    return $("#InputHead").click();

}


$(function () {
   var usr_data = ajaxPostLogined({},api_url+"/usr");
   if(!isEmpty(usr_data)){
       var data = usr_data['data'];
       $(".usr-face").attr("src","../static/img/"+data['face']);
       $(".usr-account-show").html(data['account']);
       $(".usr-username-show").html(data['username']);
       $(".usr-phone-show").html(data['phone']);
       $(".usr-email-show").html(data['email']);
       $(".usr-info-show").html(data['info']);
       $(".usr-sex-show").html(GetSex(data['sex']));
       var opt = $("#usr-sex-input").find('option');
       opt[data['sex']].selected=true;
   }
});

function GetSex(sexnum) {
    if(sexnum==0)return "保密";
    else if(sexnum==1)return "男";
    else if(sexnum==2)return "女";
    else return "未知";
}

function ChangeHead() {
    var params = {
        "url": document.getElementById('user_head_pic').src
    };

    var ret = ajaxPostLogined(params,api_url+"/changeHeaded");
    if(!isEmpty(ret)){
        window.location.reload();
    }
}

function ChangeUsername() {
    var params={
        "username":document.getElementById("usr-name-input").value,
    };
    var ret = ajaxPostLogined(params,api_url+"/username_change");
    if(!isEmpty(ret)){
        if(!ret['code']){
            location.reload();
        }
        else{
            alert(ret['msg']);
        }
    }
}

function ChangePassword() {
    var params={
        "password":document.getElementById("usr-pwd-input").value,
    };
    var ret = ajaxPostLogined(params,api_url+"/password_change");
    if(!isEmpty(ret)){
        if(!ret['code']){
            location.reload();
        }
        else{
            alert(ret['msg']);
        }
    }
}

function ChangeSex() {
    var params={
        "sex":document.getElementById("usr-sex-input").value,
    };
    var ret = ajaxPostLogined(params,api_url+"/sex_change");
    if(!isEmpty(ret)){
        if(!ret['code']){
            location.reload();
        }
        else{
            alert(ret['msg']);
        }
    }
}


function ChangeEmail() {
    var params={
        "email":document.getElementById("usr-email-input").value,
    };
    var ret = ajaxPostLogined(params,api_url+"/email_change");
    if(!isEmpty(ret)){
        if(!ret['code']){
            location.reload();
        }
        else{
            alert(ret['msg']);
        }
    }
}

function ChangeInfo() {
    var params={
        "info":document.getElementById("usr-info-input").value,
    };
    var ret = ajaxPostLogined(params,api_url+"/info_change");
    if(!isEmpty(ret)){
        if(!ret['code']){
            location.reload();
        }
        else{
            alert(ret['msg']);
        }
    }
}

function RdrLiverIndex() {
    window.location.href = "/liver"
}

