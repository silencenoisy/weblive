document.write("<script type='text/javascript' src='../static/js/ajaxPost.js'></script>");
window.danmu_num = 0;
window.roomname = GetRoomName(location.href);

function SendDaman() {
    var content = document.getElementById("danmu-send-content").value
    if(isEmpty(content)){
        return false;
    }
    var params = {
        "content":content,
        "room_name":window.roomname,
        "last_time":window.lasttime,
    };

    var retData = ajaxPostLogined(params,api_url+"/send_danmu");
    if(!isEmpty(retData)){
        console.log("发送成功!");
        document.getElementById("danmu-send-content").value = "";
    }
    else{
        console.log("发送失败!")
    }
}

$(function () {
    var myDate = new Date();
    window.lasttime = parseInt(myDate.getTime()/1000);
    var t1 = window.setInterval(fetch_danmu,2000);

});

function fetch_danmu() {
    var params = {
        "room_name":window.roomname,
        "danmu_num":window.danmu_num,
        "last_time":window.lasttime,
    };
    var retData = ajaxPost(params,api_url+"/fetch_danmu");
    if(!isEmpty(retData)){
        window.lasttime = retData['new_time'];
        var list_wrap = $("#chat-room__list");

        for(var one_danmu in retData['data']){

            var danmu_html = DanmuHtml(retData['data'][one_danmu])
            list_wrap.append(danmu_html);
        }
    }
}


function DanmuHtml(data) {
    var dHtml = "<li class=\"J_msg\">"+"<div><span class=\"glyphicon glyphicon-music\" style='font-size: 20px;color: pink'>"+data['username']+"(亲密等级"+GetLevel(data['cvalue'])+")</span>："+data['content']+"</div>"+"</li>"
    return dHtml
}


function GetLevel(evalue) {
    // alert("e"+evalue)
    var base_level = 20;
    for(var j=0;j<30;j++){
        if(evalue>base_level){
            base_level*=2;
        }else{
            // alert(j)
            return j;
        }
    }
}
