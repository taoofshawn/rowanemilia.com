FROM alpine:3.21 AS builder

WORKDIR /src

RUN apk add --no-cache --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community \
    hugo jpegoptim optipng python3

COPY . .

# Optimize images before build
RUN find static -type f \( -iname '*.jpg' -o -iname '*.jpeg' \) -print0 | xargs -0 jpegoptim --strip-all --max=85
RUN find static -type f -iname '*.png' -print0 | xargs -0 optipng -o3

# Generate per-month archive pages
RUN python3 gen_archives.py

# Build site
RUN hugo --minify --disableKinds=taxonomy

# Add loading="lazy" and inject width/height to prevent CLS
RUN find public -name '*.html' -exec sed -i 's|<img |<img loading="lazy" |g' {} +
RUN python3 scripts/add-img-dimensions.py public

# Pre-compress for nginx gzip_static
RUN find public -type f \( -name '*.html' -o -name '*.css' -o -name '*.js' \) -exec gzip -kf {} +

FROM nginx:1.27-alpine AS runner
COPY --from=builder /src/public /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
