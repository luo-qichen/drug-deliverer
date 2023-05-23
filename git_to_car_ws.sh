#!/bin/bash

### 执行该脚本后，小车的功能包与本地仓库git功能包中完全相同。小车中的修改将被 **完全覆盖**. ###

# 从git同步到虚拟机的工作空间
# rsync -av --delete /home/$(whoami)/drug-deliverer/actuator/ /home/$(whoami)/robot_ws/src/actuator/
# rsync -av --delete /home/$(whoami)/drug-deliverer/deliver_scheduler/ /home/$(whoami)/robot_ws/src/deliver_scheduler/
# rsync -av --delete /home/$(whoami)/drug-deliverer/board_reminder/ /home/$(whoami)/robot_ws/src/board_reminder/

# 从git同步到小车
ping -c 1 EPRobot0 > /dev/null

if [ $? -eq 0 ]; then
    rsync -av --delete /home/$(whoami)/drug-deliverer/actuator/ EPRobot@EPRobot:/home/EPRobot/robot_ws/src/actuator/
    rsync -av --delete /home/$(whoami)/drug-deliverer/deliver_scheduler/ EPRobot@EPRobot:/home/EPRobot/robot_ws/src/deliver_scheduler/
    rsync -av --delete /home/$(whoami)/drug-deliverer/board_reminder/ EPRobot@EPRobot:/home/EPRobot/robot_ws/src/board_reminder/
    rsync -av --delete /home/$(whoami)/drug-deliverer/char_recognizer/ EPRobot@EPRobot:/home/EPRobot/robot_ws/src/char_recognizer/
    rsync -av --delete /home/$(whoami)/drug-deliverer/param/myparam/ EPRobot@EPRobot:/home/EPRobot/robot_ws/src/robot_navigation/param/
    rsync -av --delete /home/$(whoami)/drug-deliverer/send_goals/ EPRobot@EPRobot:/home/EPRobot/robot_ws/src/send_goals/
    echo "[Master]成功将本地drug-deliverer仓库的修改同步到小车的工作空间"
else
    echo "[Master]无法连接到小车，与小车的同步不会进行"
fi

# 同步到副车
ping -c 1 slave > /dev/null

if [ $? -eq 0 ]; then
    rsync -av --delete /home/$(whoami)/drug-deliverer/watcher_basic/ slave@slave:/home/slave/robot_ws/src/watcher_basic/
    # rsync -av --delete /home/$(whoami)/drug-deliverer/param/myparam/ EPRobot@EPRobot1:/home/EPRobot/robot_ws/src/robot_navigation/param/
    # rsync -av --delete /home/$(whoami)/drug-deliverer/send_goals/ EPRobot@EPRobot1:/home/EPRobot/robot_ws/src/send_goals/
    echo "[Watcher]成功将本地drug-deliverer仓库的修改同步到小车的工作空间"
else
    echo "[Watcher]无法连接到小车，与小车的同步不会进行"
fi
date
