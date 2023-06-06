## 第二十五届中国机器人及人工智能大赛智慧药房组
ROS 破车的代码仓库
# 常用命令
* 调参工具
rosrun rqt_reconfigure rqt_reconfigure
* 杀死所有节点
rosnode kill -a
* 打开rviz观察路径
roslaunch robot_navigation navigation_rviz.launch
* 车不动调参
修改move_base.launch文件，将cmd_vel话题重命名（打开文件一看就懂）
* 观察系统结构
rosrun rqt_graph rqt_graph
# 需要启动的功能包(Master)
 * roslaunch robot_navigation robot_navigation.launch
 * roslaunch actuator car_master.launch 
 * roslaunch char_recognizer char_recognizer.launch         # 真图
 * roslaunch char_recognizer char_recognizer_fake.launch    # 假图
 * roslaunch deliver_scheduler scheduler.launch
# 需要启动的功能包（Slave）
 * roslaunch robot_navigation robot_navigation.launch
 * roslaunch actuator car_slave.launch 
# 需要启动的功能包(Watcher)
 * roslaunch robot_navigation robot_navigation.launch
 * roslaunch actuator car_watcher.launch 

# usb-cam使用注意
出现[image_view-3] process has died [pid 22787, exit code -11, cmd /opt/ros/melodic/lib/image_view/image_view image:=/usb_cam/image_raw __name:=image_view __log:=/home/EPRobot/.ros/log/8cd2c622-0464-11ee-9185-000c29f076f7/image_view-3.log].
log file: /home/EPRobot/.ros/log/8cd2c622-0464-11ee-9185-000c29f076f7/image_view-3*.log
的错误警告为正常现象，请勿慌张


# map参数
* 以114\*147pixel的fake_map（人为制作，不是slam建图）为基础，以左上角为(0,0)的原点右x正方向，下y正方向的图片坐标系
* 以114\*147pixel的fake_map按照5cm/像素转化为物理坐标系，那么生成570cm*735cm的物理扩大地图（左上为原点，xy与图片坐标系一致）
* 真实地图在扩大地图居中
* Ros栅格地图坐标系为x右y上
* 怎么算?[参考视频](https://www.bilibili.com/video/BV17W4y137pF/?spm_id_from=333.788&vd_source=16b1b0409d11ad21fe29562b0e9fc9b4)

|特殊点|图片坐标系|Ros坐标系|物理坐标系|
|:---:|:---:|:---:|:---:|
|Ros原点|(62.6,110.1)|(0,0)         |(3130,5505)|
| A点   |(72,59.5)   |(0.47,2.53)   |(3600,2975)|
| B点   |(90,49.5)   |(1.37,3.03)   |(4500,2475)|
| C点   |(90,69.5)   |(1.37,2.03)   |(4500,3475)|
| 1点   |(24,67.5)   |(-1.93,2.13)  |(1200,3375)|
| 2点   |(42,77.5)   |(-1.03,1.63)  |(2100,3875)|
| 3点   |(24,87.5)   |(-1.93,1.13)  |(1200,4375)|
| 4点   |(42.97.5)   |(-1.03,0.63)  |(2100,4875)|
| 暂停点|()|(-0.28, 3.78)|()|
