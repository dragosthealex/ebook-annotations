<?php

$header['title'] = 'Annotated eBook Reader';
include '../templates/header.php';
?>

<script>
$(document).ready(function() {
  id = <?=$_GET['id']?>;
  // Get the book
  $.ajax({url: "<?=$env['API_ROOT']?>/search",
              type: "POST",
              data: {"id": id, "type": "single"},
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
});
</script>
<?php
include '../templates/footer.php';
?>
