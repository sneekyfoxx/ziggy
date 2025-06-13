#!/usr/bin/env bash


setup() {
  local prefix="$1";
  local curdir="$(pwd)";
  local py_ver="$(ls /usr/bin | grep -E '^python3[.][0-9]+$' | tr '\n' ' ' | cut -d ' ' -f1)";
  local pattern="^[/]";

  if [ ! "${prefix}" ] || [ ! -d "${prefix}" ]; then
    prefix="${HOME}/.local/bin";

    echo -e "Creating ziggy python zipfile\n";
    sleep 1;
    command "${py_ver}" -m zipapp -o ziggy -p "/usr/bin/env python3" -c "${curdir}/pkg";

    echo -e "Moving ziggy to ${prefix}";
    sleep 1;
    mv "${curdir}/ziggy" "${prefix}/ziggy";
  else
    echo -e "Creating ziggy python zipfile\n";
    sleep 1;
    command "${py_ver}" -m zipapp -o ziggy -p "/usr/bin/env python3" -c "${curdir}/pkg";

    echo -e "Moving ziggy to ${prefix}";
    sleep 1;
    if [[ $prefix =~ $pattern ]]; then
      echo -e "sudo privileges is need to move 'ziggy' to '${prefix}'";
      sudo mv "${curdir}/ziggy" "${prefix}/ziggy";
    else
      mv "${curdir}/ziggy" "${prefix}/ziggy";
    fi
  fi
}

setup "$@";
ziggy;
