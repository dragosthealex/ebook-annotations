<?php
// Set time infinite
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
trim($query = get_post('query'));
$source = get_post('source');
$redirect_url = get_post('redirect_url');

if(!$query || !$source) {
  echo "Error: No query or source were provided.";
  exit();
}

switch ($source) {
  case 'web':
    // It means call came from web, so return the json
    $command = escapeshellcmd(PYTHON_COMMAND . ' search.py "' . $query . '"');
    echo(shell_exec($command));
    exit();
    break;

  default:
    # code...
    break;
}
?>
