#!/usr/bin/python

import os, subprocess, re, sys

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
alias hidehidden="defaults write com.apple.finder AppleShowAllFiles FALSE && killall Finder"

jira_branch_func() {
  newBranch=$1
  git fetch origin
  git branch -v -a
  git checkout --track origin/$newBranch
}

alias jira-branch="jira_branch_func"'''
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

        # npm install -g grunt-cli

        # -bash: cask: command not found
        # ln -s /Applications/Atom.app/Contents/Resources/app/atom.sh /usr/local/bin/atom

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
        install_atom_package('atom-like-brackets-editor')
        install_atom_package('language-stylus')
        install_atom_package('pigments')
        install_atom_package('atom-jade')
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
        snip = ''''
.text.html.basic':
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
		<title>My Blog</title>
	</head>
	<body>
		<div id="container">
			<div class="title">My Blog</div>
			<section class="sevenths">
				<aside>

				</aside>
				<article>

				</article>
			</section>
		</div>
	</body>
</html>
"""
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


    #=== Execute ===
    if action == None:
        print("Acceptable Actions:")
        print('''
[ -a ]                  Run all processes
[ --exec ]              make script executable from command line by simply typing file name
[ --aliases ]           Add standard aliases to bash_profile, including show/hide hidden files
[ --homebrew ]          install Homebrew
[ --install ]           install all software (node, chrome, etc)
[ --atom-custom ]       customize atom (includes packages)
[ --atom-snippets ]     markdown template snippet
[ --inkscape-custom ]   customize Inkscape.  Includes: icons, colors, keybindings
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
        print(divider)
        print("")

if __name__ == '__main__':
    main()
