<?php
include_once 'default.php';
?>
    </div>
  </body>
  <!-- Bootstrap -->
  <script
  src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'
  integrity='sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa'
  crossorigin='anonymous'></script>
  <script>
  $(document).ready(function() {
    $('#nav-search').submit(function(e) {
      e.preventDefault();
      window.location=("./?" + $(this).serialize());
      return;
    });
    <?php if(isset($_GET['query'], $_GET['source'])) {
    ?>
      search("<?=$_GET['source']?>", "<?=$_GET['query']?>");
    <?php
    }?>
    function search(source, query) {
      $.ajax({url: '<?=$env['API_ROOT']?>/search',
              type: 'POST',
              data: {"source": "web", "query": query},
              beforeSend: function(xhr) {
                $('#book-results').html("<span class='loading' id='loading'>Loading...</span>");
              },
              success: function(data, status, xhr) {
                        data = JSON.parse(data);
                        // Remove loading span
                        $('#loading').remove();
                        // For each id, add a nice link
                        for(i=0; i<data.length; i++) {
                          book = data[i];
                          if(book["title"].length > 100) {
                            el = '...';
                          } else {
                            el = '';
                          }
                          html = `<div class='col-md-6'>
                                    <div class='book-result'>
                                      <h2 class='result-title'>
                                        <a href='./book?id=${book["id"]}'>
                                          ${book["title"].substring(0, 100) + el}
                                        </a>
                                      </h2>
                                    </div>
                                  </div>`;
                          $("#book-results").append(html);
                        }

                      },
              error: function(xhr, status, error) {
                $('#main-content').html("<span class='error'>An error occurred: ' + error + '</span>");
              }
            });
      }
  });
  </script>
</html>
