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
                window.location.href = "/index/"+data;
            },
            error:function(){
                alert("error");
            },
        });
    });
});

/**
var page_size = 1;
var total_pages = 1;
var visiblePages = 8;

$(document).ready(function(){
  get_all_blogs(1);
});

function twbsPagination() {
  $('#pagination_zc').twbsPagination({
    totalPages: total_pages,
    visiblePages: visiblePages > 8 ? 8 : visiblePages,
    startPage: 1,
    first: "首页",
    prev: "上一页",
    next: "下一页",
    last: "末页",
    onPageClick: function(event,page) {
      get_all_blogs(page);
    }
  });
}
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