FROM oven/bun:1-alpine

WORKDIR /app

COPY package.json ./
COPY bun.lockb* ./
RUN bun install --frozen-lockfile

COPY tsconfig.json ./
COPY src ./src

RUN bun run build

EXPOSE 3050

CMD ["bun", "run", "dist/index.js"]