#! /bin/bash

read -r MODEL TOPIC < <(jq -r '"\(.model2) \(.topic)"' state.json)   # "\(.model) \(.topic)" is called string interpolation
gnome-terminal -- bash -c "                                         # used for taking strings with spaces and tabs
ollama run $MODEL \"Tell me about $TOPIC\"; exec bash "