[[ $# -ne 1 ]] && echo "start or stop" && exit 1
if [[ $1 == "start" ]]; then
  docker-machine start default
  echo 'eval $(docker-machine env default)'
  echo 'docker-machine ip default'
else
  docker-machine stop default
fi
