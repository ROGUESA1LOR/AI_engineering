#! /bin/bash
rm pipe1 pipe2 pipe3         #these are for terminal aesthetics
mkfifo pipe1 pipe2 pipe3
TOPIC=""
MODEL1_NAME=""
MODEL2_NAME=""
read -rp "Enter the Topic: " TOPIC
read -rp "Enter the model1(topic defender) name: " MODEL1_NAME
read -rp "Enter the model2(topic attacker) name: " MODEL2_NAME
jq -n --arg topic "$TOPIC" \
 --arg model1 "$MODEL1_NAME" \
 --arg model2 "$MODEL2_NAME" '{topic: $topic, status: "active",model1: $model1 ,model2: $model2, history: []}' > state.json
chmod +x MODEL1.sh
chmod +x MODEL2.sh
./MODEL1.sh
./MODEL2.sh