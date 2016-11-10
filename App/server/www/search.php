<?php
function get_post($key) {
  if(isset($_POST[$key])) {
    return $_POST[$key];
  }
  return '';
}
strip($query = get_post('query'));
$source = get_post('source');
$redirect_url = get_post('redirect_url');

switch ($source) {
  case 'web':
    // It means call came from web, so return html
    $command = escapeshellcmd('python search.py "' . $query . '"');
    $output = shell_exec($command);
    break;

  default:
    # code...
    break;
}
?>
