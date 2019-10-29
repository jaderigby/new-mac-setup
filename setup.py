#!/usr/bin/python

import os, subprocess, re, sys

import CustomInstallList

def main():
    try:
        action = str(sys.argv[1])
    except:
        action = None

    if action != None:
        s = ""
        sys.argv = sys.argv[1:]
        length = len(sys.argv)
        for index, elem in enumerate(sys.argv):
            if index + 1 == length:
                s += elem
            else:
                s += elem + ", "
    else:
        s = action
    print
    print "Actions: {}".format(s)
    print

    divider = "============================================================="

    def read_file(FILEPATH):
    	FILE = open(FILEPATH, 'r')
    	data = FILE.read()
    	FILE.close()
    	return data

    def write_file(FILEPATH, DATA):
    	FILE = open(FILEPATH, 'w')
    	FILE.write(DATA)
    	FILE.close()

    def verify_file(FILEPATH, VERIFY_STRING, CONFIRM_MESSAGE, ALERT_MESSAGE):
        if not os.path.exists(FILEPATH):
            write_file(FILEPATH, VERIFY_STRING)
            print("\t\t- {}".format(CONFIRM_MESSAGE))
            print("")
        elif os.path.exists(FILEPATH):
            data = read_file(FILEPATH)
            pat = re.escape(VERIFY_STRING)
            match = re.search(pat, data)
            if not match:
                write_file(FILEPATH, data + '\n' + VERIFY_STRING)
                print("\t\t- {}".format(CONFIRM_MESSAGE))
                print("")
            else:
                print("\t\t- {}!".format(ALERT_MESSAGE))
                print("")

    def handle_executable():
        base = os.path.expanduser('~')
        if not os.path.exists(base + '/Documents/new-mac-setup'):
            subprocess_cmd('cd {}/Documents && git clone https://github.com/jaderigby/new-mac-setup.git'.format(base))
        print("-- Making setup file executable --")
        alias = '''
    export PATH={}/Documents/new-mac-setup:$PATH
    '''.format(base)
        if (os.path.exists(base + '/.bash_profile')):
            FILE = open(base + '/.bash_profile', 'r')
            data = FILE.read()
            FILE.close()
        else:
            FILE = open(base + '/.bash_profile', 'w')
            FILE.close()
            data = ""
        pat = re.escape(alias)
        match = re.search(pat, data)
        if match:
            print("")
            print("\t- path variable already set!")
        else:
            print("\t- path variable for executable is set")
            FILE = open(base + '/.bash_profile', 'w')
            data += alias
            FILE.write(data)
            FILE.close()
        # check if file is already executable
        p = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        selection = None

        def find_setup_file(ELEM):
            print("ELEM: " + ELEM)
            result = re.search('setup\.py', ELEM).group()
            print("result: " + result)
            return True

        executable = False
        for line in out.split('\n'):
            if 'setup.py' in line:
                if '-x' in line:
                    executable = True

        if executable:
            print("\t- permissions for setup file already set!")
        else:
            subprocess.call(['chmod', '+x', 'setup.py'])
            print("\t- permissions for setup file set")
        print("")
        print(divider)

    def subprocess_cmd(command):
        process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        print proc_stdout

    def handle_aliases():
        base = os.path.expanduser('~')
        snippet = '''# Show hidden files in Finder
alias showhidden="defaults write com.apple.finder AppleShowAllFiles TRUE && killall Finder"
# Hide hidden files in Finder
alias hidehidden="defaults write com.apple.finder AppleShowAllFiles FALSE && killall Finder"'''
        verify_file(base + '/.bash_profile', snippet, 'Aliases are set', 'Aliases already set')

    def handle_br_aliases():
        base = os.path.expanduser('~')
        snippet = '''jira_branch_func() {
  newBranch=$1
  git fetch origin
  git branch -v -a
  git checkout --track origin/$newBranch
}

alias jira-branch="jira_branch_func"

source ~/Documents/bash-tools/.bashrc
'''
        verify_file(base + '/.bash_profile', snippet, 'Aliases are set', 'Aliases already set')

    def handle_homebrew():
        print("Installing Homebrew ...")
        print('if you have problems, please install Homebrew manually by running the following command: \n/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
        if verify_installation('brew --version') != True:
            subprocess_cmd('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
            subprocess_cmd('brew update')
        subprocess_cmd('brew doctor')
        # pathVariable = 'export PATH="/usr/local/bin:$PATH"'

    def verify_installation(CMD):
        result  = False
        if CMD != None:
            process = subprocess.Popen(CMD, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            out, err = process.communicate()

            for line in out.splitlines():
                if not "command not found" in line:
                    result = True

        return result

    def handle_installs():
        installDict = [
            {
                "name" : "Caskroom"
              , "verify" : "brew info cask"
              , "cmd" : "brew tap caskroom/cask"
            }
            ,{
                  "name" : "Git"
                , "verify" : "git --version"
                , "cmd" : "brew install git"
            }
            ,{
                  "name" : "Node"
                , "verify" : "node --version"
                , "cmd" : "brew install node"
            }
            ,{
                  "name" : "Atom"
                , "verify" : "ls /Applications/ | grep -w Atom"
                , "cmd" : "brew cask install atom"
            }
            ,{
                  "name" : "iTerm"
                , "verify" : "ls /Applications/ | grep -w iTerm"
                , "cmd" : "brew cask install iterm2"
            }
            ,{
                  "name" : "Dropbox"
                , "verify" : "ls /Applications/ | grep -w Dropbox"
                , "cmd" : "brew cask install dropbox"
            }
            ,{
                  "name" : "Slack"
                , "verify" : "ls /Applications/ | grep -w Slack"
                , "cmd" : "brew cask install slack"
            }
            ,{
                  "name" : "Inkscape"
                , "verify" : "ls /Applications/ | grep -w Inkscape"
                , "cmd" : "brew cask install inkscape"
            }
            ,{
                  "name" : "Blender"
                , "verify" : "ls /Applications/ | grep -w Blender"
                , "cmd" : "brew cask install blender"
            }
            ,{
                  "name" : "ImageMagick"
                , "verify" : "convert -version"
                , "cmd" : "brew install imagemagick"
            }
            ,{
                  "name" : "Spotify"
                , "verify" : "ls /Applications/ | grep -w Spotify"
                , "cmd" : "brew cask install spotify"
            }
            ,{
                  "name" : "Chrome"
                , "verify" : "ls /Applications/ | grep -w Chrome"
                , "cmd" : "brew cask install google-chrome"
            }
            ,{
                  "name" : "Firefox"
                , "verify" : "ls /Applications/ | grep -w Firefox"
                , "cmd" : "brew cask install firefox"
            }
            ,{
                  "name" : "ImageAlpha"
                , "verify" : "ls /Applications/ | grep -w ImageAlpha"
                , "cmd" : "brew cask install imagealpha"
            }
            ,{
                  "name" : "Astropad Studio"
                , "verify" : "ls /Applications/ | grep -w Astropad Studio"
                , "cmd" : "brew cask install astropad-studio"
            }
            ,{
                  "name" : "Kaleidoscope"
                , "verify" : "ls /Applications/ | grep -w Kaleidoscope"
                , "cmd" : "brew cask install kaleidoscope"
            }
            ,{
                  "name" : "XQuartz"
                , "verify" : "ls /Applications/Utilities/ | grep -w XQuartz"
                , "cmd" : "brew cask install xquartz"
            }
            # ,{
            #       "name" : "Affinity Designer"
            #     , "verify" : "ls /Applications/ | grep -w 'Affinity Designer'"
            #     , "cmd" : "brew cask install affinity-designer"
            # }
        ]

        installed = []
        for item in installDict:
            if verify_installation(item['verify']) != True:
                print("installing {}...".format(item['name']))
                subprocess_cmd(item['cmd'])
                installed.append(item['name'])
        if len(installed) > 0:
            print("")
            print("The following items were installed: ")
            print("")
            for item in installed:
                print "- {}".format(item)

    def handle_installs_as_list():
        installDict = {
                "Caskroom" : {
                    "name" : "Caskroom"
                    , "verify" : "brew info cask"
                    , "cmd" : "brew tap caskroom/cask"
                }
                , "Git" : {
                    "name" : "Git"
                    , "verify" : "git --version"
                    , "cmd" : "brew install git"
                }
                , "Node" : {
                    "name" : "Node"
                    , "verify" : "node --version"
                    , "cmd" : "brew install node"
                }
                , "Atom" : {
                    "name" : "Atom"
                    , "verify" : "ls /Applications/ | grep -w Atom"
                    , "cmd" : "brew cask install atom"
                }
                , "iTerm" : {
                    "name" : "iTerm"
                    , "verify" : "ls /Applications/ | grep -w iTerm"
                    , "cmd" : "brew cask install iterm2"
                }
                , "Dropbox" : {
                    "name" : "Dropbox"
                    , "verify" : "ls /Applications/ | grep -w Dropbox"
                    , "cmd" : "brew cask install dropbox"
                }
                , "Slack" : {
                    "name" : "Slack"
                    , "verify" : "ls /Applications/ | grep -w Slack"
                    , "cmd" : "brew cask install slack"
                }
                , "Inkscape" : {
                    "name" : "Inkscape"
                    , "verify" : "ls /Applications/ | grep -w Inkscape"
                    , "cmd" : "brew cask install inkscape"
                }
                , "Blender" : {
                    "name" : "Blender"
                    , "verify" : "ls /Applications/ | grep -w Blender"
                    , "cmd" : "brew cask install blender"
                }
                , "ImageMagick" : {
                    "name" : "ImageMagick"
                    , "verify" : "convert -version"
                    , "cmd" : "brew install imagemagick"
                }
                , "Spotify" : {
                    "name" : "Spotify"
                    , "verify" : "ls /Applications/ | grep -w Spotify"
                    , "cmd" : "brew cask install spotify"
                }
                , "Chrome" : {
                    "name" : "Chrome"
                    , "verify" : "ls /Applications/ | grep -w Chrome"
                    , "cmd" : "brew cask install google-chrome"
                }
                , "Firefox" : {
                    "name" : "Firefox"
                    , "verify" : "ls /Applications/ | grep -w Firefox"
                    , "cmd" : "brew cask install firefox"
                }
                , "ImageAlpha" : {
                    "name" : "ImageAlpha"
                    , "verify" : "ls /Applications/ | grep -w ImageAlpha"
                    , "cmd" : "brew cask install imagealpha"
                }
                , "Kaleidoscope" : {
                    "name" : "Kaleidoscope"
                    , "verify" : "ls /Applications/ | grep -w Kaleidoscope"
                    , "cmd" : "brew cask install kaleidoscope"
                }
                , "MAMP" : {
                    "name" : "MAMP"
                    , "verify" : "ls /Applications/ | grep -w MAMP"
                    , "cmd" : "brew cask install mamp"
                }
                , "ffmpeg" : {
                    "name" : "ffmpeg"
                    , "verify" : "ffmpeg -version"
                    , "cmd" : "brew cask install ffmpeg"
                }
                , "FileZilla" : {
                    "name" : "FileZilla"
                    , "verify" : "ls /Applications/ | grep -w FileZilla"
                    , "cmd" : "brew cask install filezilla"
                }
                , "XQuartz" : {
                    "name" : "XQuartz"
                    , "verify" : "ls /Applications/Utilities/ | grep -w XQuartz"
                    , "cmd" : "brew cask install xquartz"
                }
            }

        installed = []
        customList = CustomInstallList.execute()
        for item in customList:
            currObj = installDict[item]
            if verify_installation(currObj['verify']) != True:
                print("installing {}...".format(currObj['name']))
                # subprocess_cmd(currObj['cmd'])
                installed.append(currObj['name'])
        if len(installed) > 0:
            print("")
            print("The following items were installed: ")
            print("")
            for item in installed:
                print "- {}".format(item)

    def install_atom_package(PACKAGE):
        base = os.path.expanduser('~')
        print("")
        print('\t- Checking -- "{}":'.format(PACKAGE))
        print("")
        if os.path.exists('{}/.atom/packages/{}'.format(base, PACKAGE)):
            print("\t\t- Package already set!")
        else:
            subprocess_cmd('apm install {}'.format(PACKAGE))

    def handle_atom_customization():
        base = os.path.expanduser('~')
        print("-- Atom: Adding User Packages --")
        install_atom_package('platformio-ide-terminal')
        install_atom_package('emmet')
        install_atom_package('stylus-language')
        install_atom_package('pigments')
        install_atom_package('language-pug')
        print("")
        print("-- Atom: Setting Soft Wrap --")
        pat = re.escape(''' editor:
    softWrap: true''')
        FILE = open(base + '/.atom/config.cson', 'r')
        data = FILE.read()
        FILE.close()
        match = re.search(pat, data)
        if not match:
            print("")
            print("\t- Soft Wrap is set")
            print("")
            data = data.replace(''' editor:''', ''' editor:
    softWrap: true''')
            print("FILE: ")
            print("-------------------------------------------------------------")
            print("")
            print(data)
            FILE = open(base + '/.atom/config.cson', 'w')
            FILE.write(data)
            FILE.close()
        else:
            print("")
            print("\t- Soft Wrap already set!")
            print("")

    def handle_atom_snippets():
        base = os.path.expanduser('~')
        FILE = open(base + '/.atom/snippets.cson', 'r')
        data = FILE.read()
        FILE.close()
        FILE = open(base + '/.atom/snippets.cson', 'w')
        snip = ''''.text.html.basic':
  'markdown-html blueprint':
    'prefix': 'html-mark'
    'body': """<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<!-- <link rel="stylesheet" type="text/css" href="your/filepath/here" /> -->
		<!-- <link rel="shortcut icon" href="favicon.ico" type="image/x-icon" /> -->
		<style type="text/css">
			* {
				margin: 0;
				padding: 0;
				font-size: 100%;
			}
			h1 {
				font-size: 3.2rem;
			}
			h2 {
				font-size: 2.8rem;
			}
			h3 {
				font-size: 2.4rem;
			}
			h4 {
				font-size: 2rem
			}
			h5 {
				font-size: 1.6rem;
			}
			h6 {
				font-size: 1.2rem;
			}
			body {
				background-color: #444;
			}
			#container {
				margin: 0 auto 30px;
				padding: 0 30px 30px;
				width: 960px;
				min-height: 500px;
				background-color: #fff;
				border-radius: 0 0 8px 8px;
				box-shadow: 0 0 35px rgba(0,0,0,0.5);
				font-family: arial, verdana, sans-serif;
			}
			.centerize {
				position: absolute;
				margin: auto;
				top: 0;
				right: 0;
				bottom: 0;
				left: 0
			}
			.cf:after {
				content: " ";
				display: table;
				clear: both;
			}
			#container ul, #container ol {
				margin-top: 25px;
				margin-bottom: 25px;
				margin-left: 25px;
			}
			p {
				margin-top: 25px;
				margin-bottom: 25px;
			}
			.title {
				margin: 0 -30px 60px;
				padding: 30px;
				/* text-align: center; */
				font-size: 3rem;
				background-color: #b5d0c4;
			}
			.thirds > aside img, .fifths > aside img, .sevenths > aside img {
				width: 100%;
				height: auto;
			}
			.thirds {
				display: flex;
				flex-direction: row;
				flex-wrap: nowrap;
				align-items: stretch;
			}
			.thirds > aside {
				width: calc(33.5% - 12.5px);
			}
			.thirds > article {
				width: calc(66.5% - 12.5px);
			}
			.thirds > aside + article {
				margin-left: 25px;
			}
			.thirds > article + aside {
				margin-right: 25px;
			}
			.thirds, .fifths, .sevenths {
				display: flex;
				flex-direction: row;
				flex-wrap: nowrap;
				align-items: stretch;
			}
			.fifths > aside {
				width: calc(40% - 12.5px);
			}
			.fifths > article {
				width: calc(60% - 12.5px);
			}
			.fifths > aside + article {
				margin-left: 25px;
			}
			.fifths > article + aside {
				margin-right: 25px;
			}
			.sevenths > aside {
				width: calc(28% - 12.5px);
			}
			.sevenths > article {
				width: calc(72% - 12.5px);
			}
			.sevenths > aside + article {
				margin-left: 25px;
			}
			.sevenths > article + aside {
				margin-right: 25px;
			}
			.thirds aside.single {
				width: calc(17% - 12.5px);
			}
			.thirds aside.single + article {
				width: calc(83% - 12.5px);
			}
			.fifths aside.single {
				width: calc(20% - 12.5px);
			}
			.fifths aside.single + article {
				width: calc(80% - 12.5px);
			}
			.sevenths aside.single {
				width: calc(14% - 12.5px);
			}
			.sevenths aside.single + article {
				width: calc(86% - 12.5px);
			}
			aside img {
				margin-top: 25px;
				padding: 5px;
				box-shadow: 0 0 20px rgba(0,0,0,0.3);
			}
			hr {
				border: 1px solid #bfbfbf;
			}
			section {
				margin-bottom: 40px;
			}
		</style>
		<title>My Site</title>
	</head>
	<body>
		<div id="container">
			<div class="title">My Site</div>

		</div>
	</body>
</html>
"""
  'Instructions for Custom Snippets':
    'prefix': 'guide'
    'body': """# Instructions: #

- HTML template: [html-mark]
-

"""
  'panels':
    'prefix': 'panel'
    'body': """<panel-wrapper>
\t<panel-inner>
\t\t$1
\t</panel-inner>
</panel-wrapper>"""
  'half':
    'prefix': 'half'
    'body': """<segment-elem class="half">
\t<x-cell>$1</x-cell>
\t<x-cell>$2</x-cell>
</segment-elem>"""
  'thirds':
    'prefix': 'thirds'
    'body': """<segment-elem class="thirds">
\t<x-minor>$1</x-minor>
\t<x-major>$2</x-major>
</segment-elem>"""
  'thirds columns':
    'prefix': 'thirds-cell'
    'body': """<segment-elem class="thirds">
\t<x-cell>$1</x-cell>
\t<x-cell>$2</x-cell>
\t<x-cell>$3</x-cell>
</segment-elem>"""
  'fourths':
    'prefix': 'fourths'
    'body': """<segment-elem class="fourths">
\t<x-cell>$1</x-cell>
\t<x-cell>$2</x-cell>
\t<x-cell>$3</x-cell>
\t<x-cell>$4</x-cell>
</segment-elem>"""
  'fifths':
    'prefix': 'fifths'
    'body': """<segment-elem class="fifths">
\t<x-minor>$1</x-minor>
\t<x-major>$2</x-major>
</segment-elem>"""
  'fifths columns':
    'prefix': 'fifths-cell'
    'body': """<segment-elem class="fifths">
\t<x-cell>$1</x-cell>
\t<x-cell>$2</x-cell>
\t<x-cell>$3</x-cell>
\t<x-cell>$4</x-cell>
\t<x-cell>$5</x-cell>
</segment-elem>"""
  'sixths':
    'prefix': 'sixths'
    'body': """<segment-elem class="sixths">
\t<x-cell>$1</x-cell>
\t<x-cell>$2</x-cell>
\t<x-cell>$3</x-cell>
\t<x-cell>$4</x-cell>
\t<x-cell>$5</x-cell>
\t<x-cell>$6</x-cell>
</segment-elem>"""
  'sevenths':
    'prefix': 'sevenths'
    'body': """<segment-elem class="sevenths">
\t<x-minor>$1</x-minor>
\t<x-major>$2</x-major>
</segment-elem>"""
  'sevenths columns':
    'prefix': 'sevenths-cell'
    'body': """<segment-elem class="sevenths">
\t<x-cell>$1</x-cell>
\t<x-cell>$2</x-cell>
\t<x-cell>$3</x-cell>
\t<x-cell>$4</x-cell>
\t<x-cell>$5</x-cell>
\t<x-cell>$6</x-cell>
\t<x-cell>$7</x-cell>
</segment-elem>"""
  'html blueprint':
    'prefix': 'html-seg'
    'body': """<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <!-- <link rel="stylesheet" type="text/css" href="your/filepath/here" /> -->
    <!-- <link rel="shortcut icon" href="favicon.ico" type="image/x-icon" /> -->
    <style type="text/css">
      * {
        margin: 0;
        padding: 0;
        font-size: 100%;
      }
      h1 {
        font-size: 3.2rem;
      }
      h2 {
        font-size: 2.8rem;
      }
      h3 {
        font-size: 2.4rem;
      }
      h4 {
        font-size: 2rem
      }
      h5 {
        font-size: 1.6rem;
      }
      h6 {
        font-size: 1.2rem;
      }
      body {
        background-color: #444;
      }
      #container {
        margin: 0 auto 30px;
        padding: 0 30px 30px;
        width: 960px;
        min-height: 500px;
        background-color: #fff;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 0 35px rgba(0,0,0,0.5);
        font-family: arial, verdana, sans-serif;
      }
      .centerize {
        position: absolute;
        margin: auto;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0
      }
      .cf:after {
        content: " ";
        display: table;
        clear: both;
      }
      #container ul, #container ol {
        margin-top: 25px;
        margin-bottom: 25px;
        margin-left: 25px;
      }
      p {
        margin-top: 25px;
        margin-bottom: 25px;
      }
      .title {
        margin: 0 -30px 60px;
        padding: 30px;
        /* text-align: center; */
        font-size: 3rem;
        background-color: #b5d0c4;
      }
      hr {
        border: 1px solid #bfbfbf;
      }
    </style>
    <style type="text/css">
      panel-wrapper,
      panel-inner,
      x-minor,
      x-major,
      x-cell {
        display: block;
      }

      panel-wrapper panel-inner {
        margin: 0 auto;
        padding: 60px 0;
        width: 1200px;
      }

      segment-elem {
        display: flex;
        flex-flow: row wrap;
      }

      prime-segment {
        display: flex;
        flex-flow: row nowrap;
      }

      prime-segment > aside {
        flex-shrink: 0;
      }

      prime-segment > article {
        flex-grow: 1;
      }

      x-minor,
      x-major,
      x-cell
       {
        flex-grow: 0;
        flex-shrink: 0;
      }

      .stack > x-minor:nth-child(1n),
      .stack > x-major:nth-child(1n),
      .stack > x-cell:nth-child(1n),
      .half > x-minor:nth-child(1n),
      .half > x-major:nth-child(1n),
      .half > x-cell:nth-child(1n),
      .half > x-minor:nth-child(2n),
      .half > x-major:nth-child(2n),
      .half > x-cell:nth-child(2n),
      .thirds > x-minor:nth-child(1n),
      .thirds > x-major:nth-child(1n),
      .thirds > x-cell:nth-child(1n),
      .fourths > x-minor:nth-child(1n),
      .fourths > x-major:nth-child(1n),
      .fourths > x-cell:nth-child(1n),
      .fourths.major-in-the-middle > x-minor:nth-child(1n),
      .fourths.major-in-the-middle > x-major:nth-child(1n),
      .fifths > x-minor:nth-child(1n),
      .fifths > x-major:nth-child(1n),
      .fifths > x-cell:nth-child(1n),
      .fifths.major-in-the-middle > x-minor:nth-child(1n),
      .fifths.major-in-the-middle > x-major:nth-child(1n),
      .sixths > x-cell:nth-child(1n),
      .sevenths > x-minor:nth-child(1n),
      .sevenths > x-major:nth-child(1n),
      .sevenths > x-cell:nth-child(1n),
      prime-segment > aside:nth-child(1n),
      prime-segment > article:nth-child(1n) {
        margin-right: 15px;
        margin-left: 0;
      }

      .stack > x-minor:last-child,
      .stack > x-major:last-child,
      .stack > x-cell:last-child,
      .half > x-minor:last-child,
      .half > x-major:last-child,
      .half > x-cell:last-child,
      .thirds > x-minor:last-child,
      .thirds > x-major:last-child,
      .thirds > x-cell:last-child,
      .fourths > x-minor:last-child,
      .fourths > x-major:last-child,
      .fourths > x-cell:last-child,
      .fourths.major-in-the-middle > x-minor:last-child,
      .fourths.major-in-the-middle > x-major:last-child,
      .fifths > x-minor:last-child,
      .fifths > x-major:last-child,
      .fifths > x-cell:last-child,
      .fifths.major-in-the-middle > x-minor:last-child,
      .fifths.major-in-the-middle > x-major:last-child,
      .sixths > x-cell:last-child,
      .sevenths > x-minor:last-child,
      .sevenths > x-major:last-child,
      .sevenths > .cell:last-child,
      prime-segment > aside:last-child,
      prime-segment > article:last-child {
        margin-right: 0;
      }

      .stack > x-minor:nth-child(1n),
      .stack > x-major:nth-child(1n),
      .stack > x-cell:nth-child(1n),
      .half > x-minor:nth-child(2n),
      .half > x-major:nth-child(2n),
      .half > x-cell:nth-child(2n),
      .thirds > x-minor:nth-child(3n),
      .thirds > x-major:nth-child(3n),
      .thirds > x-cell:nth-child(3n),
      .fourths > x-minor:nth-child(4n),
      .fourths > x-major:nth-child(4n),
      .fourths > x-cell:nth-child(4n),
      .fourths.major-in-the-middle > x-minor:nth-child(4n),
      .fourths.major-in-the-middle > x-major:nth-child(4n),
      .fifths > x-minor:nth-child(5n),
      .fifths > x-major:nth-child(5n),
      .fifths > x-cell:nth-child(5n),
      .fifths.major-in-the-middle > x-minor:nth-child(5n),
      .fifths.major-in-the-middle > x-major:nth-child(5n),
      .sixths > x-cell:nth-child(6n),
      .sevenths > x-minor:nth-child(7n),
      .sevenths > x-major:nth-child(7n),
      .sevenths > x-cell:nth-child(7n),
      prime-segment > aside:nth-child(2n),
      prime-segment > article:nth-child(2n) {
        margin-right: 0;
        margin-left: auto;
      }

      .stack > x-minor,
      .stack > x-major,
      .stack > x-cell {
        flex-basis: calc(99.98% * 1/1 - (15px - 15px * 1/1));
        max-width: calc(99.98% * 1/1 - (15px - 15px * 1/1));
        width: calc(99.98% * 1/1 - (15px - 15px * 1/1));
      }

      .half > x-minor,
      .half > x-major,
      .half > x-cell,
      .fourths.major-in-the-middle > x-major {
        flex-basis: calc(99.98% * 1/2 - (15px - 15px * 1/2));
        max-width: calc(99.98% * 1/2 - (15px - 15px * 1/2));
        width: calc(99.98% * 1/2 - (15px - 15px * 1/2));
      }

      .thirds > x-minor,
      .thirds > x-cell,
      .thirds.major-in-the-middle > x-minor,
      .thirds.major-in-the-middle > x-major {
        flex-basis: calc(99.98% * 1/3 - (15px - 15px * 1/3));
        max-width: calc(99.98% * 1/3 - (15px - 15px * 1/3));
        width: calc(99.98% * 1/3 - (15px - 15px * 1/3));
      }

      .thirds > x-major {
        flex-basis: calc(99.98% * 2/3 - (15px - 15px * 2/3));
        max-width: calc(99.98% * 2/3 - (15px - 15px * 2/3));
        width: calc(99.98% * 2/3 - (15px - 15px * 2/3));
      }

      .fourths > x-cell,
      .fourths.major-in-the-middle > x-minor {
        flex-basis: calc(99.98% * 1/4 - (15px - 15px * 1/4));
        max-width: calc(99.98% * 1/4 - (15px - 15px * 1/4));
        width: calc(99.98% * 1/4 - (15px - 15px * 1/4));
      }

      .fifths > x-minor {
        flex-basis: calc(99.98% * 5/13 - (15px - 15px * 5/13));
        max-width: calc(99.98% * 5/13 - (15px - 15px * 5/13));
        width: calc(99.98% * 5/13 - (15px - 15px * 5/13));
      }

      .fifths > x-major {
        flex-basis: calc(99.98% * 8/13 - (15px - 15px * 8/13));
        max-width: calc(99.98% * 8/13 - (15px - 15px * 8/13));
        width: calc(99.98% * 8/13 - (15px - 15px * 8/13));
      }

      .fifths.true > x-minor {
        flex-basis: calc(99.98% * 2/5 - (15px - 15px * 2/5));
        max-width: calc(99.98% * 2/5 - (15px - 15px * 2/5));
        width: calc(99.98% * 2/5 - (15px - 15px * 2/5));
      }

      .fifths.true > x-major,
      .fifths.major-in-the-middle > x-major {
        flex-basis: calc(99.98% * 3/5 - (15px - 15px * 3/5));
        max-width: calc(99.98% * 3/5 - (15px - 15px * 3/5));
        width: calc(99.98% * 3/5 - (15px - 15px * 3/5));
      }

      .fifths > x-cell,
      .fifths.major-in-the-middle > x-minor {
        flex-basis: calc(99.98% * 1/5 - (15px - 15px * 1/5));
        max-width: calc(99.98% * 1/5 - (15px - 15px * 1/5));
        width: calc(99.98% * 1/5 - (15px - 15px * 1/5));
      }

      .sixths > x-cell {
        flex-basis: calc(99.98% * 1/6 - (15px - 15px * 1/6));
        max-width: calc(99.98% * 1/6 - (15px - 15px * 1/6));
        width: calc(99.98% * 1/6 - (15px - 15px * 1/6));
      }

      .sevenths > x-minor {
        flex-basis: calc(99.98% * 10/23 - (15px - 15px * 10/23));
        max-width: calc(99.98% * 10/23 - (15px - 15px * 10/23));
        width: calc(99.98% * 10/23 - (15px - 15px * 10/23));
      }

      .sevenths > x-major {
        flex-basis: calc(99.98% * 13/23 - (15px - 15px * 13/23));
        max-width: calc(99.98% * 13/23 - (15px - 15px * 13/23));
        width: calc(99.98% * 13/23 - (15px - 15px * 13/23));
      }

      .sevenths.true > x-minor {
        flex-basis: calc(99.98% * 3/7 - (15px - 15px * 3/7));
        max-width: calc(99.98% * 3/7 - (15px - 15px * 3/7));
        width: calc(99.98% * 3/7 - (15px - 15px * 3/7));
      }

      .sevenths.true > x-major {
        flex-basis: calc(99.98% * 4/7 - (15px - 15px * 4/7));
        max-width: calc(99.98% * 4/7 - (15px - 15px * 4/7));
        width: calc(99.98% * 4/7 - (15px - 15px * 4/7));
      }

      .sevenths > x-cell {
        flex-basis: calc(99.98% * 1/7 - (15px - 15px * 1/7));
        max-width: calc(99.98% * 1/7 - (15px - 15px * 1/7));
        width: calc(99.98% * 1/7 - (15px - 15px * 1/7));
      }

      @media only screen and (max-width: calc(1200px + 50px)) {

        panel-wrapper panel-inner {
          padding: 60px 25px;
          width: calc(100% - 50px);
        }

      }
    </style>
    <script>
      class panelWrapper extends HTMLElement {}
      window.customElements.define('panel-wrapper', panelWrapper);

      class panelInner extends HTMLElement {
        connectedCallback() {
          if (this.hasAttribute('whitespace')) {
            var VAL = this.getAttribute('whitespace');
            // console.log(this.children[0]);
            this.style.paddingTop = VAL + "px";
            this.style.paddingBottom = VAL + "px";
          }
        }
      }
      window.customElements.define('panel-inner', panelInner);

      class segmentElem extends HTMLElement {}
      window.customElements.define('segment-elem', segmentElem);

      class segMajor extends HTMLElement {}
      window.customElements.define('x-major', segMajor);

      class segMinor extends HTMLElement {}
      window.customElements.define('x-minor', segMinor);

      class segCell extends HTMLElement {}
      window.customElements.define('x-cell', segCell);
    </script>
    <title>My Site</title>
  </head>
  <body>
    <div id="container">
      <div class="title">My Site</div>
        $1
    </div>
  </body>
</html>
'''
        snipCheck = "'prefix': 'html-mark'"
        pat = re.escape(snipCheck)
        match = re.search(pat, data)
        print(divider)
        if match:
            print("")
            print("\t- Snippet already set!")
            print("")
        else:
            print("")
            print("\t- Snippet has been added")
            print("")
            data += snip
        FILE.write(data)
        FILE.close()

    def handle_inkscape_customization():
        print("")
        print("-- Inkscape: Customizing Keys, Icons and Skin --")
        base = os.path.expanduser('~')

        keysTemplate = base +  '/Documents/new-mac-setup/Inkscape/default.xml'
        keysPath = "/Applications/Inkscape.app/Contents/Resources/share/inkscape/keys/default.xml"

        themeTemplate = base + '/Documents/new-mac-setup/Inkscape/Darken'
        themePath = base + '/.themes/Darken/'

        iconTemplate = base + '/Documents/new-mac-setup/Inkscape/icons.svg'
        iconPath = "/Applications/Inkscape.app/Contents/Resources/share/inkscape/icons/icons.svg"

        xmodmapString = '''! ~/.Xmodmap
clear Mod2
clear control
keycode 63 = Control_L
keycode 67 = Control_L
keycode 71 = Control_L
add control = Control_L
'''

        gtkString = '''gtk-theme-name = "Darken"'''

        print("")
        print("\t- Setting Keys")
        print("")
        print('Running Command: {} {} {}'.format('cp', keysTemplate, keysPath))
        subprocess_cmd('cp {} {}'.format(keysTemplate, keysPath))
        raw_input('''Instructions:
1. Start the X11 application
2. In X11, go to X11 > Preferences > Input tab. Make sure that the following options are UNCHECKED:

  - Follow system keyboard layout
  - Enable key equivalents under X11

3. Close X11 Preferences

Press "Enter" to continue:''')
        print("")
        print("\t- Finalizing Command Key Setup")
        print("")

        verify_file(base + '/.Xmodmap', xmodmapString, 'Xmodmap for command key set', 'Xmodmap for command key already set')

        raw_input('''Another issue that you may run into is copy/paste converts objects to bitmaps. You can resolve this in xQuartz by unchecking "Update Pasteboard when CLIPBOARD changes"

Press "Enter" to continue:''')

        #== In order to style the skin, you have to style the x11 theme settings, instead:
        #================================================
        print("")
        print("\t- Setting Theme: Darken")
        print("")

        if not os.path.exists(base + '/.themes'):
            subprocess_cmd('mkdir {}/.themes'.format(base))

        if not os.path.exists(themePath):
            subprocess_cmd('cp -r {} {}'.format(themeTemplate, themePath))
            print("\t\t- Theme added")
            print("")
        else:
            print("\t\t- Theme already added!")
            print("")

        verify_file(base + '/.gtkrc-2.0', gtkString, 'Theme set', 'Theme already set')
        #================================================

        print("")
        print("\t- Setting Icons")
        print("")
        print('Running Command: {} {} {}'.format('cp', iconTemplate, iconPath))
        subprocess_cmd('cp {} {}'.format(iconTemplate, iconPath))

        # Contents/Resources/etc/gtk-2.0

    def run_command(CMD):
    	import subprocess
    	subprocess.call(CMD, shell=True)

    def clone_repo(DESTINATION, USER, NAME):
    	cloneCommand = 'cd {destination} && git clone git@gitlab.com:{user}/{name}.git'.format(destination = DESTINATION, user = USER, name = NAME)
    	run_command(cloneCommand)

    def rename_repo(OLD_NAME, NEW_NAME):
    	renameCommand = "mv {} {}".format(OLD_NAME, NEW_NAME)
    	run_command(renameCommand)

    def install_wirestorm(DESTINATION):
    	print("should be downloading to: " + DESTINATION)
    	installCommand = "cd {} && curl -OL https://github.com/jaderigby/wirestorm2/archive/master.zip".format(DESTINATION)
    	run_command(installCommand)
    	unzipCommand = "cd {destination} && unzip master.zip -d {destination}".format(destination = DESTINATION)
    	run_command(unzipCommand)
    	flattenCommand = "scp -r {destination}/wirestorm2-master/ {destination}/".format(destination = DESTINATION)
    	run_command(flattenCommand)
    	cleanupCommand = "cd {destination}/ && rm master.zip && rm -r wirestorm2-master".format(destination = DESTINATION)
    	run_command(cleanupCommand)

    def handle_bash_tools_setup():
        myFolder = 'bash-tools2'
        subprocess_cmd('mkdir ~/Documents/{myFolder}'.format(myFolder = myFolder))
        subprocess_cmd('cd ~/Documents/{myFolder} && touch .bashrc'.format(myFolder = myFolder))
        subprocess_cmd('mkdir ~/Documents/{myFolder}'.format(myFolder = myFolder))
        base = os.path.expanduser("~")
        snippet = 'source ~/Documents/bash-tools2'
        if os.path.exists('{base}/.bash_profile'.format(base = base)):
            data = read_file('{base}/.bash_profile'.format(base = base))
            verify_file(base + '/.bash_profile', snippet, 'Sourcing is set', 'Sourcing already set')
        else:
            subprocess_cmd('touch ~/.bash_profile')
            verify_file(base + '/.bash_profile', snippet, 'Sourcing is set', 'Sourcing already set')

    def install_from_github(REPO_NAME, NEW_NAME):
        myFolder = 'bash-tools2'
        subprocess_cmd('cd ~/Documents/{myFolder} && curl -OL https://github.com/jaderigby/{repoName}/archive/master.zip'.format(myFolder = myFolder, repoName = REPO_NAME))
        subprocess_cmd('cd ~/Documents/{myFolder} && unzip master.zip'.format(myFolder = myFolder))
        subprocess_cmd('scp -r ~/Documents/{myFolder}/{repoName}-master/ ~/Documents/{myFolder}/{newName}/'.format(myFolder = myFolder, repoName = REPO_NAME, newName = NEW_NAME))
        subprocess_cmd('cd ~/Documents/{myFolder}/ && rm master.zip && rm -r {repoName}-master'.format(myFolder = myFolder, repoName = REPO_NAME))

    def install_from_gitlab(REPO_NAME, NEW_NAME):
        myFolder = 'bash-tools2'
        subprocess_cmd('cd ~/Documents/{myFolder} && curl -OL https://gitlab.com/jarigby/{repoName}/archive/master.zip'.format(myFolder = myFolder, repoName = REPO_NAME))
        subprocess_cmd('cd ~/Documents/{myFolder} && unzip master.zip'.format(myFolder = myFolder))
        subprocess_cmd('scp -r ~/Documents/{myFolder}/{repoName}-master/ ~/Documents/{myFolder}/{newName}/'.format(myFolder = myFolder, repoName = REPO_NAME, newName = NEW_NAME))
        subprocess_cmd('cd ~/Documents/{myFolder}/ && rm master.zip && rm -r {repoName}-master'.format(myFolder = myFolder, repoName = REPO_NAME))

    def handle_bacon_util():
        subprocess_cmd('mkdir {}'.format('~/Documents/bash-tools2'))
        handle_bash_tools_setup()
        install_from_github('bacon-util', 'bacon')
        snippet = 'alias bacon="python ~/Documents/bash-tools2/bacon/baconActions.py'
        verify_file(base + '/.bash_profile', snippet, 'Alias is set', 'Alias already set')

        # alias bacon="python ~/Documents/bash-tools/bacon-util/baconActions.py"

    def handle_videos_utility():
        install_from_gitlab('videos-utility', 'videos')
        bash_tools_alias('')

    def handle_image_optimization_utility():
        install_from_gitlab('image-optimization-utility', 'image-optimization')

    #=== Execute ===
    if action == None:
        print("Acceptable Actions:")
        print('''
[ -a ]                  Run all processes
[ --dave ]              Install components for Dave's computer
[ --exec ]              make script executable from command line by simply typing file name
[ --aliases ]           Add standard aliases to bash_profile, including show/hide hidden files
[ --homebrew ]          install Homebrew
[ --install ]           install all software (node, chrome, etc)
[ --atom-custom ]       customize atom (includes packages)
[ --atom-snippets ]     markdown template snippet
[ --inkscape-custom ]   customize Inkscape.  Includes: icons, colors, keybindings
[ --br-aliases ]        Add Basic Research Specific aliases
[ --install-list ]      Install specific items as a list
[ --bacon ]             Install bacon utilities including creating "bash-tools" folder within Documents directory
[ --image-opt ]         Install the image optimization utility
''')
    else:
        for param in sys.argv:
            if param == '-a':
                handle_executable()
                handle_aliases()
                handle_homebrew()
                handle_installs()
                handle_atom_customization()
                handle_atom_snippets()
                handle_inkscape_customization()
            elif param == '--dave':
                handle_executable()
                handle_aliases()
                handle_br_aliases()
                handle_homebrew()
                handle_installs_as_list()
                handle_atom_customization()
                handle_atom_snippets()
                handle_inkscape_customization()
            elif param == '--exec':
                handle_executable()
            elif param == '--homebrew':
                handle_homebrew()
            elif param == '--aliases':
                handle_aliases()
            elif param == '--install':
                handle_installs()
            elif param == '--atom-custom':
                handle_atom_customization()
            elif param == '--atom-snippets':
                handle_atom_snippets()
            elif param == '--inkscape-custom':
                handle_inkscape_customization()
            elif param == '--br-aliases':
                handle_br_aliases()
            elif param == '--install-list':
                handle_installs_as_list()
            elif param == '--bacon':
                handle_bacon_util()
            elif param == '--videos':
                handle_videos_utility()
            # elif param == '--image-opt':
            #     handle_image_optimization_utility()
            # elif param == '--deepignore':
            #     handle_deepignore_utility()
        print(divider)
        print("")

if __name__ == '__main__':
    main()
