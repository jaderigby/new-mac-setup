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

    def handle_executable():
        base = os.path.expanduser('~')
        if not os.path.exists(base + '/Documents/new-mac-setup'):
            subprocess_cmd('cd {}/Documents && git clone https://github.com/jaderigby/new-mac-setup.git'.format(base))
        print("-- Making setup file executable --")
        alias = '''
    export PATH={}/Documents/new-mac-setup:$PATH
    '''.format(base)
        FILE = open(base + '/.bash_profile', 'r')
        data = FILE.read()
        FILE.close()
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

        for line in out.split('\n'):
            if 'setup.py' in line:
                if '-x' in line:
                    executable = True
                else:
                    executable = False

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

    def handle_homebrew():
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
                  "name" : "Dropbox"
                , "verify" : "ls /Applications/ | grep -w Dropbox"
                , "cmd" : "brew cask install dropbox"
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
                  "name" : "Slack"
                , "verify" : "ls /Applications/ | grep -w Slack"
                , "cmd" : "brew cask install slack"
            }
            ,{
                  "name" : "Inkscape"
                , "verify" : "ls /Applications/ | grep -w Inkscape"
                , "cmd" : "brew install inkscape"
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
                  "name" : "XQuartz"
                , "verify" : None
                , "cmd" : "brew cask install xquartz"
            }
        ]

        for item in installDict:
            if verify_installation(item['verify']) != True:
                print("Downloading {} ...".format(item['name']))
                subprocess_cmd(item['cmd'])

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

    #=== Execute ===
    if action == None:
        print("Acceptable Actions:")
        print('''
[ -a ]                  Run all processes
[ --exec ]              make script executable from command line by simply typing file name
[ --homebrew ]          install Homebrew
[ --install ]           install all software (node, chrome, etc)
[ --atom-custom ]       customize atom (includes packages)
[ --atom-snippets ]     markdown template snippet
''')
    else:
        for param in sys.argv:
            if param == '-a':
                handle_executable()
                handle_homebrew()
                handle_installs()
                handle_atom_customization()
                handle_atom_snippets()
            elif param == '--exec':
                handle_executable()
            elif param == '--homebrew':
                handle_homebrew()
            elif param == '--install':
                handle_installs()
            elif param == '--atom-custom':
                handle_atom_customization()
            elif param == '--atom-snippets':
                handle_atom_snippets()
        print(divider)
        print("")

if __name__ == '__main__':
    main()
