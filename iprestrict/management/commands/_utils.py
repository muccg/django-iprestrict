import warnings


def warn_about_renamed_command(old_name, new_name):
    # DeprecationWarnings are ignored by default, so lets make sure that
    # the warnings are shown by using the default UserWarning instead
    warnings.warn("The command '%s' has been deprecated and it will be removed in a future version. "
                  "Please use '%s' instead." % (old_name, new_name))
