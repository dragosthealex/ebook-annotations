<?php
set_time_limit (0);
// Includes
include('config.php');

// Get a post variable
function get_post($key) {
  if(isset($_POST[$key])) {
    return $_POST[$key];
  }
  return '';
}
// If single
if(get_post('type') == 'single') {
  $id = trim(get_post('id'));
  // Caching
  $c = get_post('c')?get_post('c'):0;
  if(!in_array($c, [0,1,2,3])) {
    $c = 0;
  }
  $command = escapeshellcmd(PYTHON_COMMAND . ' search.py single "' . $id . '" -c ' . $c);
  echo(shell_exec($command));
  exit();
} else {
  $query = trim(get_post('query'));
  $source = get_post('source');
  $redirect_url = get_post('redirect_url');

  if(!$query || !$source) {
    echo "Error: No query or source were provided.";
    exit();
  }

  switch ($source) {
    case 'web':
      // Caching
      $c = get_post('c')?get_post('c'):0;
      // It means call came from web, so return the json
      $command = escapeshellcmd(PYTHON_COMMAND . ' search.py all "' . $query . '" -c ' . $c);
      echo(shell_exec($command));
      exit();
      break;

    default:
      # code...
      break;
  }
}
?>
