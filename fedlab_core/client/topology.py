import torch
import torch.distributed as dist
from torch.multiprocessing import Process

from fedlab_core.utils.messaging import send_message, recv_message, MessageCode
from fedlab_core.utils.logger import logger


class ClientCommunicationTopology(Process):
    """Abstract class

    If you want to define your own Network Topology, please be sure your class should subclass it and OVERRIDE its
    methods.

    Example:
        please read the code of :class:`ClientSyncTop`
    """

    def __init__(self, backend_handler, server_addr, world_size, rank, dist_backend):
        self._backend = backend_handler

        self.rank = rank
        self.server_addr = server_addr
        self.world_size = world_size
        self.dist_backend = dist_backend

        dist.init_process_group(backend=dist_backend, init_method='tcp://{}:{}'
                                .format(self.server_addr[0], self.server_addr[1]),
                                rank=self.rank, world_size=self.world_size)

    def run(self):
        """Please override this function"""
        raise NotImplementedError()

    def on_receive(self, sender, message_code, payload):
        """Please override this function"""
        raise NotImplementedError()

    def synchronize(self, payload):
        """Please override this function"""
        raise NotImplementedError()


class ClientSyncTop(ClientCommunicationTopology):
    """Synchronise communication class

    This is the top class in our framework which is mainly responsible for network communication of CLIENT!
    Synchronize with server following agreements defined in :meth:`run`.

    Args:
        backend_handler: Subclass of ClientBackendHandler, manages training and evaluation of local model on each
        client.
        server_addr (str): address of server in form of ``"[SERVER_ADDR]:[SERVER_IP]"``
        world_size (int): Number of client processes participating in the job for ``torch.distributed`` initialization
        rank (int): Rank of the current client process for ``torch.distributed`` initialization
        dist_backend (str or Backend): :attr:`backend` of ``torch.distributed``. Valid values include ``mpi``, ``gloo``,
        and ``nccl``. Default: ``"gloo"``
        logger_file (str, optional): Path to the log file for all clients of :class:`ClientSyncTop` class. Default: ``"clientLog"``
        logger_name (str, optional): Class name to initialize logger

    Raises:
        Errors raised by :func:`torch.distributed.init_process_group`

    Example:
        TODO
    """

    def __init__(self, backend_handler, server_addr, world_size, rank, dist_backend="gloo", logger_file="clientLog",
                 logger_name=""):

        super(ClientSyncTop, self).__init__(backend_handler,
                                            server_addr, world_size, rank, dist_backend)

        self._LOGGER = logger(logger_file + str(rank) + ".txt", logger_name)
        self._LOGGER.info(
            "Successfully Initialized --- connected to server:{},  world size:{}, rank:{}, backend:{}".format(
                server_addr, world_size, rank, dist_backend))

        self._buff = torch.zeros(
            self._backend.buffer.numel() + 2).cpu()  # TODO: need to be more formal

    def run(self):
        """Main procedure of each client is defined here:
            1. client waits for data from server
            2. after receiving data, client will train local model
            3. client will synchronize with server actively
        """

        while True:
            # waits for data from
            # TODO: whether this step can be wrapped?
            self._LOGGER.info("waiting message from server")
            recv_message(self._buff, src=0)  # 阻塞式

            # parse the received data
            # TODO: 通信消息解析可模块化
            sender = int(self._buff[0].item())
            message_code = MessageCode(self._buff[1].item())
            parameter = self._buff[2:]

            if message_code == MessageCode.Exit:
                exit(0)

            # perform local training
            self.on_receive(sender, message_code, parameter)

            # synchronize with server
            self.synchronize(self._backend.buffer)

    def on_receive(self, sender, message_code, payload):
        """Actions to perform on receiving new message, including local training

        Args:
            sender (int): Rank of sender
            message_code: Agreements code defined in :class:`MessageCode` class
            payload: Serialized model parameters

        Returns:
            None

        Raises:
            None
        """
        self._LOGGER.info("receiving message from {}, message code {}".format(
            sender, message_code))

        self._backend.buffer = payload
        self._backend.train(epochs=2)

    def synchronize(self, buffer):
        """Synchronize local model with server actively

        Args:
            buffer: Serialized model parameters

        Returns:
            None

        Raises:
            None
        """
        self._LOGGER.info("synchronize model parameters with server")
        send_message(MessageCode.ParameterUpdate, buffer)
