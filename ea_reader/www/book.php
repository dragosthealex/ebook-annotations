<?php

$header['title'] = 'Annotated eBook Reader';
include '../templates/header.php';
?>
<script>
$(document).ready(function() {
  id = <?=$_GET['id']?>;
  caching = '<?=$env['CACHING']?>'
  // Get the book
  $.ajax({url: "<?=$env['API_ROOT']?>/search",
              type: "POST",
              data: {"id": id, "type": "single", "caching": caching},
              beforeSend: function(xhr) {
                $("#main-content").html("<span class='loading'>Loading...</span>");
              },
              success: function(data, status, xhr) {
                        $("#main-content").html(data);
                        setTimeout(function(){
                          $(".annotation").popover({html: true});
                        },1000);
                      },
              error: function(xhr, status, error) {
                $("#main-content").html("<span class='error'>An error occurred: " + error + "</span>");
              }
              });
    $(document).click(function(e) {
      if(!$(e.target).hasClass("annotation")) {
        $(".annotation").popover("hide");
      }
    });
});
</script>
<?php
include '../templates/footer.php';
?>
