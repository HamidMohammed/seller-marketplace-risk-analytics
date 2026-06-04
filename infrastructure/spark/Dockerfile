# FROM apache/spark:3.5.3

# USER root

# RUN apt-get update && \
#     apt-get install -y wget && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /opt/spark

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY conf/spark-defaults.conf \
#      /opt/spark/conf/spark-defaults.conf

# COPY jars/ /opt/spark/jars/

# USER spark

# FROM apache/spark:3.5.3

# USER root

# RUN mkdir -p /opt/spark/jobs

# COPY jars/ /opt/spark/jars/

# COPY conf/spark-defaults.conf \
#      /opt/spark/conf/spark-defaults.conf

# USER spark

FROM apache/spark:3.5.3

USER root

RUN mkdir -p /opt/spark/jobs

COPY requirements.txt /tmp/

RUN pip3 install \
    --no-cache-dir \
    -r /tmp/requirements.txt

COPY jars/ /opt/spark/jars/

COPY conf/spark-defaults.conf \
     /opt/spark/conf/spark-defaults.conf

ENV SPARK_HOME=/opt/spark

ENV PATH=$SPARK_HOME/bin:$PATH

USER spark


# FROM bitnami/spark:3.5.3

# USER root

# COPY requirements.txt /tmp/

# RUN pip install --no-cache-dir \
#     -r /tmp/requirements.txt

# COPY conf/spark-defaults.conf \
#     /opt/bitnami/spark/conf/

# COPY jars/ \
#     /opt/bitnami/spark/jars/

# RUN mkdir -p \
#     /opt/bitnami/spark/jobs

# USER 1001