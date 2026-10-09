FROM nginx:1.27-alpine

# Configuração do Nginx (gzip, cache e headers básicos)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Arquivos estáticos do site
COPY index.html cliente.html sabores.html /usr/share/nginx/html/
COPY css/   /usr/share/nginx/html/css/
COPY image/ /usr/share/nginx/html/image/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q --spider http://127.0.0.1/ || exit 1
