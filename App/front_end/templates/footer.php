<?php
include_once 'default.php';
?>
    </div>
  </body>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <!-- Bootstrap -->
  <script
  src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
  integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa"
  crossorigin="anonymous"></script>
  <script>
  $(document).ready(function() {
    $("#nav-search").submit(function(e) {
      e.preventDefault();
      $.ajax({url: "<?=$env['API_ROOT']?>/search",
              type: "POST",
              data: $(this).serialize(),
              beforeSend: function(xhr) {
                $("#main-content").html("<span class='loading'>Loading...</span>");
              },
              success: function(data, status, xhr) {
                        $("#main-content").html(data);
                      },
              error: function(xhr, status, error) {
                $("#main-content").html("<span class='error'>An error occurred: " + error + "</span>");
              }
              });
    });
  });
  </script>
</html>
