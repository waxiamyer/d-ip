'''
This Script was created by Wasia Maya, May 2006
@Author Wasia Maya
'''

from flask import Flask, render_template
import socket
import os
import random
import webcolors

app = Flask(__name__)
os.environ['FLASK_APP'] = 'ip_file.py'
os.environ['FLASK_ENV'] = 'development'

# List of color names
COLOR_NAMES = list(webcolors.CSS3_NAMES_TO_HEX.keys())

def rgb_distance(color1, color2):
    return sum((a - b) ** 2 for a, b in zip(color1, color2))

def get_closest_color_name(hex_color_code):
    try:
        # Convert the hexadecimal color code to RGB values
        rgb_color = webcolors.hex_to_rgb(hex_color_code)
        rgb_tuple = (rgb_color.red, rgb_color.green, rgb_color.blue)
        
        # Calculate the closest named color based on RGB distance
        closest_color = min(COLOR_NAMES, key=lambda name: rgb_distance(rgb_tuple, webcolors.hex_to_rgb(webcolors.CSS3_NAMES_TO_HEX[name])))
        
        return closest_color
    except ValueError:
        return "Unknown Color"

def get_ip_address():
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Connect to a public DNS server to retrieve the IP address
        sock.connect(("8.8.8.8", 80))
        ip_address = sock.getsockname()[0]
        return ip_address
    except Exception as e:
        print("Error occurred:", str(e))
    finally:
        sock.close()

def is_valid_ip(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
        return True
    except socket.error:
        pass

    try:
        socket.inet_pton(socket.AF_INET6, address)
        return True
    except socket.error:
        pass

    return False


def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

get_ip = get_ip_address()
previous_ip = None
bg_color = None


if is_valid_ip(get_ip):
    @app.route('/')
    def container_show_ip():
        """Application GUI to display the IP"""

        global previous_ip, bg_color

        ip_address = get_ip_address()

        if ip_address != previous_ip:
            bg_color = generate_random_color()
            previous_ip = ip_address
	
        # Create the color_file in /tmp folder and write bg_color to it
        with open('/tmp/color_file.txt', 'w') as file:
            color_name = get_closest_color_name(bg_color)
            file.write(color_name)

        return render_template('display_ip.html', ip_address=ip_address, bg_color=bg_color)

else:
    @app.route('/')
    def container_show_ip():
        return render_template('display_ip.html', ip_address=None)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)


