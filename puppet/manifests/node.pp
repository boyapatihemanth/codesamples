node default {
  case $::kernal {
    'Windows': {
      Exec {
        path => $::path
      }
    }
    default: {
      Exec {
        path => '/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin:/usr/local/sbin'
      }
    }
  }

  #Using Hiera to classify our nodes
  lookup('classes', Array[String], 'unique').include
}