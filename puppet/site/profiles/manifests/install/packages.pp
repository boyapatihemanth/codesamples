class profiles::install::packages {
  $sw_install = lookup('developer::install::packages')
  create_resource('package', $sw_install)
}