/**
$(document).ready(function(){
    $("#login").click(function(){
        var user = $("#username").val();
        var pwd = $("#password").val();
        var pd = {"username":user, "password":pwd};
        $.ajax({
            type:"post",
            url:"/login",
            data:pd,
            cache:false,
            success:function(data){
              alert(data['info']);
              //window.location.href = "/";
            },
            error:function(){
                alert("error");
            },
        });
    });
});
**/


function add_blog() {
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
}


function update_blog() {
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
}



/**
function del_blog(name) {
  $.messager.confirm("操作提示",'确认删除吗?',function(data) {
    var rows = name.parentNode.parentNode.rowIndex;
    var blog_id = $("#blogIndex tr:eq("+rows+") td:eq(0)").text();
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
        window.location.href = "/index";
        
      }
    },
    error: function(data) {
      alert(data['info']);
    }
  });
  }
});   
}
**/

function edit_delete_blog() {
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
}


$(document).ready(function() {
$('#upload-pic').change(function(){
  $('#upload-pic-form').submit();
});

  //首先将#scrolltop隐藏
  $("#scrolltop").hide();
  //当滚动条的位置处于距顶部100像素以下时，跳转链接出现，否则消失
  $(function() {
    $(window).scroll(function() {
      if ($(window).scrollTop() > 100) {
        $("#scrolltop").show();
      } else {
        $("#scrolltop").hide();
      }
    });
    //当点击跳转链接后，回到页面顶部位置
    $("#scrolltop").click(function() {
      $('body,html').animate({
        scrollTop: 0
      },
      1000);
      return false;
    });
  });

  $("#under-comment").hide();
  $("#new-comment").click(function(){
    $("#under-comment").show();
  });
  $("#cancel-comment").click(function(){
    $("#under-comment").hide();
  });
});


$(document).ready(function(){
  /**搜索框伸缩**/
  $("#q").focus(function(){
    $("#q").animate({"width":300},400);
  });
  $("#q").blur(function(){
    $("#q").animate({"width":200},400);
  });

  
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
      $(this).find("#following-follower").click(function(){
        $(this).hide();
        $(this).closest('li').find("#following-followed").show();
      });
      $(this).find("#following-followed").click(function(){
        $(this).hide();
        $(this).closest('li').find("#following-follower").show();
      });

      //从关注页面添加关注用户
      $(this).find("#following-follower").click(function(){
        var path = window.location.pathname.substring(0,23);
        var url = path + '/' + 'following_u_add';
        var user_id = $(this).closest('li').find("#following-user-id").html();
        $.ajax({
          type: "post",
          url: url,
          cache: false,
          data: {"url": url,"user_id": user_id},
          success: function(data) {
          },
          error: function(data) {
            alert(data['info']);
          },
        });
      });

      //从关注页面删除关注用户
      $(this).find("#following-followed").click(function(){
        var path = window.location.pathname.substring(0,23);
        var url = path + '/' + 'following_u_remove';
        var user_id = $(this).closest('li').find("#following-user-id").html();
        $.ajax({
          type: "post",
          url: url,
          cache: false,
          data: {"url": url,"user_id": user_id},
          success: function(data) {
          },
          error: function(data) {
            alert(data['info']);
          },
        });
      });
    });

    /**个人设置页面鼠标悬停效果**/
    $("li#aside-list").mouseover(function(){
      $(this).css({"background-color":"#ededed"});
    });  
    $("li#aside-list").mouseout(function(){
      $(this).css({"background-color":"white"});
    });

    
    $("#follower-ul > li").each(function(){
      $(this).find("#follower-following").click(function(){
        $(this).hide();
        $(this).closest('li').find("#follower-followed").show();
      });
      $(this).find("#follower-followed").click(function(){
        $(this).hide();
        $(this).closest('li').find("#follower-following").show();
      });
      //从粉丝页面添加关注用户
      $(this).find("#follower-following").click(function(){
        var path = window.location.pathname.substring(0,23);
        var url = path + '/' + 'follower_u_add';
        var user_id = $(this).closest('li').find("#follower-user-id").html();
        $.ajax({
          type: "post",
          url: url,
          cache: false,
          data: {"url": url,"user_id": user_id},
          success: function(data) {
            if (data['status'] == 'success'){
            } else {
              alert(data['info']);
            }
          },
          error: function(data) {
            alert(data['info']);
          },
        });
      });
      //从粉丝页面取消关注用户
      $(this).find("#follower-followed").click(function(){
        var path = window.location.pathname.substring(0,23);
        var url = path + '/' + 'follower_u_remove';
        var user_id = $(this).closest('li').find("#follower-user-id").html();
        $.ajax({
          type: "post",
          url: url,
          cache: false,
          data: {"url": url,"user_id": user_id},
          success: function(data) {
            if (data['status'] == 'success'){
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
});

