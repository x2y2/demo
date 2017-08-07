
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
    $.messager.confirm("操作提示",'确认删除吗?',function(data) {
      var blog_id = $("#blog_id").text();
      if (data) {
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
      }
    }); 
  });
  //头像上传自动提交
  $('#upload-pic').change(function(){
    $('#upload-pic-form').submit();
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

  $("[data-toggle='tooltip']").tooltip();

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
  //将作者添加到关注列表
  $("#follower").click(function(){
    var path = window.location.pathname.substring(0,23);
    var url = path + '/' + 'following';
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
  //取消关注作者
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
/**end**/
});

