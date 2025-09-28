# 第 0 章 - Hello World

让我们从基本的 TypeScript 设置和 hello world 程序开始。

此指南是用 TypeScript 编写的（是的，Python 版本即将到来）

在工作坊步骤的每个文件编辑之间有很多检查点，
即使您不熟悉 TypeScript，
您也应该能够跟上并运行每个示例。

要运行此指南，您需要安装相对较新版本的 nodejs 和 npm

您可以使用任何 nodejs 版本管理器，[homebrew](https://formulae.brew.sh/formula/node) 就可以

    brew install node@20

您应该看到 node 版本

    node --version

复制初始 package.json

    cp ./walkthrough/00-package.json package.json

<details>
<summary>显示文件</summary>

```json
// ./walkthrough/00-package.json
{
    "name": "my-agent",
    "version": "0.1.0",
    "private": true,
    "scripts": {
      "dev": "tsx src/index.ts",
      "build": "tsc"
    },
    "dependencies": {
      "tsx": "^4.15.0",
      "typescript": "^5.0.0"
    },
    "devDependencies": {
      "@types/node": "^20.0.0",
      "@typescript-eslint/eslint-plugin": "^6.0.0",
      "@typescript-eslint/parser": "^6.0.0",
      "eslint": "^8.0.0"
    }
  }
```

</details>

安装依赖

    npm install

复制 tsconfig.json

    cp ./walkthrough/00-tsconfig.json tsconfig.json

<details>
<summary>显示文件</summary>

```json
// ./walkthrough/00-tsconfig.json
{
    "compilerOptions": {
      "target": "ES2017",
      "lib": ["esnext"],
      "allowJs": true,
      "skipLibCheck": true,
      "strict": true,
      "noEmit": true,
      "esModuleInterop": true,
      "module": "esnext",
      "moduleResolution": "bundler",
      "resolveJsonModule": true,
      "isolatedModules": true,
      "jsx": "preserve",
      "incremental": true,
      "plugins": [],
      "paths": {
        "@/*": ["./*"]
      }
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
    "exclude": ["node_modules", "walkthrough"]
  }
```

</details>

添加 .gitignore

    cp ./walkthrough/00-.gitignore .gitignore

<details>
<summary>显示文件</summary>

```gitignore
// ./walkthrough/00-.gitignore
baml_client/
node_modules/
```

</details>

创建 src 文件夹

    mkdir -p src

添加一个简单的 hello world index.ts

    cp ./walkthrough/00-index.ts src/index.ts

<details>
<summary>显示文件</summary>

```ts
// ./walkthrough/00-index.ts
async function hello(): Promise<void> {
    console.log('hello, world!')
}

async function main() {
    await hello()
}

main().catch(console.error)
```

</details>

运行以验证

    npx tsx src/index.ts

您应该看到：

    hello, world!
