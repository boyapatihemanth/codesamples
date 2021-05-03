Param (
    [Parameter(Mandatory=$True)] [String] $Role
    [Parameter(Mandatory=$False)] [String] $Test = $False
    [Parameter(Mandatory=$False)] [String] $Directory = $pwd
)

Set-Location -Path $Directory

$PUPPET_RUBY_DIR = "C:\Program Files\Puppet Labs\Puppet\sys\ruby\bin"
$GEM_BIN = Join-Path $PUPPET_RUBY_DIR "gem"

& $GEM_BIN install librarian-puppet --no-ri --no-rdoc
& librarian-puppet install --no-use-v1-api

if ($Role -eq "") {
    echo "Role param cannot be empty, currently avalable option is 'developer'"
    exit 1
} else {
    $env:FACTER_role = $Role
}

if ($Test -eq $True) {
    $NoOp = "--noop"
} else {
    $NoOp = ""
}

puppet apply .\manifests\node.pp --modulepath=".\site\;.\modules\" --hiera_config=".\hiera.yaml" $NoOp --verbose --logdest "C:\puppet-apply.log" --logdest console