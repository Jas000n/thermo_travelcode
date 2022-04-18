# 基于树莓派3B的疫情防控机器人





### 1. 概述

![travelcode_thermo (1)](https://tva1.sinaimg.cn/large/e6c9d24egy1h1dqtd2u1nj20rm1kjwgx.jpg)

<img src="https://tva1.sinaimg.cn/large/e6c9d24egy1h1dqrzrp2xj21fr0u0wog.jpg"  style="zoom:20%; " />

<center>
开发的嵌入式疫情防控机器人</center>

运用人体红外感应传感器（HC-SR501）检测人体，红外测温传感器（MLX90614）为人体测温，CSI串口的摄像头检测人脸及大数据行程卡是否绿卡，为精准、科学疫情防控助力。还设计了测温传感器的温度补偿算法，用超声波测距传感器（HC-SR04）测量机器与人的距离，来补偿距离过远，造成不能完全覆盖视场导致温度不准的问题（详见2.2.3）。

### 2. 传感器

下面我将阐释我对我用到的这几款传感器的学习体会。

#### 2.1 人体红外感应传感器（HC-SR501）

<img src="https://i2.wp.com/img-blog.csdnimg.cn/20200402192109975.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpdXhpYW5mZWkwODEw,size_16,color_FFFFFF,t_70"  width=200 />

##### 2.1.1 工作原理

任何物体都会放出红外线，人体自然也不例外。人体具有恒定的体温，一般在37度左右，发出特定波长10UM左右的红外线，HC - SR501就是靠探测人体发射的10UM左右的红外线而进行工作的。人体发射的10UM左右的红外线通过菲涅尔透镜增强后聚集到红外感应源上。而红外感应元采用具有热释电效应的元件，一般为陶瓷氧化物或压电晶体。在其感应到监测范围内有温度变化后，热释电效应会在两个电极上产生电荷，从而形成从“外部信号”（即人进入检测范围）到电信号的转化。

##### 2.1.2 功能介绍

本传感器具有两种跳线方式，我在使用时采用了不重复触发的接线方式，作为疫情防控小车主程序的开关，在检测到人体之后才会开始工作。两种触发方式如下：

* 不可重复触发方式:即感应输出高电平后，延时时间段一结束，输出将自动从高电平变成低电平；
* 可重复触发方式：即感应输出高电平后，在延时时间段内，如果有人体在其感应范围活动，其输出将一直保持高电平，直到人离开后才延时将高电平变为低电平。（感应模块检测到人体的每一次活动后会自动顺延一个延时时间段，并且以最后一次活动的时间为延时时间的起始点)

##### 2.1.3 电路图

<img src="https://i2.wp.com/img-blog.csdnimg.cn/20200402191942885.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpdXhpYW5mZWkwODEw,size_16,color_FFFFFF,t_70" style="zoom: 67%;" />



#### 2.2 红外测温传感器（MLX90614）

<img src="https://tva1.sinaimg.cn/large/e6c9d24egy1h1dqroqe47j20qq0kcgmr.jpg" alt="image-20220415225911973" width = 200 />

##### 2.2.1 工作原理

物体表面温度决定了其红外辐射能量的大小和波长的分布。因此，通过对物体红外辐射的测量，能准确地确定其表面温度，红外测温就是利用这一原理测量温度的。红外测温器由光学系统、光电探测器、信号放大器和信号处理及输出等部分组成。光学系统汇聚其视场内的目标红外辐射能量，视场的大小由测温仪的光学零件及其位置确定。红外能量聚焦在光电探测器上并转变为相应的电信号。该信号经过放大器和信号处理电路，并按照仪器内的算法和目标发射率校正后转变为被测目标的温度值。

该模块以81101热电元件作为红外感应部分。输出是被测物体温度($T_o$)与传感器自身温度($T_a$)共同作用的结果，理想情况下热电元件的输出电压为：$Vir = A(T_o^4+T_a^4)$. 其中温度单位为开氏度，A为元件的灵敏度系数。

##### 2.2.2 功能介绍

利用SMbus接口通信，传输数据，对环境温度和视场内温度进行检测，将外部信号（温度）转化为可供后续处理的电信号。

##### 2.2.3 温度补偿算法

在测温过程中，实际是计算“视场”内点的平均值。所以当被测物体完全覆盖FOV视场时的准确度是最高的。

然而在对人脸测温的过程中，因为人脸可能距离测温传感器较远，导致没有完全覆盖其视场，使得视场内很多点的温度实际是环境温度，致使测量的温度不准确。所以我设计了如下的温度补偿算法：

<img src="https://tva1.sinaimg.cn/large/e6c9d24egy1h1dqrppld8j20u00wi755.jpg" alt="Screenshot_2022-04-17-12-28-28-771_com.microsoft.office.onenote" style="zoom: 50%;" />

用距离传感器测出MLX90614与人脸的距离d，已知视场角为$2\theta$，人脸的大概大小为S。测出来的环境温度为$T_环$，测出的视场内的平均温度为$T_测$，估计的人脸温度为$T_脸$，所以可以得到如下温度对应关系：

$\pi(tan\theta*d)^2 * T_测= S * T_脸 + (\pi(tan\theta*d)^2 - S) * T_环 $

进一步推导出人脸的估计温度：

$T_脸 = （\pi(tan\theta*d)^2 * T_测 - (\pi(tan\theta*d)^2 - S) * T_环）/S $ 

这样可以尽量减少距离较远导致对视场覆盖不足的影响。但是由于疫情原因快递停运，未能买到超声波距离传感器，导致这个算法只存在于设计阶段，未能真正实现，实在是非常可惜。

##### 2.2.4 电路图

<img src="https://tva1.sinaimg.cn/large/e6c9d24egy1h1dqrkf3t9j20jm0kg75s.jpg" alt="image-20220417231144838" style="zoom:50%;" />

#### 2.3 CSI摄像头

<img src="https://tva1.sinaimg.cn/large/e6c9d24egy1h1dqrlvk5ij20n00j40u7.jpg" alt="image-20220417125112202" width=200 />

##### 2.3.1 工作原理

我使用的这款CSI串口的摄像头采用了索尼IMX219光学传感器。是一款CMOS作为感光元件的摄像头，具有低成本、低功耗、以及高整合度的特点。

<img src="https://tva1.sinaimg.cn/large/e6c9d24egy1h1dqrnpjbkj20o20hgt9z.jpg" alt="image-20220417131152878" style="zoom:33%;" />

在上面的CMOS结构图中，我们可以看出，CMOS作为传感器是如何把光学信号转化为电信号的。

* 光线从物镜进入
* 通过IR层，滤除红外光
* 在Mircolens层，每个像素上都有一个小“镜头”
* 光线经过贝尔过滤器，被分为RGB三种颜色
* 转化为电信号

##### 2.3.2 实现功能

传回电信号，即图片后，用机器学习目标检测算法，提前训练好的yolov5模型对健康码、人脸等进行检测。效果如下：

<img src="/Users/jas0n/Library/Application Support/typora-user-images/image-20220417132022927.png" alt="image-20220417132022927" style="zoom:33%;" />

从而保证只有未去过高风险地区的健康码为绿码的人，才可以通行。如果能连接政府的公民数据库，也可以对辽视通健康码进行检测，解析二维码后得到公民信息，从而对到访、经过人员进行登记，保证后续流调的顺利进行。

#### 2.4 超声波测距传感器

<img src="https://th.bing.com/th/id/OIP.mKgb0wLF9VXBYIpIH0FoIQHaHa?pid=ImgDet&rs=1" alt="查看源图像" width=200 />

计划使用HC-SR04进行机器与人脸的距离测量，实现上面2.2.3所说的温度补偿算法。

##### 2.4.1 工作原理

一般说话的频率范围为100Hz～8kHz，20kHz以上的声音称为超声波。超声波为直线传播，频率越高，绕射能力越弱，但反射能力越强，为此利用超声波的这种性质就可以制成超声波传感器。

HC-SR04这款传感器是一款兼用型传感器，即既能发送超声波又能接受超声波。

* 其发射超声波的原理为：利用压电逆效应的原理，在压电元件上施加电压，元件变形， 外部正电荷与压电陶瓷的极化正电荷相斥。同时，外部负电荷与极化负电荷相斥。由于相斥的作用，压电陶瓷在厚度方向上缩短，在长度方向上伸长。若外部施加的极性变反，压电陶瓷在厚度方向上伸长，在长度方向上缩短。采用双晶振子，两面涂敷薄膜电极，其上面用引线通过金属板(振动板)接到一个电极端，下面用引线直接接到另一个电极端。双晶振子为正方形，正方形的左右两边由圆弧形凸起部分支撑着。这两处的支点就成为振子振动的节点。金属板的中心有圆锥形振子，具有较强的方向性，因而能高效率地发送超声波；

* 其接收超声波的原理为：利用压电效应，若接收到发送器发送的超声波，振子就以发送超声波的频率进行振动。于是就产生与超声波频率相同的高频电压，当然这种电压是非常小的，必须采用放大器放大。

##### 2.4.2 实现功能

测量机器和人之间的距离，为红外测温传感器做温度补偿。

##### 2.4.3 电路图

<img src="https://gss0.baidu.com/94o3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/9f510fb30f2442a72120262bd343ad4bd1130216.jpg" alt="查看源图像" style="zoom:80%;" />

