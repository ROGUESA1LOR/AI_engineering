#! /bin/bash
#this is attackers script

read -r MODEL TOPIC < <(jq -r '"\(.model2) \(.topic)"' state.json)   # "\(.model) \(.topic)" is called string interpolation
                                                                     # used for taking strings with spaces and tabs
PROMPT="[IDENTITY: Debater B (Attacker)]
[GLOBAL_TOPIC: $TOPIC]
[RULE: Review the running history. Shred Debater A's arguments. Don't repeat Debater A's arguments. Make sure to be concise and clear. Be aggressive and assertive. Use strong language. Be short (6 lines at most) and to the point.]"

# [TRANSCRIPT]
# $TRANSCRIPT
# [/TRANSCRIPT]"
gnome-terminal -- bash -c "
sleep 1;
wmctrl -r :ACTIVE: -e 0,641,0,640,480;                                        
ollama run $MODEL \"$PROMPT\"; exec bash "