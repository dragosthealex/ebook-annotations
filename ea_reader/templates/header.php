<?php
include_once 'default.php';
?>
<!DOCTYPE html>
<html>
  <head>
    <title><?=replace_data('header', 'title')?></title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap -->
    <link rel="stylesheet"
    href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
    integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
    crossorigin="anonymous">
    <link rel="stylesheet"
    href="./css/global.css">
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'></script>
  </head>
  <body>
    <header class="header">
      <nav class="navbar navbar-default">
        <div class="container">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#main-nav-collapse" aria-expanded="false">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="./">Home</a>
          </div>
          <div class="collapse navbar-collapse" id="main-nav-collapse">
            <ul class="nav navbar-nav">
              <!-- <li class="active"><a href="#">All Books <span class="sr-only">(current)</span></a></li> -->
              <?php
              if(isset($_GET['id'])) {
                // Means we are on book page
                $url="./book?id=" . $_GET['id'] . "&c=0";
              ?>
              <li class=""><a href="<?=$url?>">Reset cache</a></li>
              <?php                
              }
              ?>
            </ul>
            <form id="nav-search" class="navbar-form navbar-left" method="post" action="<?=$env['API_ROOT']?>/search">
              <div class="input-group">
                <input name="source" type="hidden" value="web">
                <input name="query" type="text" class="form-control" placeholder="Search">
                <div class="input-group-btn">
                  <button type="submit" class="btn btn-primary">Submit</button>
                </div>
              </div>
            </form>
          </ul>
        </div>
    </header>
    <div id="main-content" class="container main-content">
