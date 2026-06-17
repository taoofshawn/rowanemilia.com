FROM alpine:latest AS builder

WORKDIR /hugo
RUN apk add --no-cache --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community git hugo python3

RUN git clone https://github.com/taoofshawn/rowanemilia.com.git /hugo

# Generate per-month archive pages before building
RUN python3 gen_archives.py

# Build the Hugo site
RUN hugo --disableKinds=taxonomy

FROM nginx:latest AS runner
COPY --from=builder /hugo/public /usr/share/nginx/html
