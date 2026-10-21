# P1 - Sistema de saludo y contador en ROS2

## 1. Descripcion

He creado un unico paquete `ament_python` llamado `p1_contador` con dos nodos:

- `publicador_saludo`: publica un `std_msgs/String` en `/saludo` una vez por segundo.
- `contador_nodo`: se suscribe a `/saludo`, cuenta los mensajes recibidos y publica el total en `/contador` como `std_msgs/Int32`.

El nodo `contador_nodo` tambien incorpora:

- servicio `/reiniciar_contador` (`std_srvs/srv/Trigger`),
- parametro dinamico `umbral` (valor inicial 10),
- QoS de `/contador`: `RELIABLE + TRANSIENT_LOCAL`, profundidad 10.

## 2. Compilacion

Desde la raiz del workspace:

```bash
cd ~/p1_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Si se abre una terminal nueva hay que volver a ejecutar:

```bash
source /opt/ros/jazzy/setup.bash
source ~/p1_ws/install/setup.bash
```

## 3. Ejecucion

Terminal 1:

```bash
ros2 run p1_contador publicador_saludo
```

Terminal 2:

```bash
ros2 run p1_contador contador_nodo
```

## 4. Pruebas

### Nodos y topics

```bash
ros2 node list
ros2 topic list
ros2 topic echo /saludo
```

### Contador

Para comprobar `/contador` con el mismo QoS que ofrece el publicador:

```bash
ros2 topic echo /contador std_msgs/msg/Int32 --qos-reliability reliable --qos-durability transient_local
```

### Servicio de reinicio

```bash
ros2 service call /reiniciar_contador std_srvs/srv/Trigger "{}"
```

### Parametro `umbral`

Consultar:

```bash
ros2 param get /contador_nodo umbral
```

Cambiarlo en caliente, por ejemplo a 5:

```bash
ros2 param set /contador_nodo umbral 5
```

Al alcanzar el valor 5 aparece un mensaje WARN sin reiniciar el nodo.

### Comprobar QoS

```bash
ros2 topic info /contador --verbose
```

Debe aparecer `RELIABLE`, `TRANSIENT_LOCAL` y profundidad 10.

### Suscriptor tardio

1. Mantengo `publicador_saludo` y `contador_nodo` ejecutandose.
2. Espero a que `/contador` tenga un valor mayor que 0.
3. Abro una terminal nueva, hago `source` y ejecuto:

```bash
ros2 topic echo /contador std_msgs/msg/Int32 --qos-reliability reliable --qos-durability transient_local
```

Aunque el `echo` se haya iniciado tarde, recibe inmediatamente el ultimo valor almacenado porque el publicador usa `TRANSIENT_LOCAL`.

### Grafo

```bash
rqt_graph
```

## 5. Decisiones de diseno

He separado cada responsabilidad en un nodo distinto: un nodo solo genera los saludos y el otro gestiona el conteo, el servicio, el parametro y la publicacion de `/contador`.

Para el parametro `umbral`, leo su valor en cada callback de `/saludo`. De esta forma cualquier cambio hecho con `ros2 param set` se aplica sin reiniciar el nodo.

En el servicio de reinicio, ademas de poner el contador a cero, publico inmediatamente el valor `0` en `/contador`. Asi el estado publicado siempre coincide con el estado interno del nodo.

Para `/contador` he utilizado exactamente el QoS solicitado: `RELIABLE + TRANSIENT_LOCAL` y profundidad 10. `RELIABLE` prioriza la entrega y `TRANSIENT_LOCAL` permite que un suscriptor que se conecte tarde reciba el ultimo valor conservado por el publicador.
