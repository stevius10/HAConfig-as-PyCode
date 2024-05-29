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
    cp "$1" /share/Extern
}
alias cpe='file_copy-to-extern'

# Terminal

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

export PATH=$HOME/bin:/usr/local/bin:$PATH
export ZSH=$HOME/.oh-my-zsh

# Terminal

ZSH_THEME="robbyrussell"
ENABLE_CORRECTION="true"
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

# User

export EDITOR='vim'
export LANG=de_DE.UTF-8
export MANPATH="/usr/local/man:$MANPATH"
# export SSH_KEY_PATH="~/.ssh/rsa_id"

source <(ha completion zsh) && compdef _ha ha