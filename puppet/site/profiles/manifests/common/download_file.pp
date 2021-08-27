class profiles::common::download_file {
  $downloadpath = lookup('common::downloadpath')

  $downloadurl = lookup( { 'name' => 'developer::file::url',
                           'merge' => {
                             'strategy' => 'hash',
                           },
                        } )
  $downloadzip = lookup( { 'name' => 'developer::zip::url',
                           'merge' => {
                             'strategy' => 'hash',
                           },
                        } )
  file {"${downloadpath}":
    ensure => 'directory'
  }

  $downloadurl.each |$name, $url| {
    file {"${downloadpath}/${name}":
      source => "${url}",
    }
  }

  $downloadzip.each |$name, $url| {
    file {"${downloadpath}/${name}":
      source => "${url}",
    }
    unzip { "${name}":
      source => "${downloadpath}/${name}",
      creates => "${downloadpath}/Click",
      destination => "${downloadpath}"
    }
  }
}