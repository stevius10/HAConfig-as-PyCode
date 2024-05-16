### Personal

# Path

# PATH=":$PATH"
export PATH

# Alias

alias python=python3
alias py=python
alias pip=pip3

alias grep='grep --color=auto'
alias ls='ls -lah --color=auto --group-directories-first --human-readable'
alias mkdir='mkdir -pv'
alias vi="vim -c 'startinsert'"

alias redo='sudo $(fc -ln -1)'

alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'

alias git-reset='git reset HEAD'

# Functions 

file_copy-to-extern() {
    cp $1 /share/Extern
}
alias cpd='file_copy-to-desktop'



# Shell

setopt AUTO_CD
setopt CORRECT
setopt CORRECT_ALL
setopt NO_CASE_GLOB

setopt SHARE_HISTORY
setopt APPEND_HISTORY
setopt INC_APPEND_HISTORY
setopt HIST_EXPIRE_DUPS_FIRST 
setopt HIST_FIND_NO_DUPS
setopt HIST_REDUCE_BLANKS

SAVEHIST=5000
HISTSIZE=2000
HISTFILE=${ZDOTDIR:-$HOME}/.zsh_history

PROMPT='%F{white}%~ %F{reset}'

### Homeassistant

export ZSH=$HOME/.oh-my-zsh
ZSH_THEME="robbyrussell"

HYPHEN_INSENSITIVE="true"
DISABLE_AUTO_UPDATE="false"
COMPLETION_WAITING_DOTS="true"
DISABLE_UNTRACKED_FILES_DIRTY="true"
HIST_STAMPS="dd.mm.yyyy"
plugins=(
    extract
    git
    tmux
    nmap
    rsync
)
source $ZSH/oh-my-zsh.sh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

export LANG=de_DE.UTF-8
export EDITOR='vim'
# export SSH_KEY_PATH="~/.storage/rsa_id"

source <(ha completion zsh) && compdef _ha ha