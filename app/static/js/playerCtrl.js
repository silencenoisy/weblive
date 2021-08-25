document.write("<script type='text/javascript' src='../static/js/ajaxPost.js'></script>");


liveUrl = "http://106.53.132.162/live?port=1935&app=http_flv";
serverUrl = "127.0.0.1:5000";
function LiveUrl() {
    var params = {
        // "blog_id": blog_id,
    };
    var roomname = GetRoomName(location.href);
    var roomurl = null;
    $.ajax({
        url: "/api/v1.0/live/"+roomname,
        type: "post",
        data: params,
        async:false,
        dataType: "json",
        // headers:{ "X-CSRFtoken":csrftoken},
    }).done(function (ret) {
        if (!ret['code']) {
            var room_data = ret['data'];
            roomurl = liveUrl+"&stream="+room_data['url'];
            RoomSet(room_data);

        } else {
            alert(ret['msg']);
        }
    });
    return roomurl
}

$(function () {
    IsLiveRound();
    var t2 = window.setInterval(IsLiveRound,5000);
});

function IsLiveRound() {

    if(!IsLive(GetRoomName(location.href))){
        console.log(IsLive(GetRoomName(location.href)));
        $("#unlive").html("主播暂时不在哦");
    }
    else{
        $("#unlive").html("");
    }
}

function RoomSet(data) {
    if(!isEmpty(data['face'])){
        $("#avatar-img").attr("src","../static/img/"+data['face']);
    }
    else{
        $("#avatar-img").attr("src","../static/img/default.png");
    }
    $("#J_roomTitle").html(data['title']);
}



function HidePlayerCtrlWrap() {
    $("#player-ctrl-wrap").css("bottom", "16px");
}

function ShowPlayerCtrlWrap() {
    $("#player-ctrl-wrap").css("bottom", "60px");
}

function StopVideoBtnShow() {
    $("#player-btn").attr("class","player-pause-btn");
    $("#player-btn").attr("title","继续播放");
    $(".player-ctrl-wrap .player-refresh-btn").css("display","block");
    $(".player-ctrl-wrap .player-play-big").css("display","none");
}

function StartVideoBtnShow() {
    $("#player-btn").attr("class","player-play-btn");
    $("#player-btn").attr("title","暂停观看");
    $(".player-ctrl-wrap .player-refresh-btn").css("display","none");
    $(".player-ctrl-wrap .player-play-big").css("display","block");
}

function StopVideo() {
    $("#smwd-video").trigger("pause");
}

function StartVideo() {
    var url = LiveUrl();
     if (flvjs.isSupported()) {
        var videoElement = document.getElementById('smwd-video');
        var flvPlayer = flvjs.createPlayer({
            type: 'flv',
            url: url
        });
        flvPlayer.attachMediaElement(videoElement);
        flvPlayer.load();
        flvPlayer.play();
    }
}

function SoundOff(){
    $("#player-sound-btn").attr("class","player-sound-off");
    $(".player-ctrl-wrap .sound-progress .sound-btn").css('left', 0);
    $(".player-ctrl-wrap .sound-progress .sound-bar").width(0);
    $("#smwd-video")[0].volume=0;
}

function SoundOn(sound=1){
    $("#player-sound-btn").attr("class","player-sound-on")
    var left = sound*85;
    $(".player-ctrl-wrap .sound-progress .sound-btn").css('left', left);
    $(".player-ctrl-wrap .sound-progress .sound-bar").width(left);
    $("#smwd-video")[0].volume=sound;
}

function IsLive(roomname) {
    var params = {
        "roomname":roomname,
    };
    var ret = ajaxPost(params,api_url+"/is_live");
    if(!isEmpty(ret)){
        if(!ret['code']){
            if(ret['data']['is_live']){
                return true;
            }
        }
    }
    return false;
}


function DanmuOff(){

}

function DanmuOn(){

}

// $(function () {
//     $(".down-toggle-btn").click(function () {
//
//     });
//     $(".down-menu").mouseleave(function () {
//         $(".down-toggle-btn").dropdown("toggle");
//     });
//
//
// });
// $(document).ready(function(){
//     $(document).off('click.bs.dropdown.data-api');
// });
// $(document).ready(function(){
//     dropdownOpen();//调用
// });
// /**
//  * 鼠标划过就展开子菜单，免得需要点击才能展开
//  */
// function dropdownOpen() {
//
//     var $dropdownLi = $('.dropdown');
//
//     $dropdownLi.mouseover(function() {
//         $(this).addClass('open');
//     }).mouseout(function() {
//         $(this).removeClass('open');
//     });
// }



// 视频播放
$(function () {
    StartVideo();
});

// 操作按钮弹出
$(function () {
    var timeoutFlag = null;
    $("#player-wrap,#player-ctrl-wrap").mousemove(function () {
        clearTimeout(timeoutFlag);
        ShowPlayerCtrlWrap();
        timeoutFlag=setTimeout(HidePlayerCtrlWrap,2000)
    });

    $("#player-wrap,#player-ctrl-wrap").mouseout(function () {
        HidePlayerCtrlWrap();
    });
});

// 操作按钮功能绑定
$(function () {
    var onPlayFlag = true;

    $("#player-btn").click(function () {
        if(onPlayFlag){
            StartVideoBtnShow();
            StopVideo();
            onPlayFlag = false;
        }
        else{
            StopVideoBtnShow();
            StartVideo();
            onPlayFlag = true;
        }
    });
    $(".player-ctrl-wrap .player-play-big").click(function () {
        if(!onPlayFlag){
            StopVideoBtnShow();
            StartVideo();
            onPlayFlag = true;
        }
    })

    $(".player-ctrl-wrap .player-refresh-btn").click(function () {
        StartVideo();
    })

});

$(function () {
    var onSound = true;
    var soundRange = 1;
    $("#player-sound-btn").click(function () {
        if(onSound){
            SoundOff();
            onSound = false;
        }
        else{
            SoundOn(soundRange);
            onSound=true;
        }
    })


        var el=$(".player-ctrl-wrap .sound-progress .sound-bg").offset;
        var tag = false,ox = el.left,left = 85,bgleft = el.left;
        $(".player-ctrl-wrap .sound-progress .sound-btn").mousedown(function(e) {
            ox = e.pageX - left;
            tag = true;
        });
        $(document).mouseup(function() {
            tag = false;
        });
        $(".player-ctrl-wrap .sound-progress .sound-btn").mousemove(function(e) {//鼠标移动
            if (tag) {
                left = e.pageX - ox;
                if (left <= 0) {
                    left = 0;
                }else if (left > 85) {
                    left = 85;
                }
                soundRange = left/85;
                if(soundRange==0){
                    SoundOff();
                }else{
                    SoundOn(soundRange);
                }
            }
        });
        $(".player-ctrl-wrap .sound-progress .sound-bg").click(function(e) {//鼠标点击
            if (!tag) {
                alert("sss")
                bgleft = $(".player-ctrl-wrap .sound-progress .sound-bg").offset().left;
                left = e.pageX - bgleft;
                if (left <= 0) {
                    left = 0;
                }else if (left > 85) {
                    left = 85;
                }
                soundRange = left/85;
                if(soundRange===0){
                    SoundOff();
                }else{
                    SoundOn(soundRange);
                }
            }
        });
})

$(function () {
    var danmuOnFlag = true;
    $("#player-danmu-btn").click(function () {
        if(danmuOnFlag){
            $(this).attr("class","danmu-show-btn danmu-hide-btn");
            $(this).attr("title","打开弹幕");
            DanmuOff();
            danmuOnFlag = false;
        }
        else{
            $(this).attr("class","danmu-show-btn");
            $(this).attr("title","关闭弹幕");
            DanmuOn();
            danmuOnFlag = true;
        }
    })
});

$(function () {

    var fullscreen = false;
    let btn = document.getElementById('player-fullscreen-btn');
    let fullarea = document.getElementById('full-screen-part')
    btn.addEventListener('click',function(){
      if (fullscreen) {    // 退出全屏
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
        fullScreenUnset();
      } else {    // 进入全屏
        if (fullarea.requestFullscreen) {
          fullarea.requestFullscreen();
        } else if (fullarea.webkitRequestFullScreen) {
          fullarea.webkitRequestFullScreen();
        } else if (fullarea.mozRequestFullScreen) {
          fullarea.mozRequestFullScreen();
        } else if (fullarea.msRequestFullscreen) {
          // IE11
          fullarea.msRequestFullscreen();
        }
        fullScreenSet();
      }
      fullscreen = !fullscreen;
    })

})

function fullScreenUnset() {

}

function fullScreenSet() {

}


function sendGive(give_id) {
    var params = {
        "roomname":GetRoomName(location.href),
        "give_id":give_id,
        "num":document.getElementById("give-send-"+give_id).value,
    };
    var ret = ajaxPostLogined(params,api_url+"/send_gives");
    if(!isEmpty(ret)){
        if(!ret['code']){
            alert("赠送成功");
        }else if(ret['code']==5){
            alert("余额不足");
        }
    }else{
        console.log("未知错误");
    }
}

function Subscript() {
    var params = {
        "roomname":GetRoomName(location.href),
    };
    var ret = ajaxPostLogined(params,api_url+"/subscript");
    if(!isEmpty(ret)){
        if(!ret['code']){
            if(ret['data']['is_subscript']){
                $("#subscript_btn").html("已订阅");
            }else{
                $("#subscript_btn").html("订阅");
            }
        }
    }
}

function IsSubed() {
    var params = {
        "roomname":GetRoomName(location.href),
    };
    var ret = ajaxPostLogined(params,api_url+"/is_subscript");
    if(!isEmpty(ret)){
        if(!ret['code']){
            if(ret['data']['is_subscript']){
                $("#subscript_btn").html("已订阅");
            }else{
                $("#subscript_btn").html("订阅");
            }
        }
    }
}
$(function () {
    IsSubed();
});




