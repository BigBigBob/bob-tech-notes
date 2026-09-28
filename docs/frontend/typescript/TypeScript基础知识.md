# TypeScript&#x20;

​

官方文档地址：[~https://www.typescriptlang.org/zh/docs/~](https://www.typescriptlang.org/zh/docs/)​

​

# 一、为 JavaScript 程序员准备的 TypeScript

原文地址：[https://www.typescriptlang.org/zh/docs/handbook/typescript-in-5-minutes.html](https://www.typescriptlang.org/zh/docs/handbook/typescript-in-5-minutes.html)​

内容总结及知识拓展。

***

这篇文档的核心是：**TypeScript = JavaScript + 静态类型系统**。它不会取代 JavaScript，而是在代码运行前检查类型错误，并为编辑器提供更可靠的补全、跳转与重构能力。[TypeScript 官方文档](https://www.typescriptlang.org/zh/docs/handbook/typescript-in-5-minutes.html)​

## 1、页面内容总结

### 1.1. 类型推断

TypeScript 经常能根据赋值自动判断类型，不需要处处手写类型：

```ts
let message = "Hello";
// TypeScript 推断 message 为 string

message = 123;
// 错误：number 不能赋给 string
```

推荐原则：**能够清晰推断时，让 TypeScript 自己推断。**

```ts
const count = 10; // 不必写 const count: number = 10
```

函数参数通常需要标注，因为 TypeScript 不知道调用者将传入什么：

```ts
function double(value: number) {
  return value * 2;
}
```

返回值 `number` 可以自动推断。

***

### 1.2. 使用接口描述对象

`interface` 用于描述对象应该具有什么结构：

```ts
interface User {
  name: string;
  id: number;
}

const user: User = {
  name: "小明",
  id: 1,
};
```

如果缺少属性、属性类型错误，或者直接写入未知属性，TypeScript 会提示：

```ts
const user: User = {
  name: "小明",
  id: "1", // 错误：应为 number
};
```

接口也能用于函数参数和返回值：

```ts
function printUser(user: User): void {
  console.log(user.name);
}

function createUser(): User {
  return {
    name: "小红",
    id: 2,
  };
}
```

类只要具有接口要求的结构，也可以被视为该接口类型：

```ts
class UserAccount {
  constructor(
    public name: string,
    public id: number
  ) {}
}

const user: User = new UserAccount("小李", 3);
```

***

### 1.3. 常见特殊类型

除了 JavaScript 中的 `string`、`number`、`boolean` 等类型，TypeScript 还提供：

| **类型**               | **含义**       |
| -------------------- | ------------ |
| `any`                | 放弃类型检查，尽量少用  |
| `unknown`            | 类型未知，检查后才能使用 |
| `void`               | 函数没有有意义的返回值  |
| `never`              | 某个值不可能出现     |
| `null` / `undefined` | 空值或未定义       |

```ts
function log(message: string): void {
  console.log(message);
}

function fail(message: string): never {
  throw new Error(message);
}
```

`unknown` 比 `any` 更安全：

```ts
function printValue(value: unknown) {
  // console.log(value.toUpperCase()); // 错误

  if (typeof value === "string") {
    console.log(value.toUpperCase()); // 安全
  }
}
```

***

### 1.4. 联合类型

联合类型用 `|` 表示“可能是其中一种类型”：

```ts
let id: string | number;

id = 100;
id = "A100";
```

联合类型也可以限制合法值：

```ts
type Status = "loading" | "success" | "error";

let status: Status = "loading";
// status = "finished"; // 错误
```

这称为**字符串字面量联合类型**，比随意使用 `string` 更严格。

***

### 1.5. 类型收窄

如果一个值具有联合类型，使用前经常需要确定它当前是哪一种类型：

```ts
function formatId(id: string | number): string {
  if (typeof id === "string") {
    return id.toUpperCase();
  }

  return id.toFixed(0);
}
```

在 `if` 分支中，TypeScript 知道 `id` 是 `string`；在剩余路径中，知道它是 `number`。这个过程叫做 **Narrowing（类型收窄）**。

常见检查方式：

```ts
typeof value === "string"
typeof value === "number"
Array.isArray(value)
value instanceof Date
"property" in value
```

注意：检查数组不能使用 `typeof value === "array"`，因为 JavaScript 中数组的 `typeof` 结果是 `"object"`。

***

### 1.6. 泛型

泛型可以理解成“类型的参数”：

```ts
const names: Array<string> = ["小明", "小红"];
const scores: Array<number> = [90, 85];
```

也可以编写自己的泛型：

```ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const name = first(["小明", "小红"]);
// 推断为 string | undefined

const score = first([90, 85]);
// 推断为 number | undefined
```

这里的 `T` 会根据调用时传入的数据确定。泛型的价值是：**在复用代码的同时，保留准确的类型信息。**

***

### 1.7. 结构化类型系统

TypeScript 主要看一个值“具有哪些属性”，而不是看它是否明确声明了某个类型：

```ts
interface Point {
  x: number;
  y: number;
}

function printPoint(point: Point) {
  console.log(point.x, point.y);
}

const position = {
  x: 10,
  y: 20,
  z: 30,
};

printPoint(position); // 可以
```

虽然 `position` 没有声明为 `Point`，但它拥有 `x` 和 `y`，而且类型正确，因此可以使用。

这叫做**结构类型**，也常被形象地称作“鸭子类型”：如果它具有所需的形状和行为，就可以作为该类型使用。

## 2、初学者需要补充理解的知识

### 2.1. TypeScript 只在开发阶段检查类型

TypeScript 最终会被编译成 JavaScript：

```ts
const age: number = 18;
```

编译后大致是：

```js
const age = 18;
```

类型标注不会保留到运行时。因此 TypeScript 并不能自动验证接口、表单或 JSON 中的外部数据：

```ts
const response = await fetch("/api/user");
const data = await response.json();
```

服务器返回的内容仍然可能不符合预期。真实项目通常会使用运行时判断，或者 Zod 等数据验证库。

***

### `2.2.interface` 和 `type` 怎么选择

两者都能描述对象：

```ts
interface User {
  name: string;
}

type Product = {
  name: string;
};
```

简单选择方法：

* 描述对象或类的公共结构：优先考虑 `interface`
* 联合类型、元组或组合类型：使用 `type`
* 团队已有统一规范：遵循团队规范

```ts
type Result =
  | { success: true; data: string }
  | { success: false; error: string };
```

不要把它们理解成竞争关系，它们各有擅长的场景。

***

### 2.3. 可选属性与只读属性

```ts
interface User {
  readonly id: number;
  name: string;
  email?: string;
}

const user: User = {
  id: 1,
  name: "小明",
};

user.name = "小李";
// user.id = 2; // 错误：id 是只读属性
```

* `email?`：属性可以不存在
* `readonly`：通过该类型引用时不能重新赋值

***

### 2.4. 数组、元组和普通对象

```ts
const numbers: number[] = [1, 2, 3];

const coordinate: [number, number] = [10, 20];

const scores: Record<string, number> = {
  Alice: 95,
  Bob: 88,
};
```

* 数组：元素类型相同，长度通常不固定
* 元组：位置和长度具有明确含义
* `Record<K, V>`：键和值分别具有统一类型

***

### 2.5. 尽早开启严格检查

学习和新项目建议启用严格模式：

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

它能开启更严格的空值、函数参数和属性检查。刚开始错误会多一些，但能帮助你形成更可靠的类型习惯。

## 3、一个综合示例

```ts
interface User {
  readonly id: number;
  name: string;
  role: "admin" | "member";
  email?: string;
}

function describeUser(user: User): string {
  const emailText =
    user.email === undefined
      ? "未填写邮箱"
      : `邮箱：${user.email}`;

  return `${user.name}（${user.role}），${emailText}`;
}

const user: User = {
  id: 1,
  name: "小明",
  role: "member",
};

console.log(describeUser(user));
```

这个例子包含：

* 对象接口
* 函数参数和返回值
* 字面量联合类型
* 可选属性
* 只读属性
* 对 `undefined` 的类型收窄

## 4、推荐学习顺序

1. JavaScript 基础：变量、函数、对象、数组和模块
2. TypeScript 基础类型与类型推断
3. 对象类型、`interface` 和 `type`
4. 联合类型与类型收窄
5. 函数类型
6. 泛型
7. 类与模块
8. 工具类型：`Partial`、`Pick`、`Omit`、`Record`
9. `tsconfig.json` 和严格模式

学习 TypeScript 最重要的思维不是“给所有变量加类型”，而是：

> 用类型描述数据可能是什么、不可能是什么，以及不同数据之间有什么关系。

​

typeof value === "string" 中的===是什么意思？

***

`===` 是 JavaScript/TypeScript 中的**严格相等运算符**，用于判断左右两边的值和类型是否都相等。

```ts
typeof value === "string"
```

可以分成两步理解：

```ts
typeof value
```

获取 `value` 在运行时的类型名称，例如 `"string"`、`"number"`。

```ts
typeof value === "string"
```

判断这个类型名称是否严格等于 `"string"`，也就是判断 `value` 是否为字符串。

```ts
const value = "你好";

console.log(typeof value);              // "string"
console.log(typeof value === "string"); // true
```

### `===` 和 `==` 的区别

`===` 不会自动转换类型，而 `==` 可能先转换类型再比较：

```ts
5 === 5;   // true
5 === "5"; // false：类型不同

5 == "5";  // true：字符串 "5" 被转换后再比较
```

通常推荐使用 `===`，因为它的行为更明确、更不容易产生意外结果。

在 TypeScript 中，这种判断还会触发**类型收窄**：

```ts
function print(value: string | number) {
  if (typeof value === "string") {
    // 此处 TypeScript 知道 value 是 string
    console.log(value.toUpperCase());
  } else {
    // 此处 TypeScript 知道 value 是 number
    console.log(value.toFixed(2));
  }
}
```

​

# 二、为 JavaScript 程序员准备的 TypeScript

​[：https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html)​

总结页面内容，并进行知识拓展

***

这篇文章主要面向熟悉 Java/C# 的程序员，但对初学者也很有价值。它强调的不是 TypeScript 语法，而是一个关键观念：

> TypeScript 虽然拥有类、接口和静态类型，但它的底层仍然是 JavaScript，不能完全套用 Java/C# 的思维。

以下内容根据 [TypeScript 官方文档：TypeScript for Java/C# Programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html) 整理。

## 1、先学一点 JavaScript

TypeScript 不会改变 JavaScript 的运行方式。

例如：

* 字符串如何转数字
* 数组如何遍历
* 异步请求如何执行
* 文件如何读取
* 对象和原型如何工作

这些仍然属于 JavaScript 的知识。

```ts
const text: string = "123";
const value: number = Number(text);
```

`: string` 和 `: number` 是 TypeScript 类型标注；真正把字符串转换成数字的是 JavaScript 的 `Number()`。

编译后，类型会消失：

```js
const text = "123";
const value = Number(text);
```

因此，学习 TypeScript 时也要学习 JavaScript，尤其是：

* 对象和数组
* 函数
* 模块
* 闭包
* `this`
* Promise 和 `async/await`
* JavaScript 的类型转换规则

## 2、重新思考“类”

Java/C# 的常见思维

在 Java/C# 中，数据和函数通常放在类中：

```java
class MathUtils {
    static int add(int a, int b) {
        return a + b;
    }
}
```

TypeScript/JavaScript 的常见写法

JavaScript 允许函数独立存在，不必为了组织代码而创建类：

```ts
export function add(a: number, b: number): number {
  return a + b;
}
```

数据也可以是普通对象：

```ts
interface User {
  name: string;
  age: number;
}

function introduce(user: User): string {
  return `我是${user.name}，今年${user.age}岁`;
}
```

这里不需要 `UserService`、`UserUtils` 或其他包装类。

静态工具类通常没有必要

不推荐为了模仿 Java 而这样写：

```ts
class StringUtils {
  static capitalize(value: string): string {
    return value[0].toUpperCase() + value.slice(1);
  }
}
```

直接导出函数通常更简单：

```ts
export function capitalize(value: string): string {
  return value[0].toUpperCase() + value.slice(1);
}
```

JavaScript 模块本身已经能提供：

* 命名空间
* 私有作用域
* 单例式加载
* 导入和导出

但类并不是不能用

当问题本身适合用对象表达状态和行为时，类依然很合适：

```ts
class BankAccount {
  private balance = 0;

  deposit(amount: number): void {
    this.balance += amount;
  }

  getBalance(): number {
    return this.balance;
  }
}
```

TypeScript 支持熟悉的面向对象功能：

* `class`
* `extends`
* `implements`
* `public`
* `protected`
* `private`
* `abstract`
* `static`

核心原则是：**根据问题选择类，而不是为了组织代码而强行创建类。**

## 3、把类型理解为“值的集合”

这是文章中最重要的思想之一。

```ts
type Text = string;
```

可以理解为：`Text` 是所有字符串组成的集合。

```ts
type Id = string | number;
```

`Id` 则是字符串集合与数字集合的并集：

```text
string 集合 ─┐
             ├─ string | number
number 集合 ─┘
```

因此以下值都是 `Id`：

```ts
let id: string | number;

id = "A100";
id = 100;
```

但是：

```ts
id = true; // 错误
```

因为 `true` 不属于 `string | number` 这个集合。

一个值可以属于多个类型

```ts
interface Named {
  name: string;
}

interface Employee {
  name: string;
  employeeId: number;
}

const person = {
  name: "小明",
  employeeId: 1001,
};
```

`person` 同时符合：

* `Named`
* `Employee`
* `{ name: string; employeeId: number }`

所以一个值不一定只有一个唯一的 TypeScript 类型。

## 4、结构类型系统

Java/C# 主要采用**名义类型系统**：类型之间通常需要明确声明关系。

例如：

```java
class Dog implements Animal {}
```

TypeScript 主要采用**结构类型系统**：重点是对象拥有哪些属性，而不是它声明自己属于哪个类型。

```ts
interface Point {
  x: number;
  y: number;
}

function printPoint(point: Point): void {
  console.log(point.x, point.y);
}

const position = {
  x: 10,
  y: 20,
  name: "当前位置",
};

printPoint(position); // 可以
```

`position` 没有显式声明为 `Point`，但是它拥有符合要求的：

```ts
x: number;
y: number;
```

所以可以传给 `printPoint()`。

可以把它简单理解成：

> 不在乎你叫什么类型，只在乎你是否具备我需要的结构。

## 5、结构类型带来的特殊现象

### 1. 空类型几乎接受任何对象

```ts
class Empty {}

function handle(value: Empty): void {}

handle({ name: "小明" }); // 可以
handle({ count: 10 });    // 也可以
```

为什么？

`Empty` 没有要求任何属性。任何对象都拥有它所要求的全部属性——因为它什么都没要求。

所以空接口也没有“任意对象必须显式实现它”的效果：

```ts
interface Empty {}

const value: Empty = { anything: 123 };
```

因此不要把空接口当作 Java 中的标记接口。

***

### 2. 结构相同的类可能相互兼容

```ts
class Car {
  drive(): void {
    console.log("汽车行驶");
  }
}

class Golfer {
  drive(): void {
    console.log("高尔夫击球");
  }
}

let car: Car = new Golfer(); // 可以
```

虽然业务含义完全不同，但 TypeScript 看到的结构都是：

```ts
{
  drive(): void;
}
```

所以两者兼容。

不过，如果类包含 `private` 或 `protected` 成员，兼容规则会更加严格：

```ts
class Car {
  private brand = "car";

  drive(): void {}
}

class Golfer {
  private brand = "golfer";

  drive(): void {}
}

// let car: Car = new Golfer(); // 错误
```

## 6、类型在运行时会被删除

TypeScript 的接口、类型别名和泛型主要用于编译阶段：

```ts
interface User {
  name: string;
}

const user: User = {
  name: "小明",
};
```

编译成 JavaScript 后大致为：

```js
const user = {
  name: "小明",
};
```

运行时不存在 `User` 这个接口。

所以这样做是不可能的：

```ts
interface User {
  name: string;
}

// if (value instanceof User) {} // 错误：User 不是运行时的值
```

`interface` 只存在于“类型空间”，不能传给 `instanceof`。

## 7、`typeof` 和 `instanceof` 的能力有限

### `typeof`

`typeof` 可以检查 JavaScript 的基础运行时类型：

```ts
function print(value: string | number): void {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  } else {
    console.log(value.toFixed(2));
  }
}
```

常见结果包括：

```ts
typeof "hello";       // "string"
typeof 123;           // "number"
typeof true;          // "boolean"
typeof undefined;     // "undefined"
typeof (() => {});    // "function"
typeof {};            // "object"
typeof [];            // "object"
typeof null;          // "object"（JavaScript 的历史遗留行为）
```

`typeof new Car()` 的结果也是 `"object"`，不会得到 `"Car"`。

### `instanceof`

类在运行时是真实存在的 JavaScript 值，因此可以使用 `instanceof`：

```ts
class Car {
  drive(): void {}
}

const value = new Car();

console.log(value instanceof Car); // true
```

但 `instanceof` 检查的是对象的原型链，不是 TypeScript 接口结构。

## 8、运行时如何判断接口类型

如果数据来自接口、文件或用户输入，不能只写一个类型断言：

```ts
const user = JSON.parse(text) as User;
```

`as User` 不会验证数据，只是在告诉编译器“请相信我”。

更安全的方式是编写类型守卫：

```ts
interface User {
  name: string;
  age: number;
}

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  return (
    "name" in value &&
    typeof value.name === "string" &&
    "age" in value &&
    typeof value.age === "number"
  );
}

const data: unknown = JSON.parse(
  '{"name":"小明","age":18}'
);

if (isUser(data)) {
  console.log(data.name);
}
```

真实项目中也常使用 Zod、Valibot 等运行时验证库。

## 9、知识拓展：需要名义类型时怎么办

有时两个值结构相同，但业务上绝不能混用，例如用户 ID 和订单 ID：

```ts
type UserId = string;
type OrderId = string;

const userId: UserId = "U100";
const orderId: OrderId = userId; // 可以，但业务上可能不合理
```

可以使用“品牌类型”模拟名义类型：

```ts
type UserId = string & {
  readonly __brand: "UserId";
};

type OrderId = string & {
  readonly __brand: "OrderId";
};

function createUserId(value: string): UserId {
  return value as UserId;
}

const userId = createUserId("U100");

// const orderId: OrderId = userId; // 错误
```

这种写法常用于：

* 不同种类的 ID
* 不同货币
* 已验证与未验证的数据
* 不同计量单位

## 10、知识拓展：用可辨识联合表达对象类型

与其依赖复杂的类继承，有时可以使用联合类型：

```ts
type Shape =
  | {
      kind: "circle";
      radius: number;
    }
  | {
      kind: "rectangle";
      width: number;
      height: number;
    };

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;

    case "rectangle":
      return shape.width * shape.height;
  }
}
```

`kind` 是识别不同类型的标签。TypeScript 会根据它自动收窄类型。

这种模式非常适合：

* 请求状态
* 操作结果
* 消息类型
* UI 状态
* Redux action
* API 成功与失败响应

例如：

```ts
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function showResult(result: Result<string>): void {
  if (result.success) {
    console.log(result.data);
  } else {
    console.log(result.error);
  }
}
```

​

​

# 三、JavaScript 模块

这里的“JavaScript 模块”主要指现代的 **ES Module（ESM）**。它通过 `export` 和 `import` 把代码拆分到不同文件中。

假设项目结构如下：

```text
src/
├─ main.ts
├─ math.ts
└─ user.ts
```

只要文件中出现顶层 `import` 或 `export`，TypeScript 通常就会把它视为模块：

```ts
export {};
```

即使没有真正导出内容，这句也可以明确告诉 TypeScript：“这是一个模块，不是全局脚本。”

***

## 1、模块提供命名空间

“命名空间”解决的是**名称冲突和代码归类**问题。

假设两个文件都定义了 `format()`：

```ts
// date-utils.ts
export function format(date: Date): string {
  return date.toISOString();
}
```

```ts
// number-utils.ts
export function format(value: number): string {
  return value.toFixed(2);
}
```

它们虽然同名，但属于不同模块，因此不会冲突。

导入时可以改名：

```ts
import {
  format as formatDate,
} from "./date-utils.js";

import {
  format as formatNumber,
} from "./number-utils.js";

console.log(formatDate(new Date()));
console.log(formatNumber(3.14159));
```

这里每个文件天然形成一个独立的名称空间。

### 1.1、整体导入为模块对象

也可以把整个模块导入为一个对象：

```ts
import * as DateUtils from "./date-utils.js";
import * as NumberUtils from "./number-utils.js";

DateUtils.format(new Date());
NumberUtils.format(3.14);
```

`DateUtils` 和 `NumberUtils` 被称为**模块命名空间对象**。

这看起来很像静态工具类：

```ts
DateUtils.format(...)
```

但不需要创建：

```ts
class DateUtils {
  static format(...) {}
}
```

### 1.2、与 TypeScript `namespace` 的区别

TypeScript 还有一个 `namespace` 关键字：

```ts
namespace DateUtils {
  export function format(date: Date) {
    return date.toISOString();
  }
}
```

不过在现代模块化项目中，通常优先使用文件模块：

```ts
// date-utils.ts
export function format(date: Date) {
  return date.toISOString();
}
```

因为 ES Module：

* 是 JavaScript 标准
* 浏览器和 Node.js 原生支持
* 构建工具能够分析
* 更容易进行 tree shaking
* 与 npm 包的组织方式一致

所以这里所说的“模块提供命名空间”，不是说必须使用 `namespace` 关键字，而是说：**每个模块天然隔离自己的名称。**

***

## 2、模块提供私有作用域

默认情况下，模块中声明的变量、函数和类只在当前模块内部可见。

```ts
// counter.ts

let count = 0;

function validateAmount(amount: number): void {
  if (amount <= 0) {
    throw new Error("amount 必须大于 0");
  }
}

export function increment(amount: number): void {
  validateAmount(amount);
  count += amount;
}

export function getCount(): number {
  return count;
}
```

这里：

```ts
count
validateAmount
```

没有被导出，因此属于模块内部实现。

其他文件只能使用导出的成员：

```ts
import {
  increment,
  getCount,
} from "./counter.js";

increment(2);
console.log(getCount());

// count;          // 错误：不可见
// validateAmount; // 错误：不可见
```

这就是模块级私有作用域。

### 2.1、“私有”不等于 `private`

它与类的 `private` 是两个不同层面的概念。

类私有成员：

```ts
class Counter {
  private count = 0;
}
```

模块私有成员：

```ts
let count = 0;

export function increment() {
  count++;
}
```

区别是：

* 类的 `private` 保护某个对象或类的内部成员
* 模块作用域保护整个文件或模块的内部实现
* 模块私有不需要额外关键字
* 只要不 `export`，其他模块就不能直接导入

### 2.2、可以隐藏具体实现，只暴露公共接口

```ts
// password.ts

function hashInternal(password: string): string {
  // 内部算法
  return `hashed:${password}`;
}

export function createPassword(password: string): string {
  if (password.length < 8) {
    throw new Error("密码至少需要 8 个字符");
  }

  return hashInternal(password);
}
```

使用者只能调用：

```ts
import { createPassword } from "./password.js";
```

以后即使更换 `hashInternal()` 的实现，只要 `createPassword()` 的使用方式不变，其他文件通常就不需要修改。

这就是所谓的**封装**。

### 2.3、浏览器中也不会自动污染全局变量

传统普通脚本：

```html
<script src="a.js"></script>
<script src="b.js"></script>
```

如果两个脚本都在顶层声明同名变量，可能发生冲突。

模块脚本：

```html
<script type="module" src="./main.js"></script>
```

模块内部的顶层声明不会自动成为 `window` 的属性：

```js
const message = "hello";

console.log(window.message); // undefined
```

***

## 3、模块提供“单例式加载”

模块第一次被加载时，顶层代码会执行一次。之后再次导入时，运行环境通常会复用已经加载过的模块实例。

考虑下面的模块：

```ts
// counter.ts

console.log("counter 模块开始执行");

let count = 0;

export function increment(): void {
  count++;
}

export function getCount(): number {
  return count;
}
```

两个文件分别导入它：

```ts
// page-a.ts

import {
  increment,
  getCount,
} from "./counter.js";

increment();

console.log("A:", getCount());
```

```ts
// page-b.ts

import {
  increment,
  getCount,
} from "./counter.js";

increment();

console.log("B:", getCount());
```

如果 `page-a.ts` 和 `page-b.ts` 处于同一模块加载环境中，它们访问的通常是同一个 `counter` 模块实例：

```text
counter 模块开始执行
A: 1
B: 2
```

而不是：

```text
A: 1
B: 1
```

这意味着模块内部的：

```ts
let count = 0;
```

只初始化一次，并由所有导入者共享。

因此它具有类似单例的效果。

***

## 4、模块提供导出

`export` 决定模块愿意向外公开什么。

### 4.1、命名导出

```ts
// math.ts

export const PI = 3.14159;

export function add(
  a: number,
  b: number
): number {
  return a + b;
}
```

也可以先声明，最后统一导出：

```ts
const PI = 3.14159;

function add(a: number, b: number): number {
  return a + b;
}

export {
  PI,
  add,
};
```

导出时还可以改名：

```ts
function add(a: number, b: number): number {
  return a + b;
}

export {
  add as sum,
};
```

使用方看到的是 `sum`：

```ts
import { sum } from "./math.js";
```

### 4.2、默认导出

一个模块最多只能有一个默认导出：

```ts
// UserService.ts

export default class UserService {
  findUser(id: number): void {
    console.log(id);
  }
}
```

导入默认值时，可以自行选择本地名称：

```ts
import UserService from "./UserService.js";
```

也可以：

```ts
import Service from "./UserService.js";
```

因为默认导入不依赖原来的名字。

### 4.3、命名导出与默认导出怎么选

命名导出的优势是名称统一：

```ts
import { createUser } from "./user.js";
```

编辑器也更容易自动补全和批量重命名。因此应用代码中，很多团队更倾向命名导出。

默认导出常见于：

* 一个文件主要导出一个组件
* 某些框架规定的文件结构
* 第三方库的既有 API

两者可以共存：

```ts
export const version = "1.0";

export default function start() {}
```

使用：

```ts
import start, {
  version,
} from "./app.js";
```

***

## 5、模块提供导入

### 5.1、导入命名成员

```ts
import {
  add,
  PI,
} from "./math.js";

console.log(add(1, 2));
console.log(PI);
```

命名必须与导出名称匹配。

### 5.2、导入时改名

```ts
import {
  add as calculateTotal,
} from "./math.js";

calculateTotal(1, 2);
```

### 5.3、导入默认成员

```ts
import UserService from "./UserService.js";
```

默认导入没有花括号。

### 5.4、导入整个模块

```ts
import * as MathUtils from "./math.js";

MathUtils.add(1, 2);
console.log(MathUtils.PI);
```

### 5.5、只执行模块，不导入成员

```ts
import "./setup.js";
```

这种写法用于模块的副作用。例如：

```ts
// setup.ts
console.log("正在初始化应用");
registerGlobalHandlers();
```

在入口文件中：

```ts
import "./setup.js";
```

应该谨慎使用副作用导入，因为它可能使程序行为依赖加载顺序。

​

# 四、5分钟了解TypeScript

原文地址：[https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html](https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html)​

***

这篇官方教程通过一个简单的网页问候程序，展示 TypeScript 的核心工作方式：

> 编写 `.ts` → 静态类型检查 → 编译为 `.js` → 由浏览器或 Node.js 执行。

TypeScript 本身不是新的运行环境；最终运行的仍然是 JavaScript。[官方教程](https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html)​

## 1. 页面内容总结

### 安装与编译

页面使用全局安装：

```bash
npm install -g typescript
tsc greeter.ts
```

`tsc` 是 TypeScript 编译器。它检查 `greeter.ts`，然后生成浏览器能执行的 `greeter.js`。

实际项目中更建议本地安装，避免不同项目之间版本冲突：

```bash
npm init -y
npm install --save-dev typescript
npx tsc --init
npx tsc
```

### TypeScript 可以直接接受 JavaScript

最初的文件虽然使用 `.ts` 扩展名，内容却完全是 JavaScript：

```ts
function greeter(person) {
  return "Hello, " + person;
}

const user = "Jane User";

document.body.textContent = greeter(user);
```

这体现了 TypeScript 的重要特征：它是 JavaScript 的超集，大量 JavaScript 代码可以直接迁移到 TypeScript。

### 类型注解

给参数添加 `: string`：

```ts
function greeter(person: string) {
  return "Hello, " + person;
}
```

它表示函数要求调用者传入字符串。下面的代码会产生编译错误：

```ts
greeter([0, 1, 2]);
// number[] 不能赋值给 string
```

类型注解可以理解为一份“调用契约”：

```ts
function add(a: number, b: number): number {
  return a + b;
}
```

* `a: number`：参数类型
* `b: number`：参数类型
* `): number`：返回值类型

不过并非处处都要手写类型。TypeScript 经常能够自动推断：

```ts
const name = "Alice"; // 推断为 string
const scores = [90, 85]; // 推断为 number[]
```

官方也建议初学时不要添加过多多余注解。[常用类型与类型推断](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)​

### 接口与结构化类型

页面定义了一个接口：

```ts
interface Person {
  firstName: string;
  lastName: string;
}
```

然后让函数接收符合这个结构的对象：

```ts
function greeter(person: Person) {
  return `Hello, ${person.firstName} ${person.lastName}`;
}

const user = {
  firstName: "Jane",
  lastName: "User",
};

greeter(user);
```

`user` 没有显式声明 `implements Person`，但它拥有接口要求的两个属性，所以可以传入。

这叫作结构化类型系统，通俗地说：

> TypeScript 关心一个值“长什么样、能做什么”，而不是它明确声称自己属于哪个类型。

例如，多出属性通常也没有问题：

```ts
const employee = {
  firstName: "Jane",
  lastName: "User",
  department: "Engineering",
};

greeter(employee); // 可以
```

但直接传对象字面量时，会触发额外属性检查：

```ts
greeter({
  firstName: "Jane",
  lastName: "User",
  department: "Engineering", // 通常报错：Person 中没有该属性
});
```

### 类

页面最后定义了一个 `Student` 类：

```ts
class Student {
  fullName: string;

  constructor(
    public firstName: string,
    public middleInitial: string,
    public lastName: string,
  ) {
    this.fullName = `${firstName} ${middleInitial} ${lastName}`;
  }
}
```

构造器参数前的 `public` 是一种简写：

```ts
constructor(public firstName: string) {}
```

大致等价于：

```ts
firstName: string;

constructor(firstName: string) {
  this.firstName = firstName;
}
```

`Student` 实例包含 `firstName` 和 `lastName`，因此符合 `Person` 的结构：

```ts
const user = new Student("Jane", "M.", "User");
greeter(user); // 可以
```

这里没有使用继承。它展示的是“类的实例可以符合接口”。

### 在浏览器运行

HTML 引入的不是 `.ts`，而是编译后的 `.js`：

```html
<!doctype html>
<html>
  <head>
    <title>TypeScript Greeter</title>
  </head>
  <body>
    <script src="greeter.js"></script>
  </body>
</html>
```

浏览器通常不会直接运行 TypeScript，因此完整流程是：

```text
greeter.ts
    ↓ tsc：类型检查并转换
greeter.js
    ↓ 浏览器加载
网页运行
```

## 2. 最重要的知识扩展

### 类型只存在于编译阶段

接口和大部分类型注解不会出现在最终 JavaScript 中：

```ts
interface User {
  name: string;
}

const user: User = { name: "Alice" };
```

编译后大致只剩：

```js
const user = { name: "Alice" };
```

所以 TypeScript 类型不能自动验证网络数据：

```ts
const response = await fetch("/api/user");
const data = await response.json();
```

`data` 来自运行时，可能不符合你期望的结构。真正的项目需要自行校验，或者使用 Zod 等运行时验证库。

### 类型错误不一定阻止生成 JavaScript

教程指出，即使发生类型错误，`tsc` 默认仍可能生成 JavaScript。这是因为 `noEmitOnError` 默认是 `false`。

项目中可以启用：

```json
{
  "compilerOptions": {
    "noEmitOnError": true
  }
}
```

这样存在类型错误时就不输出 JavaScript。[官方配置说明](https://www.typescriptlang.org/tsconfig/noEmitOnError.html)​

### 建议开启严格模式

初学时就开启严格检查，长期反而更容易形成正确习惯：

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict` 会同时启用一组严格类型检查规则，提供更强的正确性保证。[官方 strict 说明](https://www.typescriptlang.org/tsconfig/strict.html)​

例如：

```ts
function greeter(person) {
  // strict 模式下，person 隐式为 any 会报错
}
```

### 尽量避免 `any`

`any` 相当于告诉 TypeScript：“不要检查这个值”：

```ts
let value: any = "hello";

value.notExistingMethod(); // 编译器不阻止，运行时可能崩溃
```

不确定类型时，优先考虑 `unknown`：

```ts
function printValue(value: unknown) {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  }
}
```

`unknown` 会要求你先检查类型，这个过程叫类型收窄。

### `interface` 和 `type` 的简单选择

对象结构通常可以使用任意一种：

```ts
interface Person {
  name: string;
}
```

```ts
type Person = {
  name: string;
};
```

初学阶段可以这样记：

* 描述对象、类的公共结构：优先考虑 `interface`
* 联合类型、元组或复杂组合：使用 `type`

例如：

```ts
type ID = string | number;
type Point = [number, number];
```

`interface` 可以声明合并，而 `type` 能表达更广泛的类型组合。[官方对比](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#differences-between-type-aliases-and-interfaces)​

## 3. 更适合现在项目的完整示例

`greeter.ts`：

```ts
interface Person {
  firstName: string;
  lastName: string;
  middleInitial?: string;
}

function formatName(person: Person): string {
  const middle = person.middleInitial
    ? ` ${person.middleInitial}`
    : "";

  return `${person.firstName}${middle} ${person.lastName}`;
}

function greet(person: Person): string {
  return `Hello, ${formatName(person)}!`;
}

const user: Person = {
  firstName: "Jane",
  middleInitial: "M.",
  lastName: "User",
};

const output = document.querySelector<HTMLParagraphElement>("#output");

if (output) {
  output.textContent = greet(user);
}
```

`index.html`：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <title>TypeScript Greeter</title>
    <script src="greeter.js" defer></script>
  </head>
  <body>
    <p id="output"></p>
  </body>
</html>
```

建议的 `tsconfig.json`：

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "strict": true,
    "noEmitOnError": true,
    "outDir": "dist"
  },
  "include": ["*.ts"]
}
```

注意：设置 `outDir: "dist"` 后，HTML 中应改为：

```html
<script src="dist/greeter.js" defer></script>
```

## 4. 推荐学习顺序

学完这个页面后，可以依次学习：

1. 基础类型和类型推断
2. 数组、对象、函数类型
3. 可选属性与联合类型
4. 类型收窄
5. `interface` 与 `type`
6. 泛型
7. 模块：`import` / `export`
8. `tsconfig.json`
9. 异步函数和 `Promise`
10. DOM 类型或 Node.js 类型

这篇页面真正需要建立的核心认识是：

> TypeScript 利用静态类型，在代码运行之前发现一部分错误，并为编辑器提供补全、跳转、重构等能力；编译后，程序仍然是 JavaScript。

​

# 五、The TypeScript Handbook

原文地址：[https://www.typescriptlang.org/docs/handbook/intro.html](https://www.typescriptlang.org/docs/handbook/intro.html)​

***

这篇是 TypeScript Handbook 的“使用说明”，重点不是语法，而是回答三个问题：

1. TypeScript 为什么存在？
2. Handbook 应该怎样阅读？
3. Handbook 不会教什么？

​[TypeScript Handbook 导言](https://www.typescriptlang.org/docs/handbook/intro.html)​

## 1. TypeScript 为什么出现？

JavaScript 最初主要用于给网页增加简单交互，后来逐渐扩展到：

* 大型前端应用
* Node.js 后端
* 桌面应用
* 移动应用
* 跨平台工具

随着项目变大，代码之间的关系越来越复杂，但原生 JavaScript 不容易直接表达这些关系。

例如：

```js
function calculatePrice(price, quantity) {
  return price * quantity;
}

calculatePrice("100", 2);
```

调用者到底应该传入数字还是字符串？单看函数名并不明确。JavaScript 通常要等代码运行后，才能发现某些问题。

TypeScript 可以明确表达约束：

```ts
function calculatePrice(
  price: number,
  quantity: number,
): number {
  return price * quantity;
}

calculatePrice("100", 2);
// 错误：string 不能传给 number
```

因此，TypeScript 的核心目标是：

> 在 JavaScript 代码运行之前，对它进行静态类型检查。

“静态”表示运行前，“类型检查”表示检查值的使用方式是否符合预期。[官方说明](https://www.typescriptlang.org/docs/handbook/intro.html#about-this-handbook)​

## 2. TypeScript 主要防止什么错误？

页面指出，程序中很多常见错误都属于类型错误，例如：

### 拼写错误

```ts
const user = {
  name: "Alice",
};

console.log(user.naem);
// 错误：不存在 naem，可能想写 name
```

### 误解第三方 API

```ts
const names = ["Alice", "Bob"];

names.push(100);
// 错误：number 不能加入 string[]
```

### 错误理解返回值

```ts
function findUser(): User | undefined {
  // ...
}

const user = findUser();
console.log(user.name);
// 错误：user 可能是 undefined
```

### 使用了错误的参数

```ts
function setAge(age: number) {}

setAge("十八");
// 错误：string 不能传给 number
```

这些错误不一定会立即导致程序崩溃，但往往代表程序员的假设和实际代码不一致。

## 3. 静态检查不等于运行时检查

这是导言背后最重要的知识扩展。

TypeScript 检查的是源代码，类型通常会在编译时被删除：

```ts
function greet(name: string): string {
  return `Hello, ${name}`;
}
```

编译后大致为：

```js
function greet(name) {
  return `Hello, ${name}`;
}
```

因此 TypeScript 不能保证外部数据一定正确：

```ts
interface User {
  id: number;
  name: string;
}

const response = await fetch("/api/user");
const user = (await response.json()) as User;
```

这里的 `as User` 只是告诉编译器“把它当成 User”，不会真正验证服务器返回的数据。

如果服务器返回：

```json
{
  "id": "not-a-number",
  "name": null
}
```

TypeScript 在运行时不会自动阻止它。

所以应该区分：

| **检查方式**        | **发生时间** | **示例**      |
| --------------- | -------- | ----------- |
| TypeScript 静态检查 | 运行前      | 参数类型、属性拼写   |
| 运行时验证           | 程序运行时    | API 响应、用户输入 |
| 自动化测试           | 执行测试时    | 业务逻辑是否正确    |

简单的运行时验证可以这样写：

```ts
function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const candidate = value as Record<string, unknown>;

  return (
    typeof candidate.id === "number" &&
    typeof candidate.name === "string"
  );
}
```

## 4. Handbook 的结构

官方文档主要分成两种内容。

### Handbook

Handbook 是连续的学习材料，适合按照左侧目录从上往下阅读。

完成后，读者应该能够：

* 阅读常见的 TypeScript 语法
* 理解常见的 TypeScript 编程模式
* 解释重要编译器选项的作用
* 预测大部分类型系统行为

它是一份综合指南，但不是完整的语言规范。[Handbook 结构说明](https://www.typescriptlang.org/docs/handbook/intro.html#how-is-this-handbook-structured)​

### Reference

Reference 是专题参考资料，例如：

* Utility Types
* 类型推断
* 类型兼容性
* 枚举
* 装饰器
* 声明合并

它不强调连续性，适合已经知道概念名称之后查阅。

可以这样理解：

* Handbook：像教材
* Reference：像词典
* TSConfig Reference：像配置说明书
* Language Specification：偏向语言实现者的正式定义

初学时不要试图从头读完 Reference。

## 5. Handbook 不教什么？

### 不系统教授 JavaScript 基础

Handbook 默认你对以下 JavaScript 概念有一定了解：

* 变量与作用域
* 条件语句和循环
* 函数
* 对象与数组
* 类
* 闭包
* Promise 和异步编程
* ES 模块

例如：

```ts
const double = (value: number) => value * 2;
```

TypeScript Handbook 会解释 `value: number`，但不一定详细解释箭头函数本身。

如果 TypeScript 是你的第一门语言，官方建议先学习 JavaScript 基础。[官方初学建议](https://www.typescriptlang.org/docs/handbook/intro.html#about-this-handbook)​

### 不是完整语言规范

Handbook 以容易理解为目标，不会覆盖所有边界情况和形式化规则。

例如，初学时只需要知道结构符合就可能类型兼容：

```ts
interface Named {
  name: string;
}

const employee = {
  name: "Alice",
  department: "Engineering",
};

const person: Named = employee; // 可以
```

至于结构化类型系统的全部兼容规则，应在需要时再查 Reference。

### 不负责讲解所有工具链

Handbook 不会系统教授 TypeScript 如何与这些工具集成：

* React、Vue、Angular、Svelte
* Vite、webpack、Rollup
* Babel
* npm、pnpm、Yarn
* 测试框架
* 单体仓库工具

这些属于生态和工程工具，不是 TypeScript 类型系统本身。

## 6. 根据背景选择入口

官方给出了几种入口：

* 完全没有编程基础：先学习 JavaScript
* 会 JavaScript：阅读 TypeScript for JavaScript Programmers
* 会 Java/C#：阅读 TypeScript for Java/C# Programmers
* 熟悉函数式编程：阅读对应介绍
* 已理解基本定位：直接进入 The Basics

如果你是 TypeScript 和 JavaScript 的初学者，我建议采用双线学习：

```text
JavaScript 基础
    ├─ 变量、函数、对象、数组
    ├─ 作用域、闭包
    ├─ 类和原型
    ├─ Promise / async
    └─ import / export
              ↓
TypeScript 类型系统
    ├─ 基础类型
    ├─ 函数和对象类型
    ├─ 联合类型与类型收窄
    ├─ interface / type
    ├─ 泛型
    └─ 模块与编译配置
```

不要等“彻底学完 JavaScript”再碰 TypeScript。可以学完一个 JavaScript 概念，紧接着学习它对应的 TypeScript类型表达。

## 7. 对“类型”的正确理解

初学者容易把类型理解成给变量贴标签：

```ts
let age: number = 18;
```

更有价值的理解是：类型表达代码之间的关系。

```ts
interface Product {
  id: string;
  price: number;
}

function findProduct(id: Product["id"]): Product | undefined {
  // ...
  return undefined;
}
```

这里表达了三个关系：

* 输入必须符合 `Product.id` 的类型
* 成功时返回 `Product`
* 查找失败时返回 `undefined`

调用者因此必须处理失败情况：

```ts
const product = findProduct("p-001");

if (product) {
  console.log(product.price);
}
```

类型系统的真正价值不是让代码显得严格，而是让函数、数据和模块之间的假设变得明确。

## 8. 推荐的 Handbook 阅读顺序

对于初学者，建议按下面的顺序：

1. [The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html)
2. Everyday Types
3. Narrowing
4. More on Functions
5. Object Types
6. Generics
7. Classes
8. Modules

第一遍可以暂时跳过：

* Conditional Types
* Mapped Types
* Template Literal Types
* Declaration Merging
* Decorators
* 自己编写 `.d.ts`

最后，用一句话总结这篇导言：

> TypeScript 是 JavaScript 的静态类型检查器；Handbook 教你理解和使用它的类型系统，但不会代替 JavaScript 基础课程、完整语言规范或前端工程工具教程。

​

# 六、The Basics

原文地址：[https://www.typescriptlang.org/docs/handbook/2/basic-types.html](https://www.typescriptlang.org/docs/handbook/2/basic-types.html)​

***

这篇 [TypeScript Handbook：The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) 并不是在罗列 `string`、`number` 等基础类型，而是在解释 TypeScript 的核心工作方式：**在 JavaScript 运行之前，通过静态类型分析提前发现错误。**

## 1、页面核心内容

### 1.1. TypeScript 是 JavaScript 的静态类型检查器

JavaScript 通常要运行代码后，才能发现某些错误：

```js
const message = "Hello World";

message(); // 运行时报错：message 不是函数
```

TypeScript 可以在运行前发现它：

```ts
const message = "Hello World";

message();
// 编译错误：This expression is not callable.
```

可以这样理解：

* JavaScript：运行时才检查值能做什么。
* TypeScript：编写和编译时预测值能做什么。
* TypeScript 最终仍然生成 JavaScript，由浏览器或 Node.js 执行。

类型描述的其实是一个值具有哪些“能力”。例如：

* `string` 可以调用 `toLowerCase()`。
* 函数可以被调用。
* `Date` 可以调用 `toDateString()`。
* 普通对象只能访问其类型中存在的属性。

***

### 1.2. TypeScript 还能发现“不一定立即报错”的问题

下面的 JavaScript 可以运行，但很可能是程序错误：

```js
const user = {
  name: "Daniel",
  age: 26,
};

console.log(user.location); // undefined
```

TypeScript 会提前指出：

```ts
user.location;
// Property 'location' does not exist
```

它还能发现：

#### 拼写错误

```ts
const announcement = "Hello";

announcement.toLocalLowerCase(); // 方法名写错
announcement.toLocaleLowerCase(); // 正确
```

#### 忘记调用函数

```ts
Math.random < 0.5;   // 错误：比较的是函数本身
Math.random() < 0.5; // 正确：比较函数返回值
```

#### 不可能成立的逻辑

```ts
const value = Math.random() < 0.5 ? "a" : "b";

if (value !== "a") {
  // 这里 value 已经只能是 "b"
} else if (value === "b") {
  // 永远无法到达
}
```

这体现了 TypeScript 一个重要能力：它不仅检查类型名称，还会根据程序流程分析变量当前可能的取值。

***

### 1.3. 类型也能增强编辑器功能

类型信息不仅用来报错，也能支持：

* 自动补全
* 参数提示
* 跳转到定义
* 查找所有引用
* 自动重构
* 快速修复
* 鼠标悬停查看类型

因此，TypeScript 的价值不只是“少出错”，也包括“更容易阅读、修改和重构代码”。

***

### 1.4. `tsc` 编译器

`tsc` 是 TypeScript 官方编译器。页面展示的是全局安装方式；实际项目中更推荐把它安装为项目开发依赖：

```bash
npm init -y
npm install --save-dev typescript
npx tsc --init
```

创建 `hello.ts`：

```ts
console.log("Hello world!");
```

编译：

```bash
npx tsc hello.ts
```

通常会生成：

```text
hello.ts
hello.js
```

执行的是生成后的 JavaScript：

```bash
node hello.js
```

完整流程是：

```text
hello.ts
   ↓ TypeScript 类型检查与转换
hello.js
   ↓ JavaScript 运行环境
程序结果
```

***

### 1.5. 默认情况下，有类型错误也可能生成 JavaScript

例如：

```ts
function greet(person: string, date: Date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}

greet("Alice"); // 缺少第二个参数
```

`tsc` 会报告错误，但默认情况下仍可能输出 JavaScript。这是为了方便旧 JavaScript 项目逐步迁移到 TypeScript。

新项目通常应该禁止这种行为：

```json
{
  "compilerOptions": {
    "noEmitOnError": true
  }
}
```

或者：

```bash
npx tsc --noEmitOnError
```

如果项目使用其他工具负责生成 JavaScript，还可以只做检查：

```bash
npx tsc --noEmit
```

***

### 1.6. 显式类型标注

类型标注写在变量或参数名称之后：

```ts
function greet(person: string, date: Date): void {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}
```

含义分别是：

* `person: string`：参数必须是字符串。
* `date: Date`：参数必须是 `Date` 对象。
* `: void`：函数不返回有意义的值。

注意 `Date()` 和 `new Date()` 不一样：

```ts
Date();     // 返回 string
new Date(); // 返回 Date 对象
```

所以：

```ts
greet("Alice", Date());     // 错误
greet("Alice", new Date()); // 正确
```

***

### 1.7. 类型推断

并非所有地方都需要手动写类型：

```ts
let message = "hello";
// TypeScript 推断 message 为 string
```

下面的写法通常没有必要：

```ts
let message: string = "hello";
```

比较实用的原则是：

* 函数参数通常写类型。
* 公共函数的返回值可以显式标注。
* 普通局部变量尽量让 TypeScript 推断。
* 推断结果不够准确时再补充类型。

例如：

```ts
function add(a: number, b: number): number {
  return a + b;
}

const result = add(10, 20); // 自动推断为 number
```

***

### 1.8. 类型会在编译后被擦除

下面的 TypeScript：

```ts
function greet(person: string): string {
  return `Hello ${person}`;
}
```

编译成 JavaScript 后大致是：

```js
function greet(person) {
  return `Hello ${person}`;
}
```

`string` 等类型信息消失了。官方文档强调：**类型标注不会改变程序的运行时行为。**

这会带来一个非常重要的结论：

```ts
type User = {
  name: string;
};

const data = JSON.parse(input) as User;
```

写成 `as User` 并不会检查输入中是否真的存在 `name`。它只是告诉编译器“请把它当作 `User`”。

对于 API、JSON、表单等外部数据，仍然需要运行时校验：

```ts
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "name" in value &&
    typeof value.name === "string"
  );
}
```

***

### 1.9. 降级编译（downleveling）

TypeScript 可以把较新的 JavaScript 语法转换为较旧的语法。

例如：

```ts
const message = `Hello ${name}`;
```

面向旧环境时可能转换为：

```js
var message = "Hello ".concat(name);
```

由 `target` 决定输出哪个版本的 JavaScript：

```json
{
  "compilerOptions": {
    "target": "ES2022"
  }
}
```

需要区分两个概念：

* `target`：生成什么版本的 JavaScript。
* `lib`：类型检查时允许使用哪些平台 API。

例如，能否使用 `document` 不只是由 `target` 决定，还取决于是否包含 DOM 类型库。

***

### 1.10. 严格模式

新项目建议启用：

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict` 是一组严格检查选项的总开关，其中页面重点介绍了两个。

#### `noImplicitAny`

如果 TypeScript 无法推断参数类型，宽松模式下可能退化为 `any`：

```ts
function printName(name) {
  console.log(name.toUpperCase());
}
```

开启严格检查后，必须明确说明类型：

```ts
function printName(name: string): void {
  console.log(name.toUpperCase());
}
```

#### `strictNullChecks`

开启后，`null` 和 `undefined` 不再能随意赋给其他类型：

```ts
function findUser(): string | undefined {
  return Math.random() > 0.5 ? "Alice" : undefined;
}

const user = findUser();
console.log(user.toUpperCase()); // 错误：user 可能是 undefined
```

必须先缩小类型范围：

```ts
if (user !== undefined) {
  console.log(user.toUpperCase());
}
```

或者在适合默认值的场景使用：

```ts
console.log((user ?? "Guest").toUpperCase());
```

## 2、知识扩展

### 2.1. `any` 和 `unknown` 的区别

`any` 基本等于关闭类型检查：

```ts
let value: any = "hello";

value.notExist();
value();
value.foo.bar;
```

这些操作编译器可能都不阻止。

`unknown` 表示“类型暂时不知道”，使用前必须检查：

```ts
let value: unknown = "hello";

if (typeof value === "string") {
  console.log(value.toUpperCase());
}
```

处理外部数据时，优先使用 `unknown`，尽量避免 `any`。

***

### 2.2. TypeScript 采用结构类型系统

TypeScript 主要关心对象“长什么样”，而不是它叫什么名字：

```ts
type Person = {
  name: string;
};

const employee = {
  name: "Alice",
  department: "Engineering",
};

function greet(person: Person): void {
  console.log(person.name);
}

greet(employee); // 合法，因为 employee 至少具有 name: string
```

这种机制称为结构类型（structural typing），也可以简单理解成“鸭子类型的静态版本”。

***

### 2.3. 类型缩小（narrowing）

TypeScript 会根据条件判断，把宽泛类型缩小成更具体的类型：

```ts
function format(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // 此处是 string
  }

  return value.toFixed(2); // 此处是 number
}
```

常见的缩小方式包括：

* `typeof`
* `instanceof`
* `in`
* 判空
* 字面量比较
* 自定义类型守卫

这是学完基础后最值得继续掌握的能力之一。

***

### 2.4. TypeScript 不能保证程序绝对安全

TypeScript 擅长发现：

* 参数类型不匹配
* 属性不存在
* 可能为空
* 拼写错误
* 某些不可能成立的逻辑

但它通常不能独立发现：

* API 返回了错误格式的数据
* 用户输入不合法
* 数据库内容不符合预期
* 网络错误
* 业务规则错误
* 数组访问越界等运行时问题

所以正确认识是：

> TypeScript 提高了程序的静态可靠性，但不能替代运行时校验、测试和错误处理。

​

​

# 七、Everyday Types

原文地址：[https://www.typescriptlang.org/docs/handbook/2/everyday-types.html](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)​

***

这篇 [TypeScript Handbook：Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) 介绍开发中最常用的类型，是后续学习类型缩小、函数、泛型的基础。

核心思想是：

> TypeScript 使用基本类型描述数据，再通过数组、对象、联合类型、字面量类型等方式组合出复杂类型。

## 1、基本类型

### 1. `string`、`number`、`boolean`

```ts
const username: string = "Alice";
const age: number = 20;
const active: boolean = true;
```

JavaScript 不区分整数和浮点数，统一使用 `number`：

```ts
const count: number = 10;
const price: number = 19.99;
```

类型名称应该使用小写：

```ts
let name: string;   // 推荐
let age: number;
let active: boolean;
```

不要使用包装对象类型：

```ts
let name: String;   // 不推荐
let age: Number;
let active: Boolean;
```

`string` 表示普通字符串值，而 `String` 表示 JavaScript 的字符串包装对象。日常开发几乎总是使用小写版本。

***

### 2. 数组

有两种等价写法：

```ts
const scores: number[] = [90, 85, 100];
const names: Array<string> = ["Alice", "Bob"];
```

通常简单类型使用 `T[]` 更易读：

```ts
string[]
number[]
User[]
```

复杂类型有时使用泛型形式更清楚：

```ts
Array<string | number>
```

注意：

```ts
number[] // 任意长度的数字数组
[number] // 只能包含一个数字的元组
```

知识扩展：如果数组不应该被修改，可以使用只读数组。

```ts
const names: readonly string[] = ["Alice", "Bob"];

names.push("Eve"); // 错误
```

***

## 2、`any`

`any` 会关闭相关值的类型检查：

```ts
let value: any = { name: "Alice" };

value.foo.bar();
value();
value = 100;

const age: number = value;
```

上面的代码基本都不会产生编译错误，但运行时可能崩溃。

因此建议：

* 开启 `strict` 或 `noImplicitAny`。
* 不知道类型时优先使用 `unknown`。
* 只有迁移旧项目或处理确实无法描述的第三方数据时，才临时使用 `any`。

### `any` 和 `unknown`

```ts
let input: unknown = "hello";

input.toUpperCase(); // 错误：还不知道 input 是什么

if (typeof input === "string") {
  input.toUpperCase(); // 正确
}
```

区别可以简单记成：

| **类型**    | **含义**        |
| --------- | ------------- |
| `any`     | 不检查，我自己负责     |
| `unknown` | 暂时不知道，使用前必须检查 |

***

## 3、类型标注和类型推断

类型标注写在变量名称后面：

```ts
let username: string = "Alice";
```

但如果 TypeScript 能够推断，就不必重复：

```ts
let username = "Alice"; // 推断为 string
let age = 20;           // 推断为 number
let active = true;      // 推断为 boolean
```

推荐原则：

```ts
// 局部变量：优先推断
const price = 99;

// 函数参数：通常显式标注
function double(value: number) {
  return value * 2;
}

// 公共函数返回值：可以显式标注
function getUsername(): string {
  return "Alice";
}
```

类型推断不等于类型永远固定为初始值：

```ts
let status = "loading";
// status 被推断为 string，而不是字面量 "loading"

status = "success"; // 合法
```

***

## 4、函数类型

### 1. 参数类型

```ts
function greet(name: string) {
  console.log(name.toUpperCase());
}

greet("Alice"); // 正确
greet(42);      // 错误
```

即使参数没有类型标注，TypeScript 仍然会检查参数数量：

```ts
function add(a, b) {
  return a + b;
}

add(1); // 缺少一个参数
```

不过在严格模式下，`a` 和 `b` 会产生隐式 `any` 错误，因此应写成：

```ts
function add(a: number, b: number): number {
  return a + b;
}
```

### 2. 返回值类型

```ts
function getAge(): number {
  return 20;
}
```

返回值通常也能自动推断：

```ts
function getAge() {
  return 20; // 推断返回 number
}
```

显式标注返回值的优点是能防止函数实现被意外修改：

```ts
function getAge(): number {
  return "20"; // 立即报错
}
```

### 3. 异步函数

`async` 函数的返回类型是 `Promise<T>`：

```ts
async function getUsername(): Promise<string> {
  return "Alice";
}
```

注意不是：

```ts
async function getUsername(): string {
  return "Alice";
}
// 错误：async 函数返回 Promise
```

### 4. 上下文类型推断

```ts
const names = ["Alice", "Bob", "Eve"];

names.forEach((name) => {
  console.log(name.toUpperCase());
});
```

虽然没有给 `name` 添加类型标注，TypeScript 根据 `names` 是 `string[]`，推断出回调参数是 `string`。

这种根据代码所在位置推断类型的方式称为上下文类型推断。

***

## 5、对象类型

可以直接描述对象的结构：

```ts
function printUser(user: { name: string; age: number }) {
  console.log(user.name);
  console.log(user.age);
}

printUser({
  name: "Alice",
  age: 20,
});
```

TypeScript 采用结构类型系统：只关心对象是否具有需要的属性，而不关心它是如何创建的。

```ts
const employee = {
  name: "Bob",
  age: 30,
  department: "Development",
};

printUser(employee); // 合法
```

`employee` 多出一个 `department` 属性没有关系，因为它已经拥有 `name` 和 `age`。

### 可选属性

属性名后添加 `?`：

```ts
type User = {
  name: string;
  nickname?: string;
};
```

下面两种对象都合法：

```ts
const alice: User = {
  name: "Alice",
};

const bob: User = {
  name: "Bob",
  nickname: "Bobby",
};
```

读取可选属性时，它可能是 `undefined`：

```ts
function printNickname(user: User) {
  user.nickname.toUpperCase();
  // 错误：nickname 可能是 undefined
}
```

安全处理方式：

```ts
function printNickname(user: User) {
  if (user.nickname !== undefined) {
    console.log(user.nickname.toUpperCase());
  }
}
```

或者使用可选链和默认值：

```ts
console.log(user.nickname?.toUpperCase());
console.log(user.nickname?.toUpperCase() ?? "NO NICKNAME");
```

需要区分：

```ts
nickname?: string;
```

表示属性可以不存在。

```ts
nickname: string | undefined;
```

表示属性必须存在，但值可以是 `undefined`。

启用 `exactOptionalPropertyTypes` 后，这种区别会更加严格。

***

## 6、联合类型

联合类型表示一个值可能属于多个类型中的任意一个：

```ts
type ID = string | number;

function printId(id: ID) {
  console.log(id);
}

printId(100);
printId("USER-100");
```

### 只能直接使用共有能力

```ts
function printId(id: string | number) {
  id.toUpperCase();
  // 错误：number 没有 toUpperCase
}
```

必须先进行类型缩小：

```ts
function printId(id: string | number) {
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id.toFixed(0));
  }
}
```

对于数组可以使用 `Array.isArray()`：

```ts
function welcome(value: string | string[]) {
  if (Array.isArray(value)) {
    console.log(value.join(", "));
  } else {
    console.log(value.toUpperCase());
  }
}
```

如果联合类型中的所有成员都支持某个操作，可以直接使用：

```ts
function firstThree(value: string | number[]) {
  return value.slice(0, 3);
}
```

`string` 和数组都有 `slice()`，因此不需要先缩小。

***

## 7、类型别名 `type`

类型别名可以给任意类型起一个名字：

```ts
type Point = {
  x: number;
  y: number;
};

type ID = string | number;

type Status = "loading" | "success" | "error";
```

使用类型别名能减少重复：

```ts
function printPoint(point: Point) {
  console.log(point.x, point.y);
}
```

但别名不会创造一个全新的运行时类型：

```ts
type SanitizedString = string;

let value: SanitizedString = "ordinary string"; // 仍然合法
```

`SanitizedString` 本质上仍然只是 `string` 的另一个名字。

***

## 8、接口 `interface`

接口专门用于描述对象结构：

```ts
interface User {
  name: string;
  age: number;
}

function printUser(user: User) {
  console.log(user.name);
}
```

### `type` 和 `interface` 的区别

两者描述普通对象时非常相似：

```ts
type UserType = {
  name: string;
};

interface UserInterface {
  name: string;
}
```

主要区别：

| **能力**          | **`interface`** | **`type`** |
| --------------- | --------------- | ---------- |
| 描述对象            | 支持              | 支持         |
| 描述联合类型          | 不支持             | 支持         |
| 描述基本类型别名        | 不支持             | 支持         |
| 使用 `extends` 继承 | 支持              | 可用交叉类型实现   |
| 同名声明合并          | 支持              | 不支持        |

接口继承：

```ts
interface Animal {
  name: string;
}

interface Bear extends Animal {
  honey: boolean;
}
```

类型交叉：

```ts
type Animal = {
  name: string;
};

type Bear = Animal & {
  honey: boolean;
};
```

接口可以声明合并：

```ts
interface WindowConfig {
  title: string;
}

interface WindowConfig {
  width: number;
}

// 最终同时具有 title 和 width
```

实用选择原则：

* 普通、可扩展的对象模型：优先考虑 `interface`。
* 联合类型、元组、映射类型等组合类型：使用 `type`。
* 团队已有统一风格：遵循项目约定。
* 不要为了选择它们而过度纠结。

***

## 9、类型断言

类型断言表示：“我比编译器更清楚这个值的类型。”

```ts
const canvas = document.getElementById(
  "main-canvas",
) as HTMLCanvasElement;
```

也有另一种写法：

```ts
const canvas =
  <HTMLCanvasElement>document.getElementById("main-canvas");
```

但尖括号写法不能在 `.tsx` 中正常使用，因此通常统一使用 `as`。

### 断言不是类型转换

```ts
const value = "123" as unknown as number;
```

运行时的 `value` 仍然是字符串，不会变成数字。

真正转换数据应使用：

```ts
const value = Number("123");
```

也就是说：

* `as number`：只影响编译器。
* `Number(value)`：真正影响运行时数据。

避免为了消除错误而滥用双重断言：

```ts
value as unknown as User;
```

这种写法通常意味着类型设计或运行时校验存在问题。

***

## 10、字面量类型

字面量类型表示某一个具体值：

```ts
let direction: "left";

direction = "left";  // 正确
direction = "right"; // 错误
```

单独使用意义不大，但与联合类型结合非常实用：

```ts
type Direction = "left" | "right" | "center";

function align(direction: Direction) {
  // ...
}

align("left");
align("center");
align("top"); // 错误
```

也可以使用数字字面量：

```ts
function compare(a: string, b: string): -1 | 0 | 1 {
  return a === b ? 0 : a > b ? 1 : -1;
}
```

字面量联合类型经常比枚举更加轻量：

```ts
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type Theme = "light" | "dark";
type RequestState = "idle" | "loading" | "success" | "error";
```

***

## 11、字面量推断和 `as const`

注意下面的对象：

```ts
const request = {
  url: "/users",
  method: "GET",
};
```

虽然变量使用了 `const`，但对象属性仍然可以修改：

```ts
request.method = "DELETE";
```

所以 TypeScript 把 `request.method` 推断为 `string`，而不是字面量 `"GET"`。

如果函数只接受固定方法：

```ts
function send(method: "GET" | "POST") {}

send(request.method); // 可能报错：request.method 是 string
```

可以使用 `as const`：

```ts
const request = {
  url: "/users",
  method: "GET",
} as const;
```

此时大致推断为：

```ts
{
  readonly url: "/users";
  readonly method: "GET";
}
```

注意：

> `const` 防止变量重新赋值；`as const` 让对象属性在类型层面成为只读字面量。

### 延伸：`satisfies`

如果既想检查对象是否符合某种结构，又想保留精确推断，可以使用 `satisfies`：

```ts
type RequestConfig = {
  url: string;
  method: "GET" | "POST";
};

const request = {
  url: "/users",
  method: "GET",
} satisfies RequestConfig;
```

与 `as RequestConfig` 相比，`satisfies` 更侧重“检查”，不会简单地用目标类型覆盖原有推断。

***

## 12、`null` 和 `undefined`

它们都表示“缺少值”，但含义通常不同：

* `undefined`：尚未提供、属性不存在。
* `null`：显式表示没有值。

开启 `strictNullChecks` 后，必须显式处理：

```ts
function printName(name: string | null) {
  if (name === null) {
    console.log("No name");
  } else {
    console.log(name.toUpperCase());
  }
}
```

也可以使用空值合并：

```ts
function displayName(name: string | null | undefined) {
  return name ?? "Anonymous";
}
```

`??` 与 `||` 不完全相同：

```ts
0 || 10; // 10
0 ?? 10; // 0

"" || "default"; // "default"
"" ?? "default"; // ""
```

`??` 只把 `null` 和 `undefined` 当成缺少值。

### 非空断言 `!`

```ts
const element = document.getElementById("app");

element!.textContent = "Hello";
```

`!` 告诉 TypeScript：“它绝对不是 `null` 或 `undefined`。”

但它不会添加运行时检查。如果元素不存在，程序仍然会崩溃。更安全的写法是：

```ts
const element = document.getElementById("app");

if (element !== null) {
  element.textContent = "Hello";
}
```

只在能由程序逻辑严格保证非空时使用 `!`。

***

## 13、枚举 `enum`

```ts
enum Direction {
  Up,
  Down,
  Left,
  Right,
}
```

与大多数 TypeScript 类型不同，`enum` 通常会生成运行时代码。官方文档建议知道它的存在，但不要急着使用。

很多场景可以使用字面量联合代替：

```ts
type Direction = "up" | "down" | "left" | "right";
```

也可以使用常量对象：

```ts
const Direction = {
  Up: "up",
  Down: "down",
  Left: "left",
  Right: "right",
} as const;

type Direction = typeof Direction[keyof typeof Direction];
```

初学阶段建议：

* 只需要限制字符串取值：使用字面量联合。
* 必须提供运行时对象或项目已有约定：再考虑 `enum`。

***

## 14、`bigint` 和 `symbol`

### `bigint`

用于表示超过普通 `number` 安全整数范围的大整数：

```ts
const amount1: bigint = BigInt(100);
const amount2: bigint = 100n;
```

不能直接混合 `number` 和 `bigint`：

```ts
1n + 1;  // 错误
1n + 1n; // 正确
```

使用 `bigint` 字面量时，编译目标通常需要支持 ES2020 或更高版本。

### `symbol`

每个 `Symbol()` 都是唯一值：

```ts
const first = Symbol("name");
const second = Symbol("name");

console.log(first === second); // false
```

即使描述文字相同，它们也不是同一个值。`symbol` 常用于创建不会发生命名冲突的对象键。

***

## 15、综合示例

```ts
type UserStatus = "active" | "disabled";

interface User {
  id: string | number;
  name: string;
  nickname?: string;
  status: UserStatus;
}

function formatUser(user: User): string {
  const nickname = user.nickname?.toUpperCase() ?? "NONE";

  return [
    `ID: ${user.id}`,
    `Name: ${user.name}`,
    `Nickname: ${nickname}`,
    `Status: ${user.status}`,
  ].join(", ");
}

const user = {
  id: 1001,
  name: "Alice",
  status: "active",
} satisfies User;

console.log(formatUser(user));
```

这个例子同时使用了：

* 对象类型
* `interface`
* 联合类型
* 字面量类型
* 可选属性
* 可选链 `?.`
* 空值合并 `??`
* 返回值类型
* `satisfies`

## 16、速查表

| **写法**             | **含义**     |
| ------------------ | ---------- |
| `string`           | 字符串        |
| `number`           | 数字         |
| `boolean`          | 布尔值        |
| `string[]`         | 字符串数组      |
| `Array<string>`    | 字符串数组      |
| `name?: string`    | 可选属性       |
| `string \| number` | 联合类型       |
| `"GET" \| "POST"`  | 字面量联合      |
| `type A = ...`     | 类型别名       |
| `interface A {}`   | 对象接口       |
| `value as T`       | 类型断言       |
| `value!`           | 非空断言       |
| `as const`         | 保留字面量并设为只读 |
| `unknown`          | 未知类型，使用前检查 |
| `any`              | 关闭类型检查     |

最值得牢牢记住的三点是：

1. **优先利用类型推断，不必为每个变量手写类型。**
2. **联合类型只能直接使用所有成员共有的能力，其他操作需要先缩小类型。**
3. **类型断言和非空断言不会进行运行时检查，不能把它们当作数据转换或安全验证。**

下一章是 [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)，会系统讲解如何通过 `typeof`、判空、`in`、`instanceof` 和控制流分析缩小联合类型。

​

​

​

​

​

​

​

​

​
