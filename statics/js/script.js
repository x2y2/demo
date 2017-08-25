
$(function(){
/**begin**/

  //用户登录
  $("#login_submit").click(function(){
    $.ajax({
      type: 'post',
      url: '/login',
      data: $('#loginForm').serialize(),
      success: function(data) {
         if (data['status'] == 'noexists') {
           $('.alert').html(data['info']).addClass('alert-danger').show();
         }
         else if (data['status'] == 'errorpassword') {
           $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
         }
         else if (data['status'] == 'nouser') {
           $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
         }
         else if (data['status'] == 'nopassword') {
           $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
         }
         else if (data['status'] == 'success') {
           window.location.href = "/";
         }
      },
      error: function(data) {
         $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
      }
    });
  });

  //用户注册
  $("#signup_submit").click(function(){
    $.ajax({
      type: 'post',
      url: '/sign_up',
      data: $('#signupForm').serialize(),
      success: function(data) {
         if (data['status'] == 'userexists') {
           $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
         }
         else if (data['status'] == 'emailexists') {
           $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
         }
         else if (data['status'] == 'nouser') {
           $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
         }
         else if (data['status'] == 'nopassword') {
           $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
         }
         else if (data['status'] == 'noemail') {
           $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
         }
         else if (data['status'] == 'emailformat') {
           $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
         }
         else if (data['status'] == 'success') {
           window.location.href = data['info'];
         }
      },
      error: function(data) {
         $('.alert').html('err').addClass('alert-danger').show().delay(1500).fadeOut();
      }
    });
  });


  //添加新文章
  $("#add_blog").click(function(){
    var blog_title = $("#blog_title").val();
    var blog_content = $("#blog_content").val();
    if(blog_title == ""){
      $('.alert').html('标题不能为空！').addClass('alert-danger').show().delay(1500).fadeOut();
      return;
    }
    else if (blog_title.length > 50){
        $('.alert').html('标题不能太长！').addClass('alert-warning').show().delay(1500).fadeOut();
        return;
    }
    else if(blog_content == "") 
    {
      $('.alert').html('正文不能为空！').addClass('alert-warning').show().delay(1500).fadeOut();
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
        if(data['status'] == 'success') {
          window.location.href = "/blog/" + data['info'];
        }
        else {
          $('.alert').html('添加失败').addClass('alert-warning').show().delay(1500).fadeOut();
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
    else if (blog_title.length > 50){
        alert("标题太长");
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
        if(data['status'] == 'success') {
          window.location.href = "/blog/" + blog_id;
        }
        else {
          $('.alert').html('更新失败').addClass('alert-warning').show().delay(1500).fadeOut();
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
        if(data['status'] == 'success') {
          window.location.href = "/users/" + data['info'];
        }
        else {
          $('.alert').html('删除失败').addClass('alert-warning').show().delay(1500).fadeOut();
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

  //基础设置
  $("#setting_basic_submit").click(function(){
    $.ajax({
      type: 'post',
      url: '/setting/basic/info',
      data: $('#settingbasicForm').serialize(),
      success: function(data) {
        if (data['status'] == 'success') {
          $('.alert').html(data['info']).addClass('alert-success').show().delay(1500).fadeOut();
        }
        else if (data['status'] == 'emailexists') {
          $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
        }
        else if (data['status'] == 'userexists') {
          $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
        }
        else if (data['status'] == 'nouser') {
          //alert(data['info'])
          $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
        }
        else {
          $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
        }
      },
      error: function(data) {
        $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
      }
    });
  });

  //账号管理
  $("#account_manage_submit").click(function(){
    $.ajax({
      type: 'post',
      url: '/setting/basic/account',
      data: $('#accountmanageForm').serialize(),
      success: function(data) {
        if (data['status'] == 'success') {
          $('.alert').html(data['info']).addClass('alert-info').show().delay(1500).fadeOut();
        }
        else if (data['status'] == 'errpassword') {
          $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
        }
        else if (data['status'] == 'samepassword') {
          $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
        }
        else if (data['status'] == 'errconfirm') {
          $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
        }
        else if (data['status'] == 'nopassword') {
          $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
        }
        else {
          $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
        }
      },
      error: function(data) {
        $('.alert').html(data['info']).addClass('alert-danger').show().delay(1500).fadeOut();
      }
    });
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
      //window.location.href = path;
      $('.alert').html('更新成功').addClass('alert-success').show().delay(1500).fadeOut();
    },
    error: function(data){
      alert(data['info']);
    },
    });
  });
  //个人主页的个人介绍提交
  $(".personal-message").click(function(){
    var personal_profile = $(".personal-textarea").val().replace(/\n/g,"<br/>").replace(/\s/g,"&nbsp;");
    var href = window.location.href;
    var reg = new RegExp("/users/[0-9a-z]{16}");
    var pathname = href.match(reg);
    var url = pathname + '/personal_profile_save';
    $.ajax({
      type: "post",
      url: url,
      cache: false,
      data: {"url": url,"personal_profile": personal_profile},
      success: function(data) {
      //alert(data['info']);
      window.location.href = href;
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


    /**
     * 弹出式提示框，默认1.2秒自动消失
     * @param message 提示信息
     * @param style 提示样式，有alert-success、alert-danger、alert-warning、alert-info
     * @param time 消失时间
     
    function prompt(message, style, time)
    {
        style = (style === undefined) ? 'alert-success' : style;
        time = (time === undefined) ? 1200 : time;
        $('<div>')
            .appendTo('body')
            .addClass('alert ' + style)
            .html(message)
            .show()
            .delay(time)
            .fadeOut();
    };
    **/
    
    //设置页脚
    $(window).bind("load", function() { 
      var footerHeight = 0;
      var footerTop = 0;
      var $footer = $("#footer"); 
      positionFooter(); //定义positionFooter function 
      function positionFooter() { //取到div#footer高度 
        footerHeight = $footer.height(); //div#footer离屏幕顶部的距离 
        footerTop = ($(window).scrollTop()+$(window).height()-footerHeight)+"px"; 
          //if ( ($(document.body).height()+footerHeight) < $(window).height()) { 
          if (document.body.clientHeight < document.documentElement.clientHeight) {
              $footer.css({ position: "absolute" }).stop().animate({ top: footerTop }); 
          } else { 
            $footer.css({ position: "static" }); 
          } 
        } 

      });
    
    //点赞
    $(".comment").each(function(){
      $(this).find('#comment_upvote').click(function(){
        var state = $(this).closest("li").find("#upvote_state").text();
        var upvote_count = $(this).closest("li").find("#upvote_count").text()
        var obj = $(this).closest("li").find("#comment_upvote");
        var blog_id = $("#blog_content_id").text();
        var comment_id = $(this).closest('li').find('#comment_id').text();
        var url = '/blog/' + blog_id + '/add_upvote';
        var _this = $(this)
        if (state == '0') {  
            $.ajax({
              type: 'post',
              url: url,
              data: {"url":url,
                     "blog_id":blog_id,
                     "comment_id":comment_id
                    }, 
              success: function(data){
                //_this.closest("li").find("#upvote_state")[0].innerHTML = '1';
                _this.closest("li").find("#upvote_state").get(0).innerHTML = '1';
                var count =  String(Number(upvote_count) + 1);
                _this.closest("li").find("#upvote_count").get(0).innerHTML = count;
                obj.css('color','red');
              }, 
              error: function(data){
                alert(data['info']);
              }
            }); 
          } else {
              $.ajax({
                type: 'post',
                url: url,
                data: {'url': url,'blog_id': blog_id,'comment_id':comment_id}, 
                success: function(data) {
                  _this.closest("li").find("#upvote_state").get(0).innerHTML = '0';
                  var count =  String(Number(upvote_count) - 1);
                  _this.closest("li").find("#upvote_count").get(0).innerHTML = count;
                  obj.css('color','gray');
                }, 
                error:function(data){
                  alert(data['info']);
                }
              });
          } 
      });
    });
    
/**end**/
});

