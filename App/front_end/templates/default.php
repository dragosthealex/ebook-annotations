<?php
// This File is included everywhere. Defining the globals here
$env = [];
$file = fopen('../.env', 'r');
while(($line = fgets($file)) !== false)
{
  $line = explode('=', trim($line));
  if(count($line) == 2)
  {
    // if we have key/value
    $env[$line[0]] = preg_replace("/\"/", '', $line[1]);
  }
}

// Replace data in files included
function replace_data($page, $key) {
  if(isset($$page) && isset($$page[$key])) {
    return $$page[$key];
  }
  return '';
}
