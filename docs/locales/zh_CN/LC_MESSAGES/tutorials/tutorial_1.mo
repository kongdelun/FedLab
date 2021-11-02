��          |               �      �      �   �         &   *  4   Q  :   �  v   �  i   8  �   �  �   0  w       �     �  �  �  !   �	  '   �	  S   �	  `   >
  W   �
  k   �
  �   c  �   "   Check the available ethernet: Distributed Communication FedLab uses `torch.distributed <https://pytorch.org/docs/stable/distributed.html>`_ as point-to-point communication package. The communication backend is Gloo as default. FedLab processes send/receive data through TCP network connection. If the automatically detected interface is not correct, you need to choose the network interface to use for Gloo, by setting the environment variables ``GLOO_SOCKET_IFNAME``, for example ``export GLOO_SOCKET_IFNAME=eth0`` or ``os.environ['GLOO_SOCKET_IFNAME'] = "eth0"``. How to create package? How to initialize distributed network? Make sure ``world_size`` is the same across process. Rank should be different (from ``0`` to ``world_size-1``). The ``(server_ip, server_port)`` is the address of server. please be aware of that the rank of server is 0 as default. The ``ethernet_name`` must be checked (using ``ifconfig``). Otherwise, network initialization would fail. The ethernet can be None, torch.distributed will try to find the right ethernet. If it doesn't work, user need to assign right ethernet name. You need to assign right ethernet to :class:`DistNetwork`, making sure ``torch.distributed`` network initialization works. :class:`DistNetwork` is for quickly network configuration, which you can create one as follows: Project-Id-Version: FedLab 
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2021-10-30 17:11+0800
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: zh_CN
Language-Team: zh_CN <LL@li.org>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.9.0
 检查可用的以太网： 分布式通信 FedLab 基于 `torch.distributed <https://pytorch.org/docs/stable/distributed.html>`_ 实现了点对点通信模块。 默认Gloo为分布式通信后端。 FedLab 进程通过TCP网络连接发送/接收数据。 如果自动使用的以太网接口错误，则需要用户设置环境变量 ``GLOO_SOCKET_IFNAME`` 的方式，手动指定正确的以太网口。比如在终端运行 ``export GLOO_SOCKET_IFNAME=eth0`` 或者在Python代码中 ``os.environ['GLOO_SOCKET_IFNAME'] = "eth0"`` 。 如何创建一个FedLab通信包 如何初始化分布式通信网络？ 保证所有进程上的 :class:`DistNetwork` 的 ``world_size`` 值是一致的。 任意两个进程的rank应该不同，可选的rank号应该为 ``0`` 到 ``world_size-1`` 。 ``(server_ip, server_port)`` 是服务器端的ip地址。服务端的rank默认为0。 务必在终端运行指令 ``ifconfig`` 检查可用的以太网接口。否则网络初始化会失败。  ``ethernet`` 可以设置为None， ``torch.distributed`` 会尝试搜索正确的网络以太网接口。如果默认时，网络初始化失败，可以尝试手动指定 ``ethernet`` 。 用户需要正确初始化 :class:`DistNetwork` 来保证 ``torch.distributed`` 的网络通信连接成功。可以通过一下方式来创建一个正确的 :class:`DistNetwork` 。 