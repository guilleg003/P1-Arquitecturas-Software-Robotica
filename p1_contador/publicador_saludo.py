import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublicadorSaludo(Node):
    def __init__(self):
        super().__init__('publicador_saludo')

        # Creo el publicador del topic /saludo con una cola de 10 mensajes.
        self.publicador = self.create_publisher(String, 'saludo', 10)

        # Publico un mensaje cada segundo.
        self.timer = self.create_timer(1.0, self.publicar_saludo)
        self.contador = 0

    def publicar_saludo(self):
        mensaje = String()
        mensaje.data = f'Hola desde ROS2, mensaje numero {self.contador}'
        self.publicador.publish(mensaje)
        self.get_logger().info(f'Publico: "{mensaje.data}"')
        self.contador += 1


def main(args=None):
    rclpy.init(args=args)
    nodo = PublicadorSaludo()

    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
