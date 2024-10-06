import paho.mqtt.client as mqtt

import threading
from django.conf import settings
from core.logger import logger
from home.models import Device, Home
from notifications.models import Notification
import json
import paho.mqtt.subscribe as subsribde
    
class Smarthome(threading.Thread):
    def callback(self, client, userdata, message):
        logger.info("Callback triggered")
        logger.info(f"Message received: {message.payload}")

        data = json.loads(message.payload)
        home_id = data.pop('i')
        
        home = Home.objects.get(id=home_id)
        output_data = []

        gas = data.pop('g', None)  # Thêm tham số mặc định là None
        humidity = data.pop('h', None)
        temperature = data.pop('t', None)

        # Xử lý gas
        try:
            gas_device = Device.objects.get(type__name='gas', room__home__id=home_id)
            old_gas_value = gas_device.value
            logger.info(f"old_gas_value: {old_gas_value}")

            if gas is not None:
                logger.info(f"homeId: {home_id}, gas_device: {gas_device}")
                gas_device.value = gas
                gas_device.save()
                output_data.append({
                    "device_id": gas_device.id.__str__(),
                    "type": gas_device.type.name,
                    "value": gas,
                })
        except Device.DoesNotExist:
            logger.error(f"Gas device not found for home_id {home_id}")

        # Xử lý humidity nếu có
        if humidity is not None:
            try:
                humidity_device = Device.objects.get(type__name='humidity', room__home__id=home_id)
                logger.info(f"homeId: {home_id}, humidity_device: {humidity_device}")
                humidity_device.value = humidity
                humidity_device.save()
                output_data.append({
                    "device_id": humidity_device.id.__str__(),
                    "type": humidity_device.type.name,
                    "value": humidity,
                })
            except Device.DoesNotExist:
                logger.error(f"Humidity device not found for home_id {home_id}")

        # Xử lý temperature nếu có
        try:
            temperature_device = Device.objects.get(type__name='temperature', room__home__id=home_id)
            old_temp_value = temperature_device.value
            logger.info(f"old_temp_value: {old_temp_value}")

            if temperature is not None:
                logger.info(f"homeId: {home_id}, temperature_device: {temperature_device}")
                temperature_device.value = temperature
                temperature_device.save()
                output_data.append({
                    "device_id": temperature_device.id.__str__(),
                    "type": temperature_device.type.name,
                    "value": temperature,
                })
        except Device.DoesNotExist:
            logger.error(f"Temperature device not found for home_id {home_id}")

        # Xử lý các thiết bị khác
        for k, v in data.items():
            try:
                # Kiểm tra nếu v là một dictionary và lấy giá trị v
                if isinstance(v, dict):
                    value = v.get('v', None)  # Lấy giá trị 'v'
                    is_auto = v.get('a', None)  # Lấy giá trị 'a'
                else:
                    logger.warning(f"Unexpected data format for device {k}: {v}")
                    continue

                device = Device.objects.get(id=k)
                device.value = 1 if value == 0 else 0  # Thay đổi theo quy luật
                device.is_auto = bool(is_auto)  # Chuyển đổi thành boolean
                device.save()
                output_data.append({
                    "device_id": k,
                    "type": device.type.name,
                    "value": 1 if value == 0 else 0,
                })
            except Device.DoesNotExist:
                logger.warning(f"Device with id {k} does not exist.")
            except Exception as e:
                logger.error(f"Error updating device {k}: {e}")

        notification_data = {
            "data": json.dumps(output_data),
        }
        string_data = json.dumps(notification_data)
        logger.info(f"Notification string data: {output_data}")
        notification = Notification(
            data=string_data,
            user_id=home.user.id
        )
        
        # Kiểm tra và gửi thông báo nếu cần
        if old_gas_value is not None and gas is not None and old_gas_value <= settings.GAS_MIN and gas > settings.GAS_MIN:
            notification.title = 'Gas Leak'
            notification.body = 'Gas Leak Detected'
            notification.save()
        
        if old_temp_value is not None and temperature is not None and old_temp_value <= settings.TEMP_MIN and temperature > settings.TEMP_MIN:
            notification.title = 'Temperature High'
            notification.body = 'Temperature High Detected'
            notification.save()
        
        notification.send()




    def run(self):
        subsribde.callback(callback=self.callback, topics=settings.MQTT_TOPIC, qos=0,hostname=settings.MQTT_SERVER,
           port=settings.MQTT_PORT, client_id="", keepalive=60, will=None, auth=settings.MQTT_AUTH,
           tls=settings.MQTT_TLS)
        
        subsribde.loop_start()