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
            FILE = open(base + '/.bashrc', 'w')
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
              , "verify" : None
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
        ]

        for item in installDict:
            if verify_installation(item['verify']) != True:
                print("Downloading {} ...".format(item['name']))
                subprocess_cmd(item['cmd'])

        # npm install -g grunt-cli

        # -bash: cask: command not found
        # ln -s /Applications/Atom.app/Contents/Resources/app/atom.sh /usr/local/bin/atom

    #=== Execute ===
    if action == None:
        print("Acceptable Arguments:")
        print('''
[ -a ]                  Run all processes
[ --exec ]              make script executable from command line by simply typing file name
[ --homebrew ]          install Homebrew
[ --install ]           install all packages (node, etc)
''')
    else:
        for param in sys.argv:
            if param == '-a':
                handle_executable()
                handle_homebrew()
                handle_installs()
            elif param == '--exec':
                handle_executable()
            elif param == '--homebrew':
                handle_homebrew()
            elif param == '--install':
                handle_installs()
        print(divider)
        print("")

if __name__ == '__main__':
    main()
