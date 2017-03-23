<?php

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
if(isset($_GET['max'])) {
  $__max = $_GET['max'];
}
else {
  $__max = 2;
}
?>

$(document).ready(function() {
  id = <?=$_GET['id']?>;
  caching = '<?=$__caching?>'
  max = <?=$__max?>
  // Get the book
  $.ajax({url: "<?=$env['API_ROOT']?>/search",
              type: "POST",
              data: {"id": id, "type": "single", "caching": caching, "max": max},
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
                        $("#title").html($($(".title")[0]).html());
                        // Add footnotes for annotations
                        $(".chapter").each(function() {
                          var chapter = $(this),
                              title = $($(this).children("chapter-title")[0]).html(),
                              notes = $("<div></div>"),
                              number = 0;
                          notes.addClass("foot-notes");
                          chapter.find(".annotation").each(function() {
                            var word = $(this).html(),
                                data = $(this).attr("data-content"),
                                n = $("<a></a>");
                            $(this).append('<span class="note-number">[' + number + ']</span>')
                            n.addClass("note");
                            data = data.split(":");
                            data.splice(0, 1);
                            data = data.join(":");
                            n.html('<span class="word">[' + number + ']&nbsp;' + word + "</span>" + ":&nbsp;" + data);
                            notes.append(n);
                            number += 1;
                          });
                          chapter.append(notes);
                        });
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
