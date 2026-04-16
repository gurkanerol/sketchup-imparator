if not contains "." $PATH
    # Prepending path in case a system-installed binary needs to be overridden
    set -x PATH "." $PATH
end
