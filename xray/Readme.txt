


# 确保准备好文件
# 配置文件
/root/xray/config.json
# 导入新连接的模板
/root/xray/inbound.json
# xray程序
/root/xray/xray-linux-amd64




# 创造工作目录
mkdir /root/xray/

# 进入目录
cd /root/xray






# 让xray可执行
chmod +x /root/xray/xray-linux-amd64


# 试下运行
./xray-linux-amd64 run -config config.json


# 生成每次唯一UUID防止重复，重复也没事其实
./xray-linux-amd64 uuid

# 试下导入新的连接配置，xray不会储存的
./xray-linux-amd64 api adi --server 127.0.0.1:1270 inbound.json





# 查看 端口 哪些IP正在连接状态 是否超过1分钟无人连接
ss -antp | grep ':8096' | grep ESTAB

确认端口已经一分钟没有被连接，就查看端口是否正在被占用，被哪个程序占用
ss -ltnp | grep ':8096'


# xray 删除指定端口 配置文件 也就是删除指定端口 删除整个vmess 释放端口出来
./xray-linux-amd64 api rmi --server 127.0.0.1:1270 inbound-8096




# 让xray变成系统服务更方便
tee /etc/systemd/system/xray.service <<EOF
[Unit]
Description=Xray Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/xray
ExecStart=/root/xray/xray-linux-amd64 run -config /root/xray/config.json
Restart=on-failure  # 崩溃时自动重启
RestartSec=3s       # 重启前等待 3 秒

[Install]
WantedBy=multi-user.target  # 随系统启动
EOF


# 然后执行
systemctl daemon-reload
systemctl start xray
systemctl enable xray

# 重新启动
systemctl daemon-reload

# 查看运行状态
systemctl status xray


# 让它随着系统启动
systemctl enable xray
















# 其他
# 获取下载流量
 ./xray-linux-amd64 api stats --name="inbound>>>api>>>traffic>>>downlink" --server=127.0.0.1:1270

# 随机获取一个未被占用的端口
while true;do PORT=$(shuf -i 2000-64999 -n 1);if ! ss -ltn | grep -q ":$PORT\b";then echo "$PORT";break;fi;done















