=====================================
ssh访问远程tensorboard

本机运行：
ssh -L 16006:127.0.0.1:6006 zzydty@172.29.244.218 -N -v -v

远端运行：
nohup tensorboard --logdir=./ --port=6006 --samples_per_plugin scalars=999999999

本地浏览器访问：
http://localhost:16006

如果要重新运行，可以用以下指令杀死6006端口上的进程：
fuser -k 6006/tcp

========================================
Nohup：在ssh断开的情况下也能跑程序
删除上次的记录：
rm nohup.out

用nohup 运行一个python文件
nohup python3 -u train.py > nohup.out 2>&1 &

然后输入以下命令，这样程序就不会被终端影响，可以在后台运行，并且不会被杀死
disown

想要实时看到输出结果就再写一行代码
tail -fn 50 nohup.out

查看后台进程的PID：
ps

如果关闭了命令行，可以这样查看进程PID：
ps aux | grep "train.py"

终止进程：
kill -9 PID
