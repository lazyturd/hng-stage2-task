# Stage 1: Build and install dependencies
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Install production dependencies only
RUN npm ci --omit=dev

# Stage 2: Production runner
FROM node:18-alpine
WORKDIR /app

# Copy node_modules from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy application source code
COPY . .

# Change ownership of the app directory to the built-in 'node' user
RUN chown -R node:node /app

# Switch to non-root user
USER node

EXPOSE 3000

# Healthcheck: Ping the root endpoint using wget (standard in Alpine)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/ || exit 1

CMD ["npm", "start"]