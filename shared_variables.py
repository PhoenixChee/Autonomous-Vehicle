# Shared Global Variables/GenerateData

controlCloseloop = False

odrive_dic = {
	'battery_voltage': 0,
	'control_mode': 0,
	'm0_state': '-',
	'm1_state': '-',
	'm0_velocity': 0, 
	'm1_velocity': 0,
	'm0_current': 0,
	'm1_current': 0,
	'm0_calibration': 0, 
	'm1_calibration': 0,
	'watchdog_timer': 0,
 	'a1_system_error': '-',
 	'a0_system_error': '-',
	'a0_motor_error': '-',
 	'a1_motor_error': '-',
	'a0_controller_error': '-',
	'a1_controller_error': '-',
 	'a0_encoder_error': '-',
	'a1_encoder_error': '-'
}

steer_dic = {
	'steer_angle': 0,
 }

temperature_dic = {
 	'sensor_0': 0,
	'sensor_1': 0,
	'sensor_2': 0,
	'sensor_3': 0,
	'sensor_4': 0,
	'sensor_5': 0
 }

ultrasonic_dic = {
	'ultrasonic_0': 0,
	'ultrasonic_1': 0, 
	'ultrasonic_2': 0,
	'stop': 0
}
