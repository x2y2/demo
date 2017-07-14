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
        window.location.href = "/";
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
        window.location.href = "/";
      }
    },
    error: function(data) {
      alert(data['info']);
    }
  });
  }
});   
}

$(document).ready(function () {
    $.goup({
        trigger: 100,
        bottomOffset: 150,
        locationOffset: 100,
        title: '回到顶部',
        titleAsText: true
    });
});

$('#upload-pic').change(function(){
  $('#upload-pic-form').submit();
});

  

