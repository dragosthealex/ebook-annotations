<?php

include '../templates/header.php';
?>
<div class="row" id="book-results">
  <div class="panel panel-default">
    <div class="panel-heading">
      <h2>Welcome to EbookAnnotations</h2>
    </div>
    <div class="panel-body">
      <p>
        Use the search box to search for any book by title. Please be advised that
        annotations currently work only for the first chapter, on the English books.
      </p>
      <h3>Demos</h3>
      <a class="btn btn-lg btn-primary"
         href="./book?id=11&c=3&max=0"
         target="_blank">Alice, full, cached</a>
      <a class="btn btn-lg btn-primary"
         href="./book?id=74&c=0&max=2"
         target="_blank">Tom sawyer, first 2, no cache</a>
      <a class="btn btn-lg btn-primary"
         href="./book?id=74&c=2&max=2"
         target="_blank">Tom sawyer, first 2, cached anns</a>
      <a class="btn btn-lg btn-primary"
         href="./book?id=174&c=3&max=2"
         target="_blank">Dorian Gray, first 2, cached</a>
      <a class="btn btn-lg btn-primary"
         href="./book?id=1301&c=3&max=5"
         target="_blank">French Revolution, first 2, cached</a>
    </div>
  </div>
</div>
<?php
include '../templates/footer.php';
?>
