api_url="/api/v1.0";

function isEmpty(item) {
    if (item == '' || item == undefined || item == null) {
        return true;
    } else return false;
}

function ajaxPost(data, url) {
    var retData=null;
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'JSON',
        async:false,

    }).done(function (ret) {
        retData = ret;
    });
    return retData;

}

function ajaxGET(url) {
    var retData=null;
    $.ajax({
        url: url,
        type: 'GET',
        async:false,

    }).done(function (ret) {
        retData = ret;
    });
    return retData;

}

function ajaxPostLogined(data, url) {
    var retData=null;
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'JSON',
        async:false,
        beforeSend: function (XMLHttpRequest) {
            XMLHttpRequest.setRequestHeader("Authorization", "Bearer "+localStorage.getItem("access_token"));
        },
        success:function (ret) {
            retData = ret
        },
        complete:function (xhr) {
            if (xhr.status==401){
                if(get_refresh_token()){
                    retData = ajaxPostLogined(data,url);
                }else{
                    // loginInvailable();
                }
            }
        }
    });
    return retData;

}

function ajaxPostLoginedFile(data, url) {
    var retData=null;
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'JSON',
        async:false,
        processData: false,
        contentType: false,
        beforeSend: function (XMLHttpRequest) {
            XMLHttpRequest.setRequestHeader("Authorization", "Bearer "+localStorage.getItem("access_token"));
        },
        success:function (ret) {
            retData = ret
        },
        complete:function (xhr) {
            if (xhr.status==401){
                if(get_refresh_token()){
                    retData = ajaxPostLogined(data,url);
                }else{
                    // loginInvailable();
                }
            }
        }
    });
    return retData;

}

function get_refresh_token() {
    var refresh_url = api_url+"/refresh";
    var retData=false;
    $.ajax({
        url: refresh_url,
        type: 'POST',
        dataType: 'JSON',
        async:false,
        beforeSend: function (XMLHttpRequest) {
            XMLHttpRequest.setRequestHeader("Authorization", "Bearer "+localStorage.getItem("refresh_token"));
        },
        success:function(ret){
          localStorage.setItem("access_token",ret['access_token']);
          retData = true;
        },
    });

    return retData;
}

function loginInvailable() {
    window.location = "/login";
}


function GetRoomName(url) {
    var arr1 = url.split("/");
    var arr2 = arr1[arr1.length-1].split("?");
    var arr3 = arr2[arr2.length-1].split("#");
    var str = arr3[0];
    return str;
}

function GetTopUrl(url) {
    var arr1 = url.split("/");
    // alert(arr1[2]);
    return arr1[2];
}