ZSH_THEME_GIT_PROMPT_CLEAN=""
ZSH_THEME_GIT_PROMPT_ADDED="+"
ZSH_THEME_GIT_PROMPT_MODIFIED="*"
ZSH_THEME_GIT_PROMPT_RENAMED="~"
ZSH_THEME_GIT_PROMPT_DELETED="X"
ZSH_THEME_GIT_PROMPT_DIRTY="%"
ZSH_THEME_GIT_PROMPT_UNTRACKED="!"
ZSH_THEME_GIT_PROMPT_UNMERGED="#"

function sancho_prompt_char {
	if [ $UID -eq 0 ]; then
		echo '#';
	else
		echo '$';
	fi
}

function sancho_git_status {
	local branch=$(git_current_branch)
	if [ "$branch" != "" ]; then
		echo " %{$fg[green]%}(%{$branch%}%{$fg[red]%}$(git_prompt_status)%{$fg[green]%})"
	fi
}

PROMPT='%{$fg[white]%}[%*]%(?,, %{$fg[red]%}X) %{$fg[green]%}%n%{$fg[magenta]%}@%{$fg[cyan]%}%m %{$fg_bold[blue]%}%~%{$reset_color%}$(sancho_git_status) %{$fg[yellow]%}$(sancho_prompt_char)%{$reset_color%} '
