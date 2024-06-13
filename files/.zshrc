# immutable requires privileged ssh addon run init command to 
# append 'source .zshrc' via supervisor /root/.zshrc, e. g. 
# echo "source /homeassistant/.storage/zsh/.zshrc" >> /root/.zshrc
# or echo "ZDOTDIR=/config/.storage/zsh" >> /root/.zshrc

# Path

export PATH=$HOME/bin:/usr/local/bin:$PATH

# Alias

alias python=python3
alias py=python
alias pip=pip3

alias grep='grep --color=auto'
alias ls='ls -lhA --color=auto --group-directories-first'
alias mkdir='mkdir -pv'
alias vi="vim -c 'startinsert'"

alias redo='sudo $(fc -ln -1)'

alias cdp='cd /homeassistant/pyscript/
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'

alias git-reset='git reset HEAD'

# Functions 

copy_to_extern() {
    cp "$1" /share/Extern
}
alias cpe='copy_to_extern'