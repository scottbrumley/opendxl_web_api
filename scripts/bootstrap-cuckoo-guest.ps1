# To run this file you will need to open Powershell as administrator and first run:
# Set-ExecutionPolicy Unrestricted
# Then source this script by running:
# . .\install_python.ps1

$save_dir=Resolve-Path $home/tmp
$project_dir = "C:\Projects"
$virtualenv_dir = $project_dir + "\virtualenvs"

$client = New-Object System.Net.WebClient

function InstallPythonMSI($installer) {
	$Arguments = @()
	$Arguments += "/i"
	$Arguments += "`"$installer`""
	$Arguments += "ALLUSERS=`"1`""
	$Arguments += "/passive"

	Start-Process "msiexec.exe" -ArgumentList $Arguments -Wait
}

function download_file([string]$url, [string]$d) {
	# Downloads a file if it doesn't already exist
	if(!(Test-Path $d -pathType leaf)) {
		# get the file
		write-host "Downloading $url to $d";
		$client.DownloadFile($url, $d);
	}
}

function get-python-ver($version) {
	# Download Python indicated by version. For example:
	#  > get-python-ver 3.4.0rc1
	# or
	#  > get-python-ver 2.7.6

	$filename = 'python-' + $version + '.amd64.msi';
	$save_path = '' + $save_dir + '\' + $filename;
	if(!(Test-Path -pathType container $save_dir)) {
		write-host -fore red $save_dir " does not exist";
		exit;
	}

	$url = 'http://www.python.org/ftp/python/' + $version.Substring(0,5) + '/' + $filename;
	download-file $url $save_path
	write-host "Installing Python"
	InstallPythonMSI $save_path $target_dir

	write-host "Add Python to the PATH"
	[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")
}

function get_setuptools {
	write-host "Installing setuptools"
	$setuptools_url = "https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py"
	$ez_setup = '' + $save_dir + "\ez_setup.py"
	download_file $setuptools_url $ez_setup
	python $ez_setup
}

function get_pip {
	write-host "Installing pip"
	$setuptools_url = "https://raw.github.com/pypa/pip/master/contrib/get-pip.py"
	$get_pip = '' + $save_dir + "\get_pip.py"
	download_file $setuptools_url $get_pip
	python $get_pip
}

function get_virtualenv {
	write-host "Installing virtualenv"
	pip install virtualenv
	pip install virtualenvwrapper-win C:\Projects\virtualenvs
	[Environment]::SetEnvironmentVariable("WORKON_HOME", "C:\Projects\virtualenvs\", "User")
}

function get_git {
	write-host "Installing git"
	$url = "https://msysgit.googlecode.com/files/Git-1.8.5.2-preview20131230.exe"
	$dest = '' + $save_dir + "\Git-1.8.5.2-preview20131230.exe"
	download_file $url $dest
	Start-Process $dest -ArgumentList "/silent" -Wait
	[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Program Files (x86)\Git\bin\", "User")
}

function create_directories {
	write-host "Creating directories"
	New-Item -ItemType directory -Path $project_dir
	New-Item -ItemType directory -Path $virtualenv_dir
}

function upgrade_pip($virtualenv) {
	$scripts = $virtualenv_dir + "\" + $virtualenv + "\Scripts\"
	$activate = $scripts + "activate.ps1"
	. $activate
	get_setuptools
	get_pip
}

function install_pywin32($virtualenv) {
	$url = "http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20218/pywin32-218.win32-py2.7.exe"
	$dest = '' + $save_dir + "pywin32-218.win32-py2.7.exe"
	download_file $url $dest

	$scripts = $virtualenv_dir + "\" + $virtualenv + "\Scripts\"
	$activate = $scripts + "activate.ps1"
	. $activate
	easy_install $dest
}