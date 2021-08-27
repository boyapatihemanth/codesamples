class roles::developer {
  contain profiles::common::download_file
  contain profiles::install::packages
  contain profiles::postinstall::env

  Class['profiles::common::download_file']
  -> Class['profiles::install::packages']
  -> Class['profiles::postinstall::env']
}