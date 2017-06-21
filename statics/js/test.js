function validate_required(field,alerttxt)
{
 with(field)
  {
    if (value == null||value == "")
      {alert(alerttxt);return false}
    else
      {return true}
  }
}

function validate_email(field,alerttxt)
{
with(field)
{
apos=value.indexOf("@")
dotpos=value.lastIndexOf(".")
if (apos<1||dotpos-apos<2) 
  {alert(alerttxt);return false}
else
  {return true}
}
}

function validateForm()
{
  var x = document.forms["myForm"]["fname"].value;
  if (x == null || x == ""){
    alert("input yours name");
    return false;
  }
}
