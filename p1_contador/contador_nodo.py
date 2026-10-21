import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import String, Int32
from std_srvs.srv import Trigger


class ContadorNodo(Node):
    def __init__(self):
        super().__init__('contador_nodo')

        self.contador = 0

        # R4: declaro el parametro con valor por defecto 10.
        # Leo su valor en cada mensaje para que ros2 param set tenga efecto en caliente.
        self.declare_parameter('umbral', 10)

        # R5: /contador usa RELIABLE + TRANSIENT_LOCAL con profundidad 10.
        qos_contador = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )

        self.publicador_contador = self.create_publisher(
            Int32,
            'contador',
            qos_contador,
        )

        # R2: me suscribo a /saludo y cuento cada mensaje recibido.
        self.suscripcion_saludo = self.create_subscription(
            String,
            'saludo',
            self.cb_saludo,
            10,
        )

        # R3: creo el servicio que reinicia el contador.
        self.servicio_reinicio = self.create_service(
            Trigger,
            'reiniciar_contador',
            self.cb_reiniciar,
        )

        # Publico el estado inicial para que /contador empiece en 0.
        self.publicar_contador()

        self.get_logger().info(
            'contador_nodo iniciado. Contador=0, umbral=10.'
        )

    def publicar_contador(self):
        mensaje = Int32()
        mensaje.data = self.contador
        self.publicador_contador.publish(mensaje)

    def cb_saludo(self, msg):
        self.contador += 1
        self.publicar_contador()

        self.get_logger().info(
            f'Recibido: "{msg.data}" -> contador={self.contador}'
        )

        # El parametro se consulta en cada callback para aceptar cambios en caliente.
        umbral = self.get_parameter('umbral').value

        if self.contador == umbral:
            self.get_logger().warn(
                f'El contador ha alcanzado el umbral configurado ({umbral}).'
            )

    def cb_reiniciar(self, request, response):
        self.contador = 0
        self.publicar_contador()

        response.success = True
        response.message = 'Contador reiniciado correctamente a 0.'

        self.get_logger().info('Contador reiniciado a 0 mediante el servicio.')
        return response


def main(args=None):
    rclpy.init(args=args)
    nodo = ContadorNodo()

    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
