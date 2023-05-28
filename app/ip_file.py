'''
This Script was created by Waxia Myer, May 2006
@Author Waxia Myer
'''

from flask import Flask, render_template
import socket
import os
import random




app = Flask(__name__)
os.environ['FLASK_APP'] = 'ip_file.py'
os.environ['FLASK_ENV'] = 'development'

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

        return render_template('display_ip.html', ip_address=ip_address, bg_color=bg_color)

else:
    @app.route('/')
    def container_show_ip():
        return render_template('display_ip.html', ip_address=None)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)


