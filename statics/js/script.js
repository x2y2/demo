$(document).ready(function(){

});

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
                window.location.href = "/";
            },
            error:function(){
                alert("error");
            },
        });
    });
});



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
        warningNotify("新增失败" + data['info']);
      }
      else {
        window.location.href = "/index"
        //successNotify("新增成功" + data['info']);
      }
    },
    error: function() {
      errNotify("网络异常");
    }
  });
}



function update_blog() {
  var blog_id = $("#blog_id").text()
  var blog_title = $("#blog_title").val();
  var blog_content = $("#blog_content").val();
  alert(blog_id)
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
        //window.location.href = "/index"
        alert('ok'+ data['info']);
      }
    },
    error: function() {
      alert(data['info']);
    }
  });
  
}