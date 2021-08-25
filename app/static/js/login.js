document.write("<script type='text/javascript' src='../static/js/ajaxPost.js'></script>");

function Login() {
    // alert($("#login-name").innerText,"sss");
    var params = {
        "username": document.getElementById("login-name").value,
        "password": document.getElementById("login-pwd").value,
    };
    if (isEmpty(params['username'])) {
        // window.alert(params['username']);
        alert("用户名不能为空");
        return false;
    } else if (isEmpty(params['password'])) {
        alert("密码不能为空");
        return false;
    }
    var ret = ajaxPost(params, api_url+"/checkLogin")
    if(!isEmpty(ret)){
        var isSuccess=ret['code'];
        if(!isSuccess){
            var access_token =  ret["access_token"];
            var refresh_token = ret['refresh_token'];
            localStorage.setItem("access_token",access_token);
            localStorage.setItem("refresh_token",refresh_token);
            LoginSuccess(ret['next'],ret['data']);

            return true;
        }else if(isSuccess==2) {
            alert('用户或密码错误');
            return false;
        }else{
            alert('未知错误');
            return false;
        }
    }
}

function Register() {
    var password2 = document.getElementById("register-pwd2").value;
    var params = {
        "username": document.getElementById("register-name").value,
        "password": document.getElementById("register-pwd").value,
        "phone": document.getElementById("register-phone").value,
    };
    if (isEmpty(params['username'])) {
        // window.alert(params['username']);
        alert("用户名不能为空");
        return false;
    } else if (isEmpty(params['password'])) {
        alert("密码不能为空");
        return false;
    } else if (isEmpty(password2)){
        alert("确认密码不能为空");
        return false;
    }else if (isEmpty(params['phone'])){
        alert("电话号不能为空");
        return false;
    }else if(params['password']!=password2){
        alert("两次密码不一致");
        return false;
    }
    var ret = ajaxPost(params, api_url+"/register_port");
    if(!isEmpty(ret)){
        var isSuccess=ret['code'];
        if(!isSuccess){
            var access_token =  ret["access_token"];
            var refresh_token = ret['refresh_token'];
            localStorage.setItem("access_token",access_token);
            localStorage.setItem("refresh_token",refresh_token);
            LoginSuccess(ret['next'],ret['data']);

            return true;
        }else if(isSuccess==1001) {
            alert('该手机号已被注册');
            return false;
        }else{
            alert('未知错误');
            return false;
        }
    }
}


function LoginSuccess(next,usr_data) {
    localStorage.setItem("account",usr_data['account']);
    localStorage.setItem("face",usr_data['face']);
    localStorage.setItem("role_id",usr_data['role_id']);
    localStorage.setItem("evalue",usr_data['evalue']);
    if(isEmpty(next)){
        window.location.reload();
    }
    else{
        window.location = next;
    }
}

$(function () {
    var retdata = ajaxPostLogined({},api_url+"/usr");
    if(retdata){
        $("#login-div").addClass("hide");
        $("#logout-div").removeClass("hide");
        $("#usr-home-link").html(retdata['data']['username']);
        $(".home-link").attr("href","/user/"+retdata['data']['username']);
        var face = retdata['data']['face'];
        if(!isEmpty(face)) {
            $(".usr-face").attr("src", "../static/img/" + face);
        }else{
            $(".usr-face").attr("src", "../static/img/default.png");
        }
    }

});

function Logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.reload();
}

$(function () {
    mysub();
})

function mysub() {
    var parent = $("#my-subscription")
    var ret = ajaxPostLogined({},api_url+"/usr/subscription")
    if(!isEmpty(ret)){
        if(!ret['code']){
            var data = ret['data'];
            for(var i in data){
                parent.append(sub_html(data[i]));
            }
        }
    }
}

function sub_html(data) {
    var is_live = "在播",cover=data['cover'];
    if(!data['is_live']){
        is_live = "不在播";
    }
    if(!cover){
        cover = "default_cover.png"
    }
    return "<li><a href=\"/live/"+data['name']+"\">\n" +
        "                        <img class=\"img-rounded\" width=\"45\" height=\"45\" src=\"../static/img/"+cover+"\">\n" +
        "                            "+data['name']+"\n" +
        "                        <span class=\"\" style=\"color:peru;\">("+is_live+")</span>\n" +
        "                    </a>\n" +
        "                </li>"
}


