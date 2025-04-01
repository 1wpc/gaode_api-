# -*- coding: utf-8 -*-
"""
高德地图导航程序

这个程序使用高德地图API实现步行导航功能，包括地址转换为经纬度坐标、
获取步行导航路线信息、展示导航指令和路线详情。
"""

import requests
import json
import sys

class AmapNavigation:
    def __init__(self, api_key):
        """
        初始化导航类
        
        Args:
            api_key: 高德地图API密钥
        """
        self.api_key = api_key
        self.geocode_url = "https://restapi.amap.com/v3/geocode/geo"
        self.walking_url = "https://restapi.amap.com/v5/direction/walking"
    
    def geocode(self, address):
        """
        将地址转换为经纬度坐标
        
        Args:
            address: 地址字符串
            
        Returns:
            成功返回经纬度坐标(经度,纬度)，失败返回None
        """
        params = {
            'key': self.api_key,
            'address': address
        }
        
        try:
            response = requests.get(self.geocode_url, params=params)
            result = response.json()
            
            if result['status'] == '1' and result['count'] != '0':
                location = result['geocodes'][0]['location']
                return location
            else:
                print(f"地址转换失败: {address}")
                print(f"错误信息: {result}")
                return None
        except Exception as e:
            print(f"地址转换异常: {e}")
            return None
    
    def get_walking_navigation(self, origin, destination):
        """
        获取步行导航路线信息
        
        Args:
            origin: 起点坐标(经度,纬度)
            destination: 终点坐标(经度,纬度)
                
        Returns:
            成功返回步行导航路线信息，失败返回None
        """
        params = {
            'key': self.api_key,
            'origin': origin,
            'destination': destination,
            'show_fields': 'cost,navi,polyline'  # 返回详细信息
        }
        
        try:
            response = requests.get(self.walking_url, params=params)
            result = response.json()
            
            if result['status'] == '1':
                return result
            else:
                print(f"获取步行导航路线失败")
                print(f"错误信息: {result}")
                return None
        except Exception as e:
            print(f"获取步行导航路线异常: {e}")
            return None
    
    def display_walking_navigation(self, nav_result):
        """
        展示步行导航指令和路线详情
        
        Args:
            nav_result: 步行导航路线信息
        """
        if not nav_result or 'route' not in nav_result:
            print("没有可用的步行导航信息")
            return
        
        route = nav_result['route']
        paths = route['paths'][0]  # 取第一条路径
        
        # 显示基本信息
        print("\n=== 步行导航路线信息 ===")
        print(f"总距离: {int(paths['distance'])/1000:.1f} 公里")
        
        # 如果返回了cost信息
        if 'cost' in paths:
            print(f"预计耗时: {int(paths['cost']['duration'])/60:.1f} 分钟")
        
        # 显示详细导航步骤
        print("\n=== 步行导航指令 ===")
        steps = paths['steps']
        for i, step in enumerate(steps, 1):
            instruction = step['instruction']
            road_name = step.get('road_name', '未命名道路')
            step_distance = int(step['step_distance'])
            
            # 显示导航动作指令（如果有）
            action_info = ""
            if 'navi' in step:
                action = step['navi'].get('action', '')
                if action:
                    action_info = f"动作: {action}"
            
            print(f"\n步骤 {i}: {instruction}")
            print(f"  道路名称: {road_name}")
            print(f"  距离: {step_distance} 米")
            if action_info:
                print(f"  {action_info}")


def main():
    # 用户需要替换为自己的高德地图API密钥
    api_key = "a06cea233db84d92bf07731050dcdada"
    
    # 创建导航对象
    nav = AmapNavigation(api_key)
    
    print("欢迎使用高德地图步行导航程序!")
    print("请输入起点和终点地址，程序将为您规划最佳步行路线。")
    
    # 获取起点和终点地址
    origin_address = input("请输入起点地址: ")
    destination_address = input("请输入终点地址: ")
    
    # 将地址转换为坐标
    print("\n正在转换地址为坐标...")
    origin_location = nav.geocode(origin_address)
    if not origin_location:
        print("起点地址无法识别，程序退出")
        return
    
    destination_location = nav.geocode(destination_address)
    if not destination_location:
        print("终点地址无法识别，程序退出")
        return
    
    print(f"起点坐标: {origin_location}")
    print(f"终点坐标: {destination_location}")
    
    # 获取步行导航路线
    print("\n正在获取步行导航路线...")
    nav_result = nav.get_walking_navigation(origin_location, destination_location)
    
    if nav_result:
        # 展示步行导航指令
        nav.display_walking_navigation(nav_result)
    else:
        print("获取步行导航路线失败，请检查网络连接和API密钥是否正确")


if __name__ == "__main__":
    main()