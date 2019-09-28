FROM prom/prometheus:v2.8.1
ADD ./prometheus.yml /etc/prometheus/prometheus.yml
CMD [ "--config.file=/etc/prometheus/prometheus.yml","--web.enable-admin-api" ]