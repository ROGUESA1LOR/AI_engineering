#! /bin/bash
#this is defenders script
read -r MODEL TOPIC < <(jq -r '"\(.model1) \(.topic)"' state.json)   # "\(.model) \(.topic)" is called string interpolation
                                                                     # used for taking strings with spaces and tabs
PROMPT="[IDENTITY: Debater A (Defender)]
[GLOBAL_TOPIC: $TOPIC]
[RULE: Review the running history. Do not repeat old points. Counter the opponent.]

[TRANSCRIPT]
$TRANSCRIPT
[/TRANSCRIPT]"
gnome-terminal -- bash -c "
sleep 1;
wmctrl -r :ACTIVE: -e 0,1,0,640,480;
ollama run $MODEL \"$PROMPT\"; exec bash "
