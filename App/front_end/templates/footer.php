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
    $("#nav-search").submit(function() {
      $.post("<?=$env['API_ROOT']?>/search", $(this).serialize(), function(data) {
        $("#main-content").html(data);
      });
    });
  });
  </script>
</html>
