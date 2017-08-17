
$(function(){
/**begin**/
  //添加新文章
  $("#add_blog").click(function(){
    var blog_title = $("#blog_title").val();
    var blog_content = $("#blog_content").val();
    if(blog_title == "")
    {
      alert("标题不能为空！");
      return;
    }
    else if(blog_content == "") 
    {
      alert("正文不能为空");
      return;
    }
    $.ajax({
      type: "POST",
      url: "/blog/new/add_blog",
      data: {
        "blog_title": blog_title,
        "blog_content": blog_content
      },
      success: function(data) {
        if(data['status'] == 'fail') {
          alert("新增失败" + data['info']);
        }
        else {
          window.location.href = "/blog/" + data['info'];
        }
      },
      error: function(data) {
        alert(data['info']);
      }
    });
  }); 
  //更新文章
  $("#update_blog").click(function(){
    var blog_id = $("#blog_id").text()
    var blog_title = $("#blog_title").val();
    var blog_content = $("#blog_content").val();
    if(blog_title == "")
    {
      alert("标题不能为空！");
      return;
    }
    else if(blog_content == "") 
    {
      alert("正文不能为空");
      return;
    }
    $.ajax({
      type: "POST",
      url: "/blog/edit/update_blog",
      data: {
        "blog_id": blog_id,
        "blog_title": blog_title,
        "blog_content": blog_content
      },
      success: function(data) {
        if(data['status'] == 'fail') {
          alert("提交失败" + data['info']);
        }
        else {
          window.location.href = "/blog/" + blog_id;
        }
      },
      error: function() {
        alert(data['info']);
      }
    });
  }); 
 
  //删除文章
  $("#edit_delete_blog").click(function(){
    var blog_id = $("#blog_id").text();
    $.ajax({
      type: "POST",
      url: "/blog/edit/delete_blog",
      data: {
        "blog_id": blog_id
      },
      success: function(data) {
        if(data['status'] == 'fail') {
           alert(data['info']);
        }
        else {
          //alert(data['info'])
          window.location.href = "/users/" + data['info'];
        }
      },
      error: function(data) {
        alert(data['info']);
      }
    });
  });
  //头像上传自动提交
  $('#upload-pic').change(function(){
    $('#upload-pic-form').submit();
  });
  //微信二维码上传自动提交
  $('#webchat-upload-pic').change(function(){
    $('#webchat-pic-form').submit();
  });
  /**返回到顶部**/
  $("#scrolltop").hide(); //首先将#scrolltop隐藏
  $(function() {
    $(window).scroll(function() {
      if ($(window).scrollTop() > 100) { //当滚动条的位置处于距顶部100像素以下时，跳转链接出现，否则消失
        $("#scrolltop").show();
      } else {
        $("#scrolltop").hide();
      }
    });
    $("#scrolltop").click(function() { //当点击跳转链接后，回到页面顶部位置
      $('body,html').animate({
        scrollTop: 0
      },
      1000);
      return false;
    });
  });
  //鼠标滑过显示提示框
  $("[data-toggle='tooltip']").tooltip().css({'backgroundColor':'black','borderColor':'black'});

  //文章评论按钮隐藏
  $("#under-comment").hide();
  $("#new-comment").click(function(){
    $("#under-comment").show();
  });
  $("#cancel-comment").click(function(){
    $("#under-comment").hide();
  });
  /**搜索框伸缩**/
  $("#q").focus(function(){
    $("#q").animate({"width":300},400);
  });
  $("#q").blur(function(){
    $("#q").animate({"width":200},400);
  });
  //从用户页面添加关注
  $("#follower").click(function(){
    var path = window.location.pathname.substring(0,23);
    var url = path + '/' + 'following_add';
    $.ajax({
      type: "post",
      url: url,
      cache: false,
      data: {"url": url},
      success: function(data) {
        if (data['status'] == 'success') {
          $("#follower").hide();
          $("#followed").show();
        }
        else if (data['status'] == '/login'){
          alert(data['info']);
          //window.location.href = data['info'];
        }
      },
      error: function(data) {
        alert(data['info']);
      },
    });    
  });
  
  //从用户页面取消
  $("#followed").click(function(){
    var path = window.location.pathname.substring(0,23);
    var url = path + '/' + 'following_remove';
    $.ajax({
      type: "post",
      url: url,
      cache: false,
      data: {"url": url},
      success: function(data) {
        if (data['status'] == 'success') {
          $("#follower").show();
          $("#followed").hide();
        //alert(data['info']);
        }
        else if (data['status'] == '/login'){
          alert(data['info']);
        }
      },
      error: function(data) {
        alert(data['info']);
      },
    });    
  });
  //从文章页面添加关注
  $("#blog-follower").click(function(){
    var path = window.location.pathname.substring(0,23);
    var url = path + '/' + 'following_add';
    var author_id = $("#blog-author-id").text();
    $.ajax({
      type: "post",
      url: url,
      cache: false,
      data: {"url": url,"author_id": author_id},
      success: function(data) {
        if (data['status'] == 'success') {
          $("#blog-follower").hide();
          $("#blog-followed").show();
          //alert(data['info'])
        }
        else if (data['status'] == '/login'){
          alert(data['info']);
          //window.location.href = data['info'];
        }
      },
      error: function(data) {
        alert(data['info']);
      },
    });    
  });
  //从文章页面取消关注
  $("#blog-followed").click(function(){
    var path = window.location.pathname.substring(0,23);
    var url = path + '/' + 'following_remove';
    var author_id = $("#blog-author-id").text();
    $.ajax({
      type: "post",
      url: url,
      cache: false,
      data: {"url": url,"author_id": author_id},
      success: function(data) {
        if (data['status'] == 'success') {
          $("#blog-follower").show();
          $("#blog-followed").hide();
        //alert(data['info']);
        }
        else if (data['status'] == '/login'){
          alert(data['info']);
        }
      },
      error: function(data) {
        alert(data['info']);
      },
    });    
  });
  $("#following > li").each(function(){
    //从关注页面添加，取消关注用户
    $(this).find("#following-follower").click(function(){
      var path = window.location.pathname.substring(0,23);
      var url = path + '/' + 'following_u_add';
      var user_id = $(this).closest('li').find("#following-user-id").html();
      var This =  $(this);
      $.ajax({
        type: "post",
        url: url,
        cache: false,
        data: {"url": url,"user_id": user_id},
        success: function(data) {
          This.hide();
          This.closest('li').find("#following-followed").show();
        },
        error: function(data) {
          alert(data['info']);
        },
      });
    });
    $(this).find("#following-followed").click(function(){
      var path = window.location.pathname.substring(0,23);
      var url = path + '/' + 'following_u_remove';
      var user_id = $(this).closest('li').find("#following-user-id").html();
      var This = $(this);
      $.ajax({
        type: "post",
        url: url,
        cache: false,
        data: {"url": url,"user_id": user_id},
        success: function(data) {
          This.hide();
          This.closest('li').find("#following-follower").show();
        },
        error: function(data) {
          alert(data['info']);
        },
      });
    });
  });

  //从粉丝页面添加,取消关注用户
  $("#follower-ul > li").each(function(){
    $(this).find("#follower-following").click(function(){
      var path = window.location.pathname.substring(0,23);
      var url = path + '/' + 'follower_u_add';
      var user_id = $(this).closest('li').find("#follower-user-id").html();
      var This = $(this);
      $.ajax({
        type: "post",
        url: url,
        cache: false,
        data: {"url": url,"user_id": user_id},
        success: function(data) {
          if (data['status'] == 'success'){
            This.hide();
            This.closest('li').find("#follower-followed").show();
          } else {
            alert(data['info']);
          }
        },
        error: function(data) {
          alert(data['info']);
        },
      });
    });
    $(this).find("#follower-followed").click(function(){
      var path = window.location.pathname.substring(0,23);
      var url = path + '/' + 'follower_u_remove';
      var user_id = $(this).closest('li').find("#follower-user-id").html();
      var This = $(this);
      $.ajax({
        type: "post",
        url: url,
        cache: false,
        data: {"url": url,"user_id": user_id},
        success: function(data) {
          if (data['status'] == 'success'){
            This.hide();
            This.closest('li').find("#follower-following").show();
          } else
          {
            alert(data['info']);
          }
        },
        error: function(data) {
          alert(data['info']);
        },
      });
    });
  });
  //用户页面的菜单高亮显示
  $(window).on("load hashchange",function(){
    $("#menu-list").find('a').each(function(){
      var url = window.location.protocol + '//' +  window.location.hostname + ':' + location.port
      if (url + $(this).attr('href') == String(window.location)) {
        $(this).addClass("active");
      }
    });
  });
  //个人设置页面菜单高亮显示
  $(window).on("load hashchange",function(){
    $("#aside-ul").find('a').each(function(){
      var url = window.location.protocol + '//' +  window.location.hostname + ':' + location.port
      if (url + $(this).attr('href') == String(window.location)) {
        $(this).find('li').css({"background-color":"#ededed"});
      }
    });
  });

  $(window).on("load hashchange",function(){
    $(".login-sign-title").find('a').each(function(){
      var url = window.location.protocol + '//' +  window.location.hostname + ':' + location.port
      if (url + $(this).attr('href') == String(window.location)) {
        $(this).addClass("active");
      }
    });
  });

  //鼠标滑过导航栏下拉菜单展开
  var timer;
  $(".user").mouseover(function(){
    clearTimeout(timer);
    $(".dropdown-menu").show();
  });
  $(".user").mouseout(function(){
    timer = setTimeout(function(){
      $(".dropdown-menu").hide();
    },100);
  });
  $(".dropdown-menu").mouseover(function(){
    clearTimeout(timer);
    $(".dropdown-menu").show();
  });
  $(".dropdown-menu").mouseout(function(){
    $(".dropdown-menu").hide();
  });
  //个人简介
  $("#personal-intr").hide();
  $("#personal-intr-control").hide();
  $("#personal-intr-edit").click(function(){
    $("#personal_profile").hide();
    $("#personal-intr").show();
    $("#personal-intr-control").show();
  });
  $('#personal-intr-cancle').click(function(){
    $("#personal-intr").hide();
    $("#personal-intr-control").hide();
    $("#personal_profile").show();
  });
  //显示微信二维码删除按钮
  $("#webchat_pic").mouseover(function(){
    $("#webchat_pic_delete").show();
  });
  $("#webchat_pic").mouseout(function(){
    $("#webchat_pic_delete").hide();
  });
  //删除微信二维码
  $("#webchat_pic_delete").click(function(){
    var login_user_id = $("#login_user_id").text();
    var path = window.location.pathname;
    var url = path + '/webchat_delete';
    $.ajax({
      type: "post",
      url: url,
      cache: false,
      data: {"url": url,"login_user_id": login_user_id},
      success: function(data) {
        window.location.href = path;
      },
      error: function(data){
        alert(data['info']);
      },
    });
  });
  //个人资料提交
  $("#personal_profile_save").click(function(){
    var radio = document.getElementsByName("optionsradio");
    for (i = 0 ;i<radio.length; i++) {
      if (radio[i].checked){
        gender = radio[i].value;
      }
    }
    var personal_profile = $(".textarea").val();
    var login_user_id = $("#login_user_id").text();
    var path = window.location.pathname;
    var url = path + '/personal_profile';
    $.ajax({
    type: "post",
    url: url,
    cache: false,
    data: {"url": url,
           "login_user_id": login_user_id,
           "personal_profile": personal_profile,
           "gender": gender
          },
    success: function(data) {
      //alert(data['info']);
      window.location.href = path;
    },
    error: function(data){
      alert(data['info']);
    },
    });
  });
  
  $(".personal-message").click(function(){
    var personal_profile = $(".personal-textarea").val().replace(/\n/g,"<br/>").replace(/\s/g,"&nbsp;");
    var path = window.location.pathname;
    var url = path + '/personal_profile_save';
    $.ajax({
      type: "post",
      url: url,
      cache: false,
      data: {"url": url,"personal_profile": personal_profile},
      success: function(data) {
      //alert(data['info']);
      window.location.href = path;
      },
      error: function(data){
        alert(data['info']);
      },
    });
  });
 
  //弹出微信二维码
    $("#webchat-pic").popover({
      animate: false
    }
    ).on("mouseenter",function(){
      var _this = this;
      $(this).popover("show");
      $(this).siblings(".popover").on("mouseleave",function(){
        $(_this).popover("hide");
      });
    }).on("mouseleave",function(){
      var _this = this;
      setTimeout(function(){
      if (!$(".popover:hover").length){
        $(_this).popover("hide")
      }
      },100);
    });
/**end**/
});

