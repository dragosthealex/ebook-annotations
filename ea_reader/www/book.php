<?php

$header['title'] = 'Annotated eBook Reader';
include '../templates/header.php';
?>
<a name="top">&nbsp;</a>
<div class="top-link">
  <a class="btn btn-primary btn-round" href="#top">Top</a>
</div>
<div id="book"></div>
<script>
<?php
if(isset($_GET['c'])) {
  $__caching = $_GET['c'];
} else {
  $__caching = $env['CACHING'];
}
?>
$(document).ready(function() {
  id = <?=$_GET['id']?>;
  caching = '<?=$__caching?>'
  // Get the book
  $.ajax({url: "<?=$env['API_ROOT']?>/search",
              type: "POST",
              data: {"id": id, "type": "single", "caching": caching},
              beforeSend: function(xhr) {
                if(caching == 0 || caching == 2) {
                  $("#main-content #book").html("<span class='loading'>Annotating your book...</span>");
                } else {
                  $("#main-content #book").html("<span class='loading'>Loading...</span>");
                }
              },
              success: function(data, status, xhr) {
                        $("#main-content #book").html(data);
                        setTimeout(function(){
                          $(".annotation").popover({html: true});
                        },1000);
                      },
              error: function(xhr, status, error) {
                $("#main-content #book").html("<span class='error'>An error occurred: " + error + "</span>");
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
