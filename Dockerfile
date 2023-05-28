FROM centos:latest
LABEL Waxia Myer

RUN cd /etc/yum.repos.d/ \
    && sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* \
    && sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

ENV PYTHONUNBUFFERED 1

# Install necessary packages
RUN yum -y update \
    && yum -y install iproute bash-completion iputils \
    && yum -y install epel-release \
    && yum -y install python3 python3-pip \
    && yum clean all

# Copy the requirements file to /tmp
COPY requirements.txt /tmp/

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app
COPY ./app/templates /app/templates
WORKDIR /app
EXPOSE 8000

# Set the entrypoint command
CMD [ "python3", "ip_file.py" ]
