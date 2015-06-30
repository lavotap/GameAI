#!/usr/bin/env python
#-*-coding:utf-8-*-

# 追捕函数模块，提供非连续（方格）场景的视线追捕，连续场景的视线追捕，连续场景的拦截函数

from game_tools.vector import Vector
import random
import math
import time

# 非连续（格子）移动方式的视线追捕
class Dis_pred(object):
    def __init__(self,predator_vector,max_speed,test=False):
        self.predator_vector=predator_vector# 追捕者坐标（起始坐标）[vector]
        self.max_speed=max_speed# 最大速度(pix/frame)[number]
        self.test=test# 测试模式（生成测试文件）[bool]
        if test:
            self.comment=""
            self.current_time=time.strftime('%Y-%m-%d-%X',time.localtime())
            self.current_step_num=1

    def start_test(self):
        if self.test:
            self.log_doc=open('./test_tool/log/Dispred_'+self.current_time+'.log','w')
            if self.comment!="":
                self.log_doc.write("COMMENT:["+str(self.current_time)+"]:"+self.comment+'\n')
            self.log_doc.write("START:<start_test>:Predator's vector is "+str(self.predator_vector)+"; max speed is "+str(self.max_speed)+'.\n')

    def end_test(self):
        if self.test:
            self.log_doc.write('END:<end_test>:Total step number is '+str(self.current_step_num-1)+'.\n')
            self.log_doc.close()

    # 追捕
    def hunt(self,prey_vector):# prey_vector猎物（终点）坐标
        self.log_doc.write("HUNT:<Dis_pred hunt>:Prey's vector is "+str(prey_vector)+'.\n')
        next_vector=Vector(self.predator_vector)
        delta_vector=prey_vector-self.predator_vector

        # 单位方向矢量
        col_vector=Vector(1,0) if delta_vector.x>0 else (Vector(-1,0) if delta_vector.x<0 else Vector(0,0))
        row_vector=Vector(0,1) if delta_vector.y>0 else (Vector(0,-1) if delta_vector.y<0 else Vector(0,0))

        steps=[Vector(self.predator_vector)]# steps记录移动路径

        # 斜向移动
        delta_vector.x=abs(delta_vector.x)
        delta_vector.y=abs(delta_vector.y)
        if delta_vector.x!=0 and delta_vector.y!=0:
            # Col大于Row时，以x方向为基准移动
            if delta_vector.x>delta_vector.y:
                factor=delta_vector.y*2-delta_vector.x# y方向移动因素，大于0时斜向移动，小于0时仅x方向移动
                while next_vector!=prey_vector:
                    if factor>=0:
                        next_vector+=row_vector
                        factor-=delta_vector.x
                    next_vector+=col_vector
                    factor+=delta_vector.y
                    steps.append(Vector(next_vector))

            # Row大于等于Col时，以y方向为基准移动
            else:
                factor=delta_vector.x*2-delta_vector.y# x方向移动因素，大于0时斜向移动，小于0时仅y方向移动
                while next_vector!=prey_vector:
                    if factor>=0:
                        next_vector+=col_vector
                        factor-=delta_vector.y
                    next_vector+=row_vector
                    factor+=delta_vector.x
                    steps.append(Vector(next_vector))

        # 垂直或水平或不移动
        elif delta_vector.x==0:
            while next_vector!=prey_vector:
                next_vector+=row_vector
                steps.append(Vector(next_vector))

        else:
            while next_vector!=prey_vector:
                next_vector+=col_vector
                steps.append(Vector(next_vector))

        if self.max_speed<1:
            step_factor=int(1/self.max_speed-1)# 中间应添加的步骤数
            for i in range(len(steps)-1):# 在原始步骤数组每个元素后添加新添step_factor个步骤数
                n=i+1+i*step_factor
                step_add=[]
                delta_step=(steps[n]-steps[n-1])/(step_factor+1*1.0)
                for j in range(step_factor):
                    step_add.append(Vector(steps[n-1]+delta_step*(j+1)))
                for k in range(step_factor):
                    steps.insert(n+k,Vector(step_add[k]))

        elif self.max_speed>1:
            step_factor=int(self.max_speed-1)# 中间应减去的步骤数
            n=len(steps)//(step_factor+1)# 最终应有步骤数（不包含最后一步）
            dn=len(steps)-n# 应减去的步骤总数（不包含最后一步）
            for i in range(n):
                for j in range(step_factor):
                    if dn:
                        steps.pop(i+1)
                        dn-=1

        if self.test:
            for s in steps:
                self.log_doc.write("STEP:[number]:"+str(self.current_step_num)+'.\n')
                if s is steps[-1]:
                    self.log_doc.write('TEST:[reached end]:'+str(s)+'.\n')
                else:
                    self.log_doc.write('TEST:[not reached]:'+str(s)+'.\n')
                self.current_step_num+=1

        return steps

# 连续移动方式的视线追捕
class Con_pred(object):
    def __init__(self,predator_vector,max_speed,start_speed=0,direction=Vector(1,0),search_range=0,shelter_range=0,friends_range=0,attack_range=0,end_range=0,sensitive=1,test=False):
        self.predator_vector=predator_vector# 追捕者坐标（起始坐标）[vector]
        self.current_vector=self.predator_vector# 追捕者当前坐标（动态）[vector]

        self.max_speed=max_speed# 最大速度(pix/frame)[number]
        self.current_speed=start_speed# 当前速度（动态）[number]

        self.direction=direction# 方向[vector]

        self.shelter_range=shelter_range# 躲避范围半径（躲避障碍物等）[number]
        self.friend_range=friends_range# 队友范围半径（与队友保持距离）[number]
        self.search_range=search_range# 搜索范围半径（视线最大范围）[number]
        self.end_range=end_range# 结束半径，进入结束半径后可减速停止[number]
        if self.end_range<self.max_speed:
            self.end_range=self.max_speed# 结束半径不宜小于self.max_speed
        self.attack_range=attack_range#攻击半径[number]

        self.angle=0# 总转向角{以direction为轴，逆时针（左转）为正，顺时针（右转）为负}[angle]
        self.delta_angle=0# 理论上相对上一次的转向角[angle]
        self.real_delta_angle=0# 实际相对转角

        self.sensitive=sensitive# 灵活度（0~1）[precent]
        self.test=test# 测试模式（无随机数变量，可预测路径）[bool]
        if test:
            self.sensitive=1
            self.comment=""
            self.current_time=time.strftime('%Y-%m-%d-%X',time.localtime())
            self.current_step_num=1

    def precision(self,prec,unit):
        if unit=='number':
            return float('%.4f'%(prec))
        elif unit=='long_number':
            return float('%.10f'%(prec))
        elif unit=='angle':
            angle=float('%.2f'%(prec))
            if angle==0:
                return 0.0
            else:
                return angle
        elif unit=='vector':
            return Vector(self.precision(prec.x,'number'),self.precision(prec.y,'number'))
        elif unit=='direction':
            return Vector(self.precision(prec.get_unit(),'vector'))
        else:
            if self.test:
                self.log_doc.write("ERROR:<precision>:Arguement ERROR!\n")
            exit('Error!')

    def start_test(self):
        if self.test:
            self.log_doc=open('./test_tool/log/Conpred_'+self.current_time+'.log','w')
            if self.comment!="":
                self.log_doc.write("COMMENT:["+str(self.current_time)+"]:"+self.comment+'\n')
            self.log_doc.write("START:<start_test>:Predator's vector is "+str(self.predator_vector)+"; direction is "+str(self.direction)+"; max speed is "+str(self.max_speed)+".\nRANGE:<start_test>:Shelter range is "+str(self.shelter_range)+"; friend range is "+str(self.friend_range)+"; search range is "+str(self.search_range)+"; attack range is "+str(self.attack_range)+"; end range is "+str(self.end_range)+'.\n')

    def end_test(self):
        if self.test:
            self.log_doc.write('END:<end_test>:Total step number is '+str(self.current_step_num-1)+"; total angle is "+str(self.angle)+'.\n')
            self.log_doc.close()

    def turn_speed(self):# 转向速度
        speed=2/3.0*self.current_speed
        speed=self.precision(speed,'number')
        if self.test:
            self.log_doc.write("BACKTRACK:<turn_speed>:Turn speed is "+str(speed)+'.\n')
        return speed

    def direction_angle(self,vector):# 判断self.direction到vector的角度角，从self.direction出发逆时针（左转）为正，顺时针（右转）为负
        self.delta_angle=self.direction.get_theta_with_sign(vector)
        self.delta_angle=self.delta_angle=self.precision(self.delta_angle,'angle')
        return True

    def turn_direct(self,direct):# direct['left','right','straight'],转换为与self.direction垂直的direct向量
        if direct=='left':
            vector=self.direction.get_left()
            return self.precision(vector,'vector')
        elif direct=='right':
            vector=self.direction.get_right()
            return self.precision(vector,'vector')
        elif direct=='straight':
            return Vector(0,0)
        else:
            if self.test:
                self.log_doc.write("ERROR:<turn_direct>:Direction ERROR!\n")
            exit('Error!')

    def accelerate(self,end_speed,factor):# 加速模式
        self.current_speed+=(end_speed-self.current_speed)/(factor*1.0)
        if self.current_speed<0:
            self.current_speed=0.0
        else:
            self.current_speed=self.precision(self.current_speed,'number')

        if self.test:
            self.log_doc.write("BACKTRACK:<accelerate>:Current speed is "+str(self.current_speed)+'.\n')
        return True

    def gear_box(self,speed_rank='middle'):# 变速箱（低、中、高档，减速，刹车），返回速度[number]
        if self.test:
            self.log_doc.write("BACKTRACK:<gear_box>:Speed rank is "+speed_rank+'.\n')
            r=1
        else:
            r=(random.random()*0.1+0.9)*self.sensitive


        if speed_rank=='low':
            self.accelerate(self.max_speed*1/3.0*r,200)
            return True
        elif speed_rank=='middle':
            self.accelerate(self.max_speed*2/3.0*r,150)
            return True
        elif speed_rank=='high':
            self.accelerate(self.max_speed*r,100)
            return True
        elif speed_rank=='slow_down':
            self.accelerate(0,500)
            return True
        elif speed_rank=='brake':
            if self.current_speed>self.max_speed*1/3.0:
                s=-3
            elif self.current_speed>self.max_speed*2/3.0:
                s=-6
            else:
                s=-9
            self.accelerate(s,10)
            return True
        else:
            if self.test:
                self.log_doc.write('ERROR:<gear box>:Argument ERROR!\n')
            exit()

    def rudder(self):# 方向控制，返回转向后方向[vector]
        if self.delta_angle==0.0:# straight
            turn_direction='straight'
        elif self.delta_angle<0.0 and self.delta_angle>=-180.0:# right
            turn_direction='right'
        elif self.delta_angle>0.0 and self.delta_angle<=180.0:# left
            turn_direction='left'
        else:
            if self.test:
                self.log_doc.write('ERROR:<rudder>:Angle OUT OF RANGE!\n')
            exit('Error!')

        direct=self.turn_direct(turn_direction)
        acceletration=direct*self.turn_speed()

        if abs(self.delta_angle)>90:# 最大转向角转向
            r=1
        else:
            r=abs(self.delta_angle/90.0)

        if not self.test:
            r*=(random.random()*0.1+0.9)*self.sensitive

        acceletration=self.precision(acceletration*r,'vector')

        scale=acceletration.get_length()/self.direction.get_length()
        scale=self.precision(scale,'long_number')
        self.real_delta_angle=math.atan(scale)/math.pi*180
        self.real_delta_angle=self.precision(self.real_delta_angle,'angle')

        if turn_direction=='right':
            self.real_delta_angle*=-1

        self.angle+=self.real_delta_angle

        if self.test:
            self.log_doc.write("BACKTRACK:<rudder>:Turn "+turn_direction+"; angle factor is "+str(r)+"; current direction is "+str(self.direction)+"; rudder to "+str(acceletration)+'.\n')
            self.log_doc.write("ANGLE:<rudder>:Theoretic delta angle is "+str(self.delta_angle)+"; real delta angle is "+str(self.real_delta_angle)+"; total angle is "+str(self.angle)+'.\n')

        self.direction=acceletration+self.direction# 合成方向
        self.direction=self.precision(self.direction,'direction')

        return True

    # 追捕
    def hunt(self,prey_vector,speed_model='high',return_list=False):
        self.log_doc.write("HUNT:<Con_pred hunt>:Prey's vector is "+str(prey_vector)+"; speed model is "+speed_model+"; return list? "+str(return_list)+'.\n')
        # prey_vector 终点（猎物）坐标[vector]
        # speed_model 速度模式（gear_box function）['high','middle','low','slow_down','brake']
        # return_list 返回形式（返回路径所有坐标[list]，适用于静态目标模式；或返回下一个坐标[vector]，适用于动态目标模式）[bool]
        next_vector=[]

        def routin():
            self.gear_box(speed_model)
            delta_vector=prey_vector-self.current_vector# 起点到终点的矢量
            self.direction_angle(delta_vector)
            self.rudder()# 转向
            self.current_vector+=self.direction*self.current_speed
            return True

        def reach_end():
            if Vector(self.current_vector-prey_vector).get_length()<=self.end_range:
                return True
            else:
                return False

        if return_list:
            while not reach_end():
                routin()
                if self.test:
                    self.log_doc.write("STEP:[number]:"+str(self.current_step_num)+'.\n')
                    self.log_doc.write('TEST:[not reached]:'+str(self.current_vector)+'.\n')
                    self.current_step_num+=1
                next_vector.append(Vector(self.current_vector))

            speed_model='brake'
            while self.current_speed!=0:
                routin()
                if self.test:
                    self.log_doc.write("STEP:[number]:"+str(self.current_step_num)+'.\n')
                    self.log_doc.write('TEST:[reached end]:'+str(self.current_vector)+'.\n')
                    self.current_step_num+=1
                next_vector.append(Vector(self.current_vector))

            return next_vector

        else:
            if reach_end():
                speed_model='brake'
            routin()
            if self.test:
                self.log_doc.write("STEP:[number]:"+str(self.current_step_num)+'.\n')
                if speed_model!='brake':
                    self.log_doc.write('TEST:[not reached]:'+str(self.current_vector)+'.\n')
                else:
                    self.log_doc.write('TEST:[reached end]:'+str(self.current_vector)+'.\n')
                self.current_step_num+=1
            return self.current_vector

    # 拦截
    def intercept(self,prey_vector,prey_direction,prey_speed,speed_model='high'):
        self.log_doc.write("INTE:<intercept>:Prey's vector is "+str(prey_vector)+"; prey's direction is "+str(prey_direction)+"; prey's speed is "+str(prey_speed)+"; speed model is "+speed_model+'.\n')
        # prey_vector 终点（猎物）坐标[vector]
        # prey_direction 猎物行驶方向[vector]
        # prey_speed 猎物行驶速度[number]
        # speed_model 速度模式（gear_box function）['high','middle','low','slow_down','brake']
        delta_vector=prey_vector-self.current_vector
        delta_speed=abs(prey_speed-self.current_speed)
        last_final_vector=prey_vector

        if delta_speed!=0:
            time=delta_vector.get_length()/delta_speed
            final_vector=prey_vector+prey_direction*prey_speed*time
            last_final_vector=final_vector
        else:
            final_vector=last_final_vector

        self.hunt(final_vector,speed_model,False)

        return self.current_vector

