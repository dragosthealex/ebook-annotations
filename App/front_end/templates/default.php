<?php
function replace_data($page, $key) {
  if(isset($$page) && isset($$page[$key])) {
    return $$page[$key];
  }
  return '';
}
