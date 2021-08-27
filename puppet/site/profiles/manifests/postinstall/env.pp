class profiles::postinstall::env {
  $env_vars = lookup('developer::postinstall::path')
  create_resource('windows_env', $env_vars)
}