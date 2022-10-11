
// image upload section starts

$(document).ready(function() {
	
  var readURL = function(input) {
      if (input.files && input.files[0]) {
          var reader = new FileReader();

          reader.onload = function (e) {
              $('.profile-pic').attr('src', e.target.result);
          }
  
          reader.readAsDataURL(input.files[0]);
      }
  }
 
  $(".file-upload").on('change', function(){
      readURL(this);
  });
  
  $(".upload-button").on('click', function() {
     $(".file-upload").click();
  });
  
});
// image upload section ends



// filter section starts
$(document).ready(function(){
    $('.wonder').click(function(){
        var txt = "";
        $('.wonder:checked').each(function(){
            txt+=$(this).val()+','
        
        });
        $('#valuelist').val(txt);
    });
    

});


// filter section ends
