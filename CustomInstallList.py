def execute():
    # Directory is items cherry picked to be installed
    directory = [
          "Caskroom"
        , "Git"
        , "NVM"
        , "Yarn"
        , "VSCode"
        , "iTerm2"
        , "Dropbox"
        , "Slack"
        , "ImageMagick"
        , "Chrome"
        , "Firefox"
        , "ImageAlpha"
        , "ffmpeg"
        , "XQuartz"
        , "Inkscape"
        , "GasMask"
    ]
    # Installs is the configuration for ALL possible software
    installs = {
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
        , "NVM" : {
            "name" : "NVM"
            , "verify" : "node --version"
            , "cmd" : "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.36.0/install.sh | bash"
        }
        , "Yarn" : {
            "name" : "Yarn"
            , "verify" : "yarn --version"
            , "cmd" : "brew install yarn"
        }
        , "Node" : {
            "name" : "Node"
            , "verify" : "node --version"
            , "cmd" : "brew install node"
        }
        , "VSCode" : {
            "name" : "Visual Studio Code"
            , "verify" : "ls /Applications/ | grep -w 'Visual Studio Code'"
            , "cmd" : "brew cask install visual-studio-code"
        }
        , "iTerm2" : {
            "name" : "iTerm 2"
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
        , "ffmpeg" : {
            "name" : "ffmpeg"
            , "verify" : "ffmpeg -version"
            , "cmd" : "brew install ffmpeg"
        }
        , "FileZilla" : {
            "name" : "FileZilla"
            , "verify" : "ls /Applications/ | grep -w FileZilla"
            , "cmd" : "cd ~/Downloads && curl -OL https://download.filezilla-project.org/client/FileZilla_3.45.1_macosx-x86_sponsored-setup.dmg && cd /Desktop && hdiutil attach ~/Downloads/FileZilla_3.45.1_macosx-x86_sponsored-setup.dmg"
        }
        , "XQuartz" : {
            "name" : "XQuartz"
            , "verify" : "ls /Applications/Utilities/ | grep -w XQuartz"
            , "cmd" : "brew cask install xquartz"
        }
        , "Inkscape" : {
            "name" : "Inkscape"
            , "verify" : "ls /Applications/ | grep -w Inkscape"
            , "cmd" : "brew cask install inkscape"
        }
        , "GasMask" : {
            "name" : "GasMask"
            , "verify" : "ls /Applications/ | grep -w 'Gas Mask'"
            , "cmd" : "brew cask install gas-mask"
        }
    }
    d = {}
    d['directory'] = directory
    d['installs'] = installs
    return d