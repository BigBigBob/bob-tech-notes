---
translation_id: typescript-basics
description: "TypeScript type inference, structural typing, modules, compiler settings, and everyday types."
---

# TypeScript Fundamentals



The official documentation link: [~https://www.typescriptlang.org/zh/docs/~](https://www.typescriptlang.org/zh/docs/)



## 1. TypeScript for JavaScript Programmers

Original address: [https://www.typescriptlang.org/zh/docs/handbook/typescript-in-5-minutes.html](https://www.typescriptlang.org/zh/docs/handbook/typescript-in-5-minutes.html)

Summary of content and knowledge development.

***

The core of this document is: **TypeScript = JavaScript + Static Type System**. It does not replace JavaScript. Instead, it checks for type errors before code execution, and provides the editor with more reliable completion, navigation, and refactoring capabilities. [Official documentation for TypeScript](https://www.typescriptlang.org/zh/docs/handbook/typescript-in-5-minutes.html)

### 1. Summary

#### 1.1. Type inference

TypeScript can often automatically determine the type based on assignments, eliminating the need to manually specify types everywhere.

```ts
let message = "Hello";
// TypeScript infers that message is a string.

message = 123;
// Error: number cannot be assigned to string.
```

Recommended principle: When it is clear what **represents, let TypeScript do the inference for you.**

```ts
const count = 10; // There is no need to write const count: number = 10.
```

Function parameters usually need to be annotated, because TypeScript doesn’t know what the caller will pass in.

```ts
function double(value: number) {
  return value * 2;
}
```

The return value `number` can be inferred automatically.

***

#### 1.2. Using interface description objects

`interface` describes what structure the object should have:

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

If an attribute is missing, the attribute type is incorrect, or an unknown attribute is written directly, TypeScript will give a prompt:

```ts
const user: User = {
  name: "小明",
  id: "1", // Error: It should be "number".
};
```

The interface can also be used for function parameters and return values:

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

Any class that has a structure that meets the interface requirements can also be considered as belonging to that interface type:

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

#### 1.3. Common special types

In addition to types like `string`, `number`, and `boolean` in JavaScript, TypeScript also provides:

| **Type** | **Meaning** |
| -------------------- | ------------ |
| `any`                | Abandon type checking and use it as little as possible.  |
| `unknown`            | The type is unknown and can only be used after checking |
| `void`               | The function does not have a meaningful return value  |
| `never`              | No such value can occur.     |
| `null` / `undefined` | Empty or undefined value       |

```ts
function log(message: string): void {
  console.log(message);
}

function fail(message: string): never {
  throw new Error(message);
}
```

`unknown` is safer than `any`:

```ts
function printValue(value: unknown) {
  // console.log(value.toUpperCase()); // Error

  if (typeof value === "string") {
    console.log(value.toUpperCase()); // Clear.
  }
}
```

***

#### 1.4. Combined Types

The combined type is represented by `|`, which means “possibly one of these types”.

```ts
let id: string | number;

id = 100;
id = "A100";
```

Combined types can also limit the valid values:

```ts
type Status = "loading" | "success" | "error";

let status: Status = "loading";
// status = "finished"; // Error
```

This is called the **string literal union type**. It is more restrictive than using `string` arbitrarily.

***

#### 1.5. Type narrowing

If a value has a composite type, it is often necessary to determine which type it currently is:

```ts
function formatId(id: string | number): string {
  if (typeof id === "string") {
    return id.toUpperCase();
  }

  return id.toFixed(0);
}
```

In the `if` branch, TypeScript knows that `id` is equal to `string`. In the remaining parts of the path, it knows that it is equal to `number`. This process is called **Narrowing (Type Narrowing)**.

Common ways to perform the check:

```ts
typeof value === "string"
typeof value === "number"
Array.isArray(value)
value instanceof Date
"property" in value
```

Note: You cannot use `typeof value === "array"` to check the array, because in JavaScript, the result of array `typeof` is `"object"`.

***

#### 1.6. Generics

Generics can be understood as “parameters of types”.

```ts
const names: Array<string> = ["小明", "小红"];
const scores: Array<number> = [90, 85];
```

You can also write your own generics:

```ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const name = first(["小明", "小红"]);
// Inference to String  ⁇ undefined

const score = first([90, 85]);
// Inference to number  ⁇  undefined
```

Here. `T` The value of the generics is: **Keep the exact type of information while reusing the code.**

***

#### 1.7. Structured Type System

TypeScript looks primarily at what a value has, rather than whether it clearly states a certain type:

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

printPoint(position); // Yeah.
```

Although `position` is not declared as `Point`, it has `x` and `y` associated with it. Moreover, its type is correct, so it can be used.

This is called the **structural type**. It is also commonly referred to as “duck type”: if it has the required shape and behavior, it can be used as that type.

### 2. Background for beginners

#### 2.1. TypeScript only checks types during the development phase.

TypeScript will eventually be compiled into JavaScript:

```ts
const age: number = 18;
```

The compilation is roughly:

```js
const age = 18;
```

The type annotations are not preserved during runtime. Therefore, TypeScript cannot automatically validate external data in interfaces, forms, or JSON documents.

```ts
const response = await fetch("/api/user");
const data = await response.json();
```

The content returned by the server may still not meet expectations. Real-world projects usually use runtime checks or data validation libraries like Zod.

***

#### How to choose between `2.2.interface` and `type`

Both can describe objects:

```ts
interface User {
  name: string;
}

type Product = {
  name: string;
};
```

Simple selection method:

* Describe the common structure of objects or classes: `interface` is preferred.
* Combined types, tuples, or composite types: Use `type`.
* The team has established a unified standard: follow the team's guidelines.

```ts
type Result =
  | { success: true; data: string }
  | { success: false; error: string };
```

Do not interpret them as competitive relationships; each has its own area of expertise.

***

#### 2.3. Optional properties and read-only properties

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
// user.id = 2; // Error: id is a read-only property
```

* `email?`: The attribute may not exist.
* `readonly`: When referenced by this type, it cannot be reassigned.

***

#### 2.4. Arrays, tuples, and ordinary objects

```ts
const numbers: number[] = [1, 2, 3];

const coordinate: [number, number] = [10, 20];

const scores: Record<string, number> = {
  Alice: 95,
  Bob: 88,
};
```

* Array: Elements of the same type, with a length that is not fixed.
* Tuples: They have a clear meaning for both position and length.
* `Record<K, V>`: The key and value both have the same type.

***

#### 2.5. Start strict checking as early as possible.

It is recommended to enable the strict mode for learning and new projects:

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

It enables stricter checks for null values, function parameters, and properties. There will be more errors at the beginning, but it helps you develop more reliable type habits.

### 3. A comprehensive example

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

This example includes:

* Object interface
* Function parameters and return values
* Literal union type
* Optional properties
* Read-only properties
* `undefined` type

### 4. Recommended order of learning

1. JavaScript Basics: Variables, Functions, Objects, Arrays, and Modules
2. Basic Types and Type Inference in TypeScript
3. Object type, `interface`, and `type`
4. Conjoined types and type narrowing
5. Function type
6. Generic types
7. Classes and modules
8. Tool types: `Partial`, `Pick`, `Omit`, `Record`
9. `tsconfig.json` and strict mode

The most important mindset when learning TypeScript is not to “assign types to all variables,” but rather:

> Use types to describe what data can be, what it cannot be, and the relationships between different types of data.



What does the === in the expression typeof value === "string" mean?

***

`===` is **from JavaScript/TypeScript, which is strictly equivalent to the potor** to determine whether the values and types on both sides are equal.

```ts
typeof value === "string"
```

It can be understood in two steps:

```ts
typeof value
```

Obtain the type name of `value` at runtime, such as `"string"`, `"number"`.

```ts
typeof value === "string"
```

Determine whether this type name is exactly equal to `"string"`, that is, determine whether `value` is a string.

```ts
const value = "你好";

console.log(typeof value);              // "string"
console.log(typeof value === "string"); // true
```

#### The difference between `===` and `==`

`===` does not automatically convert type, while `==` may be converted first and compared:

```ts
5 === 5;   // true
5 === "5"; // False: The types are different.

5 == "5";  // true: The string "5" is converted before comparison.
```

It is generally recommended to use `===`, as its behavior is clearer and less likely to cause unexpected results.

In TypeScript, this kind of judgment also triggers type narrowing of **:**.

```ts
function print(value: string | number) {
  if (typeof value === "string") {
    // Here, TypeScript knows the value is string
    console.log(value.toUpperCase());
  } else {
    // Here, TypeScript knows that value is number
    console.log(value.toFixed(2));
  }
}
```



## 2. TypeScript for Java/C# Programmers

[: https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html)

Summary of page content and knowledge outreach

***

This article is primarily aimed at programmers familiar with Java/C#. However, it is also valuable for beginners. What it emphasizes is not the syntax of TypeScript, but a key concept:

> Although TypeScript has classes, interfaces, and static typing, its underlying foundation is still JavaScript. Therefore, it cannot be completely applied using the mindset of Java/C#.

The following is based on [Official TypeScript documentation: TypeScript for Java/C# Programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html).

### 1. Start with JavaScript

TypeScript does not change the way JavaScript is executed.

For example:

* How do strings be converted into numbers?
* How to iterate through an array
* How does the asynchronous request work?
* How the file is read
* How do objects and prototypes work?

These are knowledge that still belongs to JavaScript.

```ts
const text: string = "123";
const value: number = Number(text);
```

`: string` and `: number` are TypeScript type annotations. It’s JavaScript’s `Number()` that actually converts strings into numbers.

After compilation, the types will disappear:

```js
const text = "123";
const value = Number(text);
```

Therefore, when learning TypeScript, it's also important to learn JavaScript. In particular:

* Objects and arrays
* The function
* Module
* Closure
* `this`
* Promise and `async/await`
* JavaScript's type conversion rules

### 2. Rethinking classes

Common approaches in Java/C#

In Java/C#, data and functions are usually placed within classes:

```java
class MathUtils {
    static int add(int a, int b) {
        return a + b;
    }
}
```

Common ways of writing in TypeScript/JavaScript

JavaScript allows functions to exist independently, without the need to create classes for organizational purposes:

```ts
export function add(a: number, b: number): number {
  return a + b;
}
```

Data can also be ordinary objects:

```ts
interface User {
  name: string;
  age: number;
}

function introduce(user: User): string {
  return `我是${user.name}，今年${user.age}岁`;
}
```

`UserService`, `UserUtils` or other packagings are not required.

It is usually not necessary to have static utility classes.

Not recommended to mimic Java.

```ts
class StringUtils {
  static capitalize(value: string): string {
    return value[0].toUpperCase() + value.slice(1);
  }
}
```

Directly exporting functions is usually simpler:

```ts
export function capitalize(value: string): string {
  return value[0].toUpperCase() + value.slice(1);
}
```

JavaScript modules can already provide:

* Namespace
* Private scope
* Singleton loading
* Import and Export

But the class isn’t completely unusable.

When the problem itself can be expressed using objects to represent states and behaviors, classes are still a good choice:

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

TypeScript supports the familiar object-oriented features:

* `class`
* `extends`
* `implements`
* `public`
* `protected`
* `private`
* `abstract`
* `static`

The core principle is: **should be selected based on the problem, rather than being created to organize the code.**

### 3. Understand types as “collections of values”.

This is one of the most important ideas in the article.

```ts
type Text = string;
```

It can be understood as follows: `Text` represents a collection of all strings.

```ts
type Id = string | number;
```

`Id` represents the union of the set of strings and the set of numbers:

```text
set of strings ─┐
             ├─ string | number
set of numbers ─┘
```

Therefore, all of the following values are `Id`:

```ts
let id: string | number;

id = "A100";
id = 100;
```

However:

```ts
id = true; // Error
```

Because `true` does not belong to the set `string | number`.

A value can belong to multiple types.

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

`person` matches the pattern:

* `Named`
* `Employee`
* `{ name: string; employeeId: number }`

So, a value doesn’t necessarily have only one unique TypeScript type.

### 4. Structural typing

Java/C# primarily uses a nominal type system like ****: It is necessary to explicitly declare the relationships between types.

For example:

```java
class Dog implements Animal {}
```

TypeScript primarily uses the **structural type system**. The key point is that an object has certain properties, rather than specifying which type it belongs to.

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

printPoint(position); // Yeah.
```

`position` No explicit declaration `Point`, but it has:

```ts
x: number;
y: number;
```

So, it can be passed to `printPoint()`.

It can be simply understood as:

> Regardless of what type you are, all that matters is whether you have the structure that I need.

### 5. Consequences of structural typing

#### 1. The empty type can accept almost any object.

```ts
class Empty {}

function handle(value: Empty): void {}

handle({ name: "小明" }); // Yeah.
handle({ count: 10 });    // Yeah.
```

Why?

`Empty` does not require any attributes. Any object has all the attributes it requires -- because it doesn't require anything.

So, the empty interface doesn’t have the effect of “any object must explicitly implement it”.

```ts
interface Empty {}

const value: Empty = { anything: 123 };
```

So do not use an empty interface as a tag interface in Java.

***

#### 2. Classes with the same structure may be compatible with each other.

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

let car: Car = new Golfer(); // Yeah.
```

Although the business meanings are completely different, the structures that TypeScript recognizes are all of the following:

```ts
{
  drive(): void;
}
```

So the two are compatible.

However, if the class contains members like `private` or `protected`, the compatibility rules become even stricter:

```ts
class Car {
  private brand = "car";

  drive(): void {}
}

class Golfer {
  private brand = "golfer";

  drive(): void {}
}

// Let car: Car = new Golfer(); // Error
```

### 6. Type erasure

In TypeScript, interfaces, type aliases, and generics are primarily used during the compilation phase.

```ts
interface User {
  name: string;
}

const user: User = {
  name: "小明",
};
```

After compiling to JavaScript, it would look like this:

```js
const user = {
  name: "小明",
};
```

Runtime does not exist `User` this interface.

So, this is not possible:

```ts
interface User {
  name: string;
}

// if (value instanceof User) {} // Error: User is not a runtime value
```

`interface` exists only in "type space" and cannot be passed to `instanceof`.

### 7. Limits of `typeof` and `instanceof`

#### `typeof`

`typeof` can be used to check the basic runtime types of JavaScript:

```ts
function print(value: string | number): void {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  } else {
    console.log(value.toFixed(2));
  }
}
```

Common results include:

```ts
typeof "hello";       // "string"
typeof 123;           // "number"
typeof true;          // "boolean"
typeof undefined;     // "undefined"
typeof (() => {});    // "function"
typeof {};            // "object"
typeof [];            // "object"
typeof null;          // "object" (a legacy behavior from JavaScript history)
```

The result of `typeof new Car()` is also `"object"`; `"Car"` will not be obtained.

#### `instanceof`

The class exists as a real JavaScript value at runtime, so you can use `instanceof`:

```ts
class Car {
  drive(): void {}
}

const value = new Car();

console.log(value instanceof Car); // true
```

However, `instanceof` checks the prototype chain of the object, not the TypeScript interface structure.

### 8. Checking interface-shaped values at runtime

If the data comes from an interface, a file, or user input, you cannot simply perform a type assertion:

```ts
const user = JSON.parse(text) as User;
```

`as User` will not verify the data, just tell the compiler "Believe me."

A safer way is to write type guards:

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

In real projects, runtime verification libraries like Zod and Valibot are also commonly used.

### 9. When you need nominal typing

Sometimes, two value structures may be identical, but they must not be used interchangeably in business scenarios. For example, user ID and order ID should not be mixed together.

```ts
type UserId = string;
type OrderId = string;

const userId: UserId = "U100";
const orderId: OrderId = userId; // Yes, but it may not be business-wise reasonable.
```

You can use “brand types” to simulate nominal types:

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

// const orderId: OrderId = userId; // Incorrect
```

This notation is commonly used for:

* Different types of IDs
* Different currencies
* Verified and unverified data
* Different units of measurement

### 10. Modeling object types with discriminated unions

Instead of relying on complex class inheritance, sometimes union types can be used:

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

`kind` is the identification of different types of labels. TypeScript automatically narrows the type according to it.

This pattern is very suitable for:

* Request status
* Operation Results
* Message type
* UI status
* Redux action
* API success and failure responses

For example:

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





## 3. JavaScript modules

The “JavaScript modules” here mainly refer to the modern **ES Modules (**). It splits the code into different files through `export` and `import`.

Assume the project structure is as follows:

```text
src/
├─ main.ts
├─ math.ts
└─ user.ts
```

As long as the top layer of the document appears `import` or `export`, TypeScript usually considers it as a module:

```ts
export {};
```

Even if no actual content is exported, this statement can still clearly convey to TypeScript: “This is a module, not a global script.”

***

### 1. Modules provide namespaces

“Namespace” addresses the issue of **name conflicts and code classification** problems.

Assuming that both documents define `format()`:

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

Although they have the same name, they belong to different modules, so there will be no conflicts.

You can change your name when importing:

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

Each file here naturally forms a separate name space.

#### 1.1. The entire import is for the module object.

You can also import the entire module as an object:

```ts
import * as DateUtils from "./date-utils.js";
import * as NumberUtils from "./number-utils.js";

DateUtils.format(new Date());
NumberUtils.format(3.14);
```

`DateUtils` and `NumberUtils` are known as **module namespace objects**.

This looks similar to a static utility class:

```ts
DateUtils.format(...)
```

However, there is no need to create it:

```ts
class DateUtils {
  static format(...) {}
}
```

#### 1.2. Differences from TypeScript `namespace`

TypeScript also has a keyword `namespace`:

```ts
namespace DateUtils {
  export function format(date: Date) {
    return date.toISOString();
  }
}
```

However, in modern modular projects, it is usually preferred to use file-based modules:

```ts
// date-utils.ts
export function format(date: Date) {
  return date.toISOString();
}
```

Because of ES Module:

* It is the JavaScript standard.
* Browsers and Node.js natively support this.
* The build tool can analyze the content.
* It's easier to perform tree shaking.
* Follow the same organization pattern as npm packages.

So, when we talk about “modules providing namespaces,” it doesn’t mean that we must use the `namespace` keyword. Instead, it means that each module naturally has its own isolated name. ****

***

### 2. Modules have private scope

By default, variables, functions, and classes declared within a module are only visible within that module.

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

Here:

```ts
count
validateAmount
```

Not exported, so it is internal to the module.

Other files can only use the exported members:

```ts
import {
  increment,
  getCount,
} from "./counter.js";

increment(2);
console.log(getCount());

// count;          // Error: Not visible
// validateAmount; // Error: Not visible
```

This is the private domain of the module level.

#### 2.1 “Private” does not equal `private`.

It is a concept at two different levels compared to the class’s `private`.

Private members:

```ts
class Counter {
  private count = 0;
}
```

Module private members:

```ts
let count = 0;

export function increment() {
  count++;
}
```

The difference lies in:

* Class `private` protects an object or class of internal members
* The module scope provides protection for the internal implementation of the entire file or module.
* Private module does not require additional keywords
* As long as `export` is not present, other modules cannot be imported directly.

#### 2.2. The specific implementation can be hidden, with only the public interfaces exposed.

```ts
// password.ts

function hashInternal(password: string): string {
  // The internal algorithm
  return `hashed:${password}`;
}

export function createPassword(password: string): string {
  if (password.length < 8) {
    throw new Error("密码至少需要 8 个字符");
  }

  return hashInternal(password);
}
```

The user can only call:

```ts
import { createPassword } from "./password.js";
```

Even if the replacement of `hashInternal()` is achieved at a later date, other documents will normally not need to be modified as long as the use of `createPassword()` remains unchanged.

This is what is referred to as **encapsulation**.

#### 2.3. In browsers, global variables are not automatically contaminated either.

Traditional regular scripts:

```html
<script src="a.js"></script>
<script src="b.js"></script>
```

If both scripts declare variables with the same name at the top level, a conflict may occur.

Module script:

```html
<script type="module" src="./main.js"></script>
```

The top-level declarations within the module do not automatically become properties of `window`.

```js
const message = "hello";

console.log(window.message); // undefined
```

***

### 3. Modules are evaluated once

When a module is loaded for the first time, the top-level code is executed once. Subsequent imports usually reuse the already loaded module instances.

Consider the following module:

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

Both files are imported separately:

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

If `page-a.ts` and `page-b.ts` are in the same module loading environment, they usually access the same `counter` module instance.

```text
counter 模块开始执行
A: 1
B: 2
```

Instead of:

```text
A: 1
B: 1
```

This means that within the module:

```ts
let count = 0;
```

Initialize only once, and it is shared by all importers.

Therefore, it has a behavior similar to a singleton.

***

### 4. Exporting from modules

`export` determines what the module is willing to expose to the outside world.

#### 4.1 Export with Names

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

You can also declare it first and then export it all together:

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

You can also change the name when you export:

```ts
function add(a: number, b: number): number {
  return a + b;
}

export {
  add as sum,
};
```

The user sees `sum`:

```ts
import { sum } from "./math.js";
```

#### 4.2 Default Export

A module can have only one default export:

```ts
// UserService.ts

export default class UserService {
  findUser(id: number): void {
    console.log(id);
  }
}
```

When importing the default value, you can choose the local name by yourself:

```ts
import UserService from "./UserService.js";
```

It could also:

```ts
import Service from "./UserService.js";
```

Because the default import does not rely on the original names.

#### 4.3. How to choose between named exports and default exports?

The advantage of naming exports is the uniformity of names:

```ts
import { createUser } from "./user.js";
```

The editor also makes it easier to autocomplete and batch rename items. Therefore, in application code, many teams prefer to name exports in this way.

Default exports are commonly found in:

* A file mainly exports a component.
* The file structure specified by certain frameworks
* Existing APIs of third-party libraries

Both can coexist:

```ts
export const version = "1.0";

export default function start() {}
```

Usage:

```ts
import start, {
  version,
} from "./app.js";
```

***

### 5. Importing from modules

#### 5.1 Importing Named Members

```ts
import {
  add,
  PI,
} from "./math.js";

console.log(add(1, 2));
console.log(PI);
```

The name must match the export name.

#### 5.2. Renaming during import

```ts
import {
  add as calculateTotal,
} from "./math.js";

calculateTotal(1, 2);
```

#### 5.3 Importing Default Members

```ts
import UserService from "./UserService.js";
```

The default import has no brackets.

#### 5.4. Importing the entire module

```ts
import * as MathUtils from "./math.js";

MathUtils.add(1, 2);
console.log(MathUtils.PI);
```

#### 5.5. Only execute the module; do not import members.

```ts
import "./setup.js";
```

This notation is used for the side effects of modules. For example:

```ts
// setup.ts
console.log("正在初始化应用");
registerGlobalHandlers();
```

In the entry file:

```ts
import "./setup.js";
```

It is important to use side effects imports with caution, as they can make the behavior of the program dependent on the loading order.



## 4. TypeScript in 5 Minutes

Original address: [https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html](https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html)

***

This official tutorial demonstrates the core workings of TypeScript through a simple web greeting program:

> Write `.ts` → Static type checking → Compile to `.js` → Executed by a browser or Node.js.

TypeScript itself isn’t a new runtime environment; ultimately, it still runs on JavaScript. [The official tutorial.](https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html)

### 1. Summary

#### Install and compile

The page uses global installation:

```bash
npm install -g typescript
tsc greeter.ts
```

`tsc` is the TypeScript compiler. It checks `greeter.ts` and then generates a browser capable of performing `greeter.js`.

Local installation is more recommended in actual projects to avoid text conflicts between different items:

```bash
npm init -y
npm install --save-dev typescript
npx tsc --init
npx tsc
```

#### TypeScript can directly accept JavaScript.

Although the original file uses the `.ts` extension, its content is entirely JavaScript.

```ts
function greeter(person) {
  return "Hello, " + person;
}

const user = "Jane User";

document.body.textContent = greeter(user);
```

This demonstrates an important feature of TypeScript: it is a superset of JavaScript. A large portion of JavaScript code can be directly migrated to TypeScript.

#### Type annotations:

Add `: string` to parameter:

```ts
function greeter(person: string) {
  return "Hello, " + person;
}
```

It means that the function requires the caller to enter a string. The following code produces a compilation error:

```ts
greeter([0, 1, 2]);
// number[] cannot be assigned to string.
```

Type annotations can be understood as a “call contract”.

```ts
function add(a: number, b: number): number {
  return a + b;
}
```

* `a: number`: Parameter type
* `b: number`: Parameter type
* `): number`: The type of the return value

However, not every case requires writing the type manually. TypeScript can often infer the type automatically.

```ts
const name = "Alice"; // It is inferred to be a string.
const scores = [90, 85]; // It is inferred to be number[]
```

It was also suggested that there should not be too many redundant comments at the beginning of the school year.[Common types and type inference](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)

#### The interface and structured types

The page defines an interface:

```ts
interface Person {
  firstName: string;
  lastName: string;
}
```

Then, let the function receive an object that conforms to this structure:

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

`user` There is no explicit declaration `implements Person`, but it has two attributes required for interface, so it can be passed on.

This is called a structural type system. In layman’s terms:

> TypeScript cares about how a value “looks” and what it can do, rather than which type it explicitly claims to belong to.

For example, having extra attributes is usually not a problem:

```ts
const employee = {
  firstName: "Jane",
  lastName: "User",
  department: "Engineering",
};

greeter(employee); // Yeah.
```

However, when passing an object literal directly, additional property checks will be performed:

```ts
greeter({
  firstName: "Jane",
  lastName: "User",
  department: "Engineering", // Usually, an error occurs: The attribute is not present in the Person object.
});
```

#### Classes

At the end of the page, a class named `Student` is defined:

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

The `public` before the constructor parameters is an abbreviation:

```ts
constructor(public firstName: string) {}
```

The approximate equivalent is:

```ts
firstName: string;

constructor(firstName: string) {
  this.firstName = firstName;
}
```

`Student` Examples include `firstName` and `lastName` and therefore conform to the structure of `Person`:

```ts
const user = new Student("Jane", "M.", "User");
greeter(user); // Yeah.
```

No inheritance is used here. It demonstrates that “an instance of a class can conform to an interface”.

#### Run in a browser.

The HTML does not introduce `.ts`, but rather the compiled `.js`:

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

Browsers generally do not run TypeScript directly. Therefore, the entire process is as follows:

```text
greeter.ts
    ↓ tsc type-checks and emits JavaScript
greeter.js
    ↓ browser loads the script
page runs the script
```

### 2. Key concepts

#### The type only exists during the compilation phase.

The interfaces and most type annotations will not appear in the final JavaScript code:

```ts
interface User {
  name: string;
}

const user: User = { name: "Alice" };
```

After compilation, only the following remains:

```js
const user = { name: "Alice" };
```

Therefore, TypeScript types cannot automatically validate network data:

```ts
const response = await fetch("/api/user");
const data = await response.json();
```

`data` From rantime, which may not match your desired structure. The real project needs to be self-verified, or use the Zod and other Runtime authentication library.

#### Type errors may not necessarily prevent the generation of JavaScript code.

The tutorial states that even if a type error occurs, `tsc` will still generate JavaScript by default. This is because `noEmitOnError` is, by default, equal to `false`.

The following can be enabled in the project:

```json
{
  "compilerOptions": {
    "noEmitOnError": true
  }
}
```

This way you don't output JavaScript when there's a type error. [The official configuration instructions:](https://www.typescriptlang.org/tsconfig/noEmitOnError.html)

#### It is recommended to enable the strict mode.

When starting out, it's better to enable strict checking. In the long run, this will actually help develop correct habits.

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict` will simultaneously introduce a set of strict type checks to provide stronger assurance of correctness. [The official strict description is as follows:](https://www.typescriptlang.org/tsconfig/strict.html)

For example:

```ts
function greeter(person) {
  // strict mode, person's hidden for any will be misreported
}
```

#### Try to avoid `any`

`any` is equivalent to telling TypeScript: "Don't check this value":

```ts
let value: any = "hello";

value.notExistingMethod(); // The compiler does not prevent this, but the runtime may crash.
```

When the type is uncertain, prioritize using `unknown`:

```ts
function printValue(value: unknown) {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  }
}
```

`unknown` will ask you to check the type first. This process is called type narrowing.

#### Simple choices for `interface` and `type`

The object structure can generally be implemented using any of the following methods:

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

This can be noted at the beginning of the school cycle:

* Describe the common structure of objects and classes: prioritize using `interface`.
* Combined types, tuples, or complex combinations: Use `type`.

For example:

```ts
type ID = string | number;
type Point = [number, number];
```

`interface` may state that the merger is combined, while `type` may express a broader combination of types. [Official comparison](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#differences-between-type-aliases-and-interfaces)

### 3. A complete example for modern projects

`greeter.ts`:

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

`index.html`:

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

The recommended value for `tsconfig.json` is:

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

Note: After setting `outDir: "dist"`, the HTML should be changed to:

```html
<script src="dist/greeter.js" defer></script>
```

### 4. Recommended order of learning

After studying this page, you can proceed to study the following topics in order:

1. Basic types and type inference
2. Array, object, function types
3. Optional properties and combined types
4. I'm sorry, type Narrowing
5. `interface` and `type`
6. Generic types
7. Module: `import` / `export`
8. `tsconfig.json`
9. Asynchronous functions and `Promise`
10. DOM type or Node.js type

The core understanding that really needs to be established on this page is:

> TypeScript utilizes static typing to detect some errors before the code is executed. It also provides the editor with features such as completion, navigation, and refactoring. After compilation, the program remains JavaScript.



## 5. The TypeScript Handbook

Original address: [https://www.typescriptlang.org/docs/handbook/intro.html](https://www.typescriptlang.org/docs/handbook/intro.html)

***

This is an “instruction” from the TypeScript Handbook. The focus is not on syntax, but rather on answering three questions:

1. Why does TypeScript exist?
2. How should one read the Handbook?
3. What doesn’t the Handbook teach?

[Introduction to TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

### 1. Why TypeScript exists

JavaScript was originally used to add simple interactions to web pages. Over time, its applications expanded to include:

* Large front-end applications
* Node.js backend
* Desktop applications
* Mobile applications
* Cross-platform tools

As the project grows, the relationships between the code become more complex. However, native JavaScript doesn’t make it easy to express these relationships directly.

For example:

```js
function calculatePrice(price, quantity) {
  return price * quantity;
}

calculatePrice("100", 2);
```

Should the caller pass in a number or a string? It’s not clear just by looking at the function name. In JavaScript, certain issues can only be identified after the code has been executed.

TypeScript can explicitly express constraints:

```ts
function calculatePrice(
  price: number,
  quantity: number,
): number {
  return price * quantity;
}

calculatePrice("100", 2);
// Error: The string cannot be passed to the number.
```

Therefore, the core goal of TypeScript is:

> Perform a state type checking of JavaScript code before it runs.

"Silent" means "type check" before running. [The official description:](https://www.typescriptlang.org/docs/handbook/intro.html#about-this-handbook) indicates whether the value is used in a manner that is not expected.

### 2. Errors TypeScript helps catch

The document states that many common errors in the program are related to type errors. For example:

#### Spelling error.

```ts
const user = {
  name: "Alice",
};

console.log(user.naem);
// Error: The "naem" does not exist. It seems you might have intended to write "name".
```

#### Misunderstanding of third-party APIs

```ts
const names = ["Alice", "Bob"];

names.push(100);
// Error: number cannot be added to string[]
```

#### Misunderstanding of the return value

```ts
function findUser(): User | undefined {
  // ...
}

const user = findUser();
console.log(user.name);
// Error: The `user` variable might be `undefined`.
```

#### The wrong parameters were used.

```ts
function setAge(age: number) {}

setAge("十八");
// Error: The string cannot be passed to the number.
```

These errors may not cause the program to crash immediately, but they often indicate that the programmer’s assumptions do not match the actual code.

### 3. Static checks and runtime checks

This is the most important knowledge extension behind the introduction.

TypeScript checks the source code. Types are usually removed during compilation:

```ts
function greet(name: string): string {
  return `Hello, ${name}`;
}
```

The compilation was roughly:

```js
function greet(name) {
  return `Hello, ${name}`;
}
```

Therefore, TypeScript cannot guarantee that the external data is correct:

```ts
interface User {
  id: number;
  name: string;
}

const response = await fetch("/api/user");
const user = (await response.json()) as User;
```

Here's `as User` simply telling the compiler to "take it as User," which doesn't really verify the data returned by the server.

If the server returns:

```json
{
  "id": "not-a-number",
  "name": null
}
```

TypeScript at runtime won't automatically stop it.

Therefore, it is necessary to distinguish between:

| **Check the method.** | **Occurrence Time** | **Examples** |
| --------------- | -------- | ----------- |
| Static checking for TypeScript | Before running | Parameter type, attribute spelling |
| Runtime verification | When the program runs | API response, user input |
| Automated testing | During testing | Is business logic correct? |

Simple runtime validation can be implemented like this:

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

### 4. The structure of the Handbook

The official documentation is divided into two main categories.

#### Handbook

The Handbook is a continuous learning material. It is recommended to read it from top to bottom, following the table of contents on the left.

After completing this task, the reader should be able to:

* Read the common TypeScript syntax.
* Understand common TypeScript programming patterns.
* Explain the functions of important compiler options.
* Predict the behavior of most types of systems.

It is a comprehensive guide, but it is not a complete linguistic norm.[Structure description of Handbook](https://www.typescriptlang.org/docs/handbook/intro.html#how-is-this-handbook-structured)

#### Reference

Reference is a reference material for the topic. For example:

* Utility Types
* Type inference
* Type compatibility
* Enumerate
* Decorator
* Declare merge

It does not emphasize continuity and is suitable for access once the concept name is known.

It can be understood as follows:

* Handbook: Like a textbook
* Reference: Similar to a dictionary
* TSConfig Reference: A guide to configuration instructions.
* Language Specification: Formal definitions for language implementers

When you are first learning, don’t try to read the Reference from beginning to end.

### 5. What doesn’t the Handbook teach?

#### Unsystemic Professor JavaScript Foundation

By default, you have a certain understanding of the following JavaScript concepts:

* Variables and their scopes
* Conditional statements and loops
* The function
* Objects and arrays
* Classes
* Closure
* Promises and Asynchronous Programming
* ES module

For example:

```ts
const double = (value: number) => value * 2;
```

The TypeScript Handbook will explain `value: number`, but it may not explain arrow functions in detail.

If TypeScript is your first language, it is recommended to learn the basics of JavaScript first. [Official beginner's recommendations](https://www.typescriptlang.org/docs/handbook/intro.html#about-this-handbook)

#### It's not a whole language code.

The Handbook aims to be easy to understand. It does not cover all possible boundary situations and formal rules.

For example, when you first start learning, you only need to know that the structure is compatible with certain types:

```ts
interface Named {
  name: string;
}

const employee = {
  name: "Alice",
  department: "Engineering",
};

const person: Named = employee; // Yeah.
```

As for all the compatibility rules of the structural type system, refer to the Reference section when necessary.

#### I'm not responsible for explaining all the tool chains.

The Handbook does not systematically teach how TypeScript can be integrated with these tools:

* React, Vue, Angular, Svelte
* Vite, webpack, Rollup
* Babel
* npm, pnpm, Yarn
* Testing framework
* Single repository tools

These are ecological and engineering tools, not part of the TypeScript type system itself.

### 6. Where to start based on your background

The official provided several entry points:

* No programming background required: Start by learning JavaScript.
* Know JavaScript: Read TypeScript for JavaScript Programmers
* Familiar with Java/C#: Reading TypeScript for Java/C# Programmers
* Familiarize yourself with functional programming: Read the corresponding introductions.
* The basic positioning has been understood: proceed directly to The Basics.

If you are a beginner in TypeScript and JavaScript, I recommend learning in a two-step approach:

```text
JavaScript fundamentals
    ├─ Variables, functions, objects, and arrays
    ├─ Scope and closures
    ├─ Classes and prototypes
    ├─ Promise / async
    └─ import / export
              ↓
TypeScript type system
    ├─ Basic types
    ├─ Function and object types
    ├─ Union types and type narrowing
    ├─ interface / type
    ├─ Generics
    └─ Modules and compiler configuration
```

Don’t wait until you’ve thoroughly learned JavaScript to start working with TypeScript. You can learn one JavaScript concept, and then immediately learn the TypeScript representation of that concept.

### 7. Understanding types

Beginners often misunderstand types as simply assigning labels to variables:

```ts
let age: number = 18;
```

A more valuable understanding is that types express the relationships between codes.

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

The following expresses three relationships:

* Type type to match `Product.id`
* Return `Product` in case of success.
* If the search fails, return `undefined`.

The caller must handle failure scenarios accordingly:

```ts
const product = findProduct("p-001");

if (product) {
  console.log(product.price);
}
```

The true value of a type system isn’t to make the code seem rigid, but rather to make the assumptions between functions, data, and modules clear.

### 8. Recommended order of reading for the Handbook

For beginners, it is recommended to follow the following order:

1. [The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html)
2. Everyday Types
3. Narrowing
4. More on Functions
5. Object Types
6. Generics
7. Classes
8. Modules

The first pass can be skipped for now:

* Conditional Types
* Mapped Types
* Template Literal Types
* Declaration Merging
* Decorators
* Prepared by myself `.d.ts`

Finally, summarize this introduction in one sentence:

> TypeScript is a static type checker for JavaScript. The Handbook teaches you how to understand and use its type system, but it does not replace the basic JavaScript courses, the complete language specifications, or tutorials on front-end engineering tools.



## 6. The Basics

Original address: [https://www.typescriptlang.org/docs/handbook/2/basic-types.html](https://www.typescriptlang.org/docs/handbook/2/basic-types.html)

***

This [TypeScript Handbook: The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) does not list the basic types like `string`, `number`, etc. Instead, it explains the core way of working in TypeScript: **uses static type analysis to detect errors before JavaScript runs.**

### 1. Core concepts

#### 1.1. TypeScript is a static type checker for JavaScript.

JavaScript usually requires the code to be executed before certain errors can be detected:

```js
const message = "Hello World";

message(); // Runtime error: message is not a function.
```

TypeScript can find it before running:

```ts
const message = "Hello World";

message();
// Compilation error: This expression is not callable.
```

It can be understood as follows:

* JavaScript: It’s only at runtime that we can determine what the value can do.
* TypeScript: What can predicted values do when it comes to writing and compiling code.
* TypeScript ultimately generates JavaScript, which is executed by browsers or Node.js.

The type actually describes what capabilities a value has. For example:

* You can call `toLowerCase()` from `string`.
* The function can be called.
* You can call `toDateString()` from `Date`.
* Regular objects can only access properties that exist within their own type.

***

#### 1.2. TypeScript can also detect issues that may not cause immediate errors.

The following JavaScript code can run, but it is likely to contain programming errors:

```js
const user = {
  name: "Daniel",
  age: 26,
};

console.log(user.location); // undefined
```

TypeScript will indicate in advance:

```ts
user.location;
// Property 'location' does not exist
```

It can also detect:

##### Spelling error.

```ts
const announcement = "Hello";

announcement.toLocalLowerCase(); // The method name was written incorrectly.
announcement.toLocaleLowerCase(); // Correct.
```

##### Forget to call the function.

```ts
Math.random < 0.5;   // Error: The comparison is made between the function itself.
Math.random() < 0.5; // Proper: Comparing the return values of functions
```

##### It's impossible to establish such a logic.

```ts
const value = Math.random() < 0.5 ? "a" : "b";

if (value !== "a") {
  // The value here can only be "b".
} else if (value === "b") {
  // It is impossible to reach there.
}
```

This demonstrates an important capability of TypeScript: it not only checks the type names, but also analyzes the possible values of variables based on the program flow.

***

#### 1.3. Types can also enhance the functionality of the editor.

Type information is used not only for error reporting, but also to support other purposes.

* Auto-completion
* Parameter Hints
* Jump to the definition.
* Find all references.
* Automatic refactoring
* Quick fix
* Hover the mouse to view the type.

Therefore, the value of TypeScript lies not only in “reducing errors,” but also in “making code easier to read, modify, and refactor.”

***

#### 1.4. `tsc` Compiler

`tsc` is an official TypeScript compiler. The page shows the way in which it is installed globally; it is more recommended in the actual project to be installed as a project development dependency:

```bash
npm init -y
npm install --save-dev typescript
npx tsc --init
```

Create `hello.ts`:

```ts
console.log("Hello world!");
```

Compilation:

```bash
npx tsc hello.ts
```

Usually generates:

```text
hello.ts
hello.js
```

The execution is after the generation of JavaScript:

```bash
node hello.js
```

The complete process is as follows:

```text
hello.ts
   ↓ TypeScript type-checks and emits JavaScript
hello.js
   ↓ JavaScript runtime executes the script
Program output
```

***

#### 1.5. By default, JavaScript can also be generated even if there are type errors.

For example:

```ts
function greet(person: string, date: Date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}

greet("Alice"); // Missing second parameter
```

`tsc` reports errors, but it is possible to export JavaScript by default. This is to facilitate the gradual migration of the old JavaScript project to TypeScript.

New projects should generally prohibit such behavior:

```json
{
  "compilerOptions": {
    "noEmitOnError": true
  }
}
```

Or:

```bash
npx tsc --noEmitOnError
```

If the project uses other tools for generating JavaScript, it is possible to perform only the verification step.

```bash
npx tsc --noEmit
```

***

#### 1.6. Explicit type annotations

The type annotation is written after the variable or parameter name:

```ts
function greet(person: string, date: Date): void {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}
```

The meanings are as follows:

* `person: string`: The parameter must be a string.
* `date: Date`: The parameter must be an object of type `Date`.
* `: void`: The function does not return any meaningful value.

Note `Date()` and `new Date()` are different:

```ts
Date();     // returns String
new Date(); // Return the Date object.
```

So:

```ts
greet("Alice", Date());     // Error
greet("Alice", new Date()); // Correct.
```

***

#### 1.7. Type inference

Not all places require manual type:

```ts
let message = "hello";
// TypeScript infers that message is a string.
```

The following writing is not usually necessary:

```ts
let message: string = "hello";
```

A practical principle is:

* The function parameters usually specify the types.
* The return value of public functions can be explicitly annotated.
* Normal local variables allow TypeScript to extrapolate as much as possible.
* When the extrapolation results are not accurate, the type is supplemented.

For example:

```ts
function add(a: number, b: number): number {
  return a + b;
}

const result = add(10, 20); // It is automatically inferred to be a number.
```

***

#### 1.8. The types will be erased after compilation.

The following TypeScript:

```ts
function greet(person: string): string {
  return `Hello ${person}`;
}
```

After compiling to JavaScript, it would look something like this:

```js
function greet(person) {
  return `Hello ${person}`;
}
```

The information of the type `string` disappears. The official document emphasizes that: **type labels do not change the behaviour of the program runtime.**

This leads to a very important conclusion:

```ts
type User = {
  name: string;
};

const data = JSON.parse(input) as User;
```

Write as `as User` does not check if `name` really exists in the input. It simply tells the compiler "please consider it `User`."

For external data such as APIs, JSON, and forms, runtime validation is still required:

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

#### 1.9. Downleveling

TypeScript can convert the newer JavaScript syntax into older syntax.

For example:

```ts
const message = `Hello ${name}`;
```

For use in older environments, it may be converted to:

```js
var message = "Hello ".concat(name);
```

It is determined by `target` which version of JavaScript to use:

```json
{
  "compilerOptions": {
    "target": "ES2022"
  }
}
```

It is necessary to distinguish between two concepts:

* `target`: What version of JavaScript should be generated?
* `lib`: Which platform APIs are allowed during type checking.

For example, whether to use `document` depends not only on `target`, but also on whether a DOM type library is included.

***

#### 1.10. Strict Mode

It is recommended to enable the new feature:

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict` is the master switch for a set of strict validation options. Two of these options are highlighted in the page.

##### `noImplicitAny`

If TypeScript cannot infer the parameter type, it may be reduced to `any` in loose mode.

```ts
function printName(name) {
  console.log(name.toUpperCase());
}
```

After enabling strict checking, it is necessary to specify the type clearly:

```ts
function printName(name: string): void {
  console.log(name.toUpperCase());
}
```

##### `strictNullChecks`

Once enabled, `null` and `undefined` can no longer be assigned to other types.

```ts
function findUser(): string | undefined {
  return Math.random() > 0.5 ? "Alice" : undefined;
}

const user = findUser();
console.log(user.toUpperCase()); // Error: The `user` variable might be `undefined`.
```

The type range must be narrowed first:

```ts
if (user !== undefined) {
  console.log(user.toUpperCase());
}
```

Or use it in scenarios where a default value is appropriate:

```ts
console.log((user ?? "Guest").toUpperCase());
```

### 2. Further reading

#### 2.1. The difference between `any` and `unknown`

`any` Basically equals closed-type check:

```ts
let value: any = "hello";

value.notExist();
value();
value.foo.bar;
```

This may not stop the compilers.

`unknown` means "type not known for the time being", which must be checked before being used:

```ts
let value: unknown = "hello";

if (typeof value === "string") {
  console.log(value.toUpperCase());
}
```

When processing external data, prioritize using `unknown` and try to avoid using `any`.

***

#### 2.2. TypeScript uses a structural type system

TypeScript primarily cares about what an object “looks like”, rather than what it is called.

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

greet(employee); // Valid, because the `employee` field has at least the `name: string` attribute.
```

This mechanism is called structural typing. It can also be simply understood as a “static version of the duck type”.

***

#### 2.3. Narrowing of types

TypeScript will reduce the broad types into more specific ones based on conditional judgments:

```ts
function format(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // This is a string.
  }

  return value.toFixed(2); // This is the number.
}
```

Common methods of reduction include:

* `typeof`
* `instanceof`
* `in`
* Clear.
* Literal comparisons
* Custom type guards

This is one of the abilities that is most worth mastering after learning the basics.

***

#### 2.4. TypeScript cannot guarantee that programs are absolutely safe.

TypeScript is good at detecting:

* Parameter type does not match
* The property does not exist.
* Could be empty.
* Spelling error.
* Some logics that are impossible to establish

However, it generally cannot be discovered independently:

* The API returned data in an incorrect format.
* User input is invalid
* The database content did not meet expectations.
* Network error
* Business rule error.
* Runtime issues such as array access out of bounds

So, the correct understanding is:

> TypeScript improves the static reliability of programs, but it cannot replace runtime validation, testing, and error handling.





## 7. Everyday Types

Original address: [https://www.typescriptlang.org/docs/handbook/2/everyday-types.html](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)

***

This [TypeScript Handbook: Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) introduces the most commonly used types in development. It serves as the foundation for further learning about type narrowing, functions, and generics.

The core idea is:

> TypeScript uses primitive types to describe data, and then combines them using arrays, objects, union types, literal types, etc., to create complex types.

### 1. Basic types

#### 1. `string`, `number`, `boolean`

```ts
const username: string = "Alice";
const age: number = 20;
const active: boolean = true;
```

JavaScript does not distinguish between integers and floating-point numbers; it uses `number` uniformly.

```ts
const count: number = 10;
const price: number = 19.99;
```

Type name should use lowercase:

```ts
let name: string;   // Recommendations
let age: number;
let active: boolean;
```

Do not use packing object type:

```ts
let name: String;   // Not recommended
let age: Number;
let active: Boolean;
```

`string` means a normal string value, while `String` means a string package object for JavaScript. The daily development is almost always in the lowercase version.

***

#### 2. Arrays

There are two equivalents:

```ts
const scores: number[] = [90, 85, 100];
const names: Array<string> = ["Alice", "Bob"];
```

It’s usually more readable to use `T[]` for simple types.

```ts
string[]
number[]
User[]
```

The complex type sometimes uses a generics format that is clearer:

```ts
Array<string | number>
```

Note:

```ts
number[] // An array of numbers of any length.
[number] // Only one digit of a widget.
```

Knowledge extension: If an array should not be modified, a read-only array can be used.

```ts
const names: readonly string[] = ["Alice", "Bob"];

names.push("Eve"); // Error
```

***

### 2, `any`

`any` Closes the type of check for the value:

```ts
let value: any = { name: "Alice" };

value.foo.bar();
value();
value = 100;

const age: number = value;
```

The code above generally does not produce any compilation errors, but it may crash during runtime.

It is therefore recommended that:

* Enable `strict` or `noImplicitAny`.
* When the type is unknown, it is preferred to use `unknown`.
* `any` is used on an ad hoc basis only when old items are relocated or third-party data are processed that are not really described.

#### `any` and `unknown`

```ts
let input: unknown = "hello";

input.toUpperCase(); // Error: It is not known what the input is yet.

if (typeof input === "string") {
  input.toUpperCase(); // Correct.
}
```

The difference can be simply remembered as:

| **Type** | **Meaning** |
| --------- | ------------- |
| `any`     | Do not check. I will be responsible for it myself.     |
| `unknown` | I don’t know for now. It’s necessary to check it before using it. |

***

### 3. Type annotation and type inference

Type label after variable name:

```ts
let username: string = "Alice";
```

But if TypeScript can deduce, there is no need to repeat:

```ts
let username = "Alice"; // It is inferred to be a string.
let age = 20;           // It is inferred to be a number.
let active = true;      // It is inferred to be a boolean value.
```

Recommended principles:

```ts
// Local variables: Prefer to infer them.
const price = 99;

// Function parameters: Usually explicitly labeled.
function double(value: number) {
  return value * 2;
}

// Public function return value: Can be explicitly annotated.
function getUsername(): string {
  return "Alice";
}
```

Type inference does not mean that the type will always remain fixed at the initial value:

```ts
let status = "loading";
// The `status` is inferred to be a string, rather than the literal "loading".

status = "success"; // Legal
```

***

### 4. Function Types

#### 1. Parameter types

```ts
function greet(name: string) {
  console.log(name.toUpperCase());
}

greet("Alice"); // Correct.
greet(42);      // Error
```

Even if the parameters have no type annotations, TypeScript will still check the number of parameters.

```ts
function add(a, b) {
  return a + b;
}

add(1); // Missing a parameter
```

However, in strict mode, `a` and `b` will generate an implicit `any` error. Therefore, it should be written as:

```ts
function add(a: number, b: number): number {
  return a + b;
}
```

#### 2. Return value type

```ts
function getAge(): number {
  return 20;
}
```

The return value can usually be inferred automatically as well:

```ts
function getAge() {
  return 20; // It is inferred that the returned value is a number.
}
```

The advantage of explicitly annotating the return value is that it prevents the function implementation from being accidentally modified.

```ts
function getAge(): number {
  return "20"; // Right away, report the mistake.
}
```

#### 3. Asynchronous functions

The return type of the `async` function is `Promise<T>`:

```ts
async function getUsername(): Promise<string> {
  return "Alice";
}
```

Note:

```ts
async function getUsername(): string {
  return "Alice";
}
// Error: The async function returns a Promise.
```

#### 4. Context type inference

```ts
const names = ["Alice", "Bob", "Eve"];

names.forEach((name) => {
  console.log(name.toUpperCase());
});
```

Although no type annotation was added to `name`, TypeScript infers that the callback parameter is `string`, based on the fact that `names` is equal to `string[]`.

This method of inferring the type based on the location of the code is called context-based type inference.

***

### 5. Object types

The structure of the object can be described directly:

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

TypeScript uses a structural type system: it only cares whether an object has the required properties, rather than how it was created.

```ts
const employee = {
  name: "Bob",
  age: 30,
  department: "Development",
};

printUser(employee); // Legal
```

`employee` More than one `department` attribute does not matter because it already has `name` and `age`.

#### Optional properties

Add `?` after the property name:

```ts
type User = {
  name: string;
  nickname?: string;
};
```

Both of the following objects are valid:

```ts
const alice: User = {
  name: "Alice",
};

const bob: User = {
  name: "Bob",
  nickname: "Bobby",
};
```

When reading optional properties, it could be `undefined`:

```ts
function printNickname(user: User) {
  user.nickname.toUpperCase();
  // Error: nickname may be undefined.
}
```

Secure handling method:

```ts
function printNickname(user: User) {
  if (user.nickname !== undefined) {
    console.log(user.nickname.toUpperCase());
  }
}
```

You can either use the optional chain and default values:

```ts
console.log(user.nickname?.toUpperCase());
console.log(user.nickname?.toUpperCase() ?? "NO NICKNAME");
```

It is necessary to distinguish between:

```ts
nickname?: string;
```

It indicates that the attribute may not exist.

```ts
nickname: string | undefined;
```

It indicates that the attribute must exist, but the value can be `undefined`.

When `exactOptionalPropertyTypes` is enabled, this distinction becomes even more stringent.

***

### 6. Union types

The union type indicates that a value can belong to any of multiple types:

```ts
type ID = string | number;

function printId(id: ID) {
  console.log(id);
}

printId(100);
printId("USER-100");
```

#### Only the shared ability can be used directly.

```ts
function printId(id: string | number) {
  id.toUpperCase();
  // Error: The number does not have the toUpperCase method.
}
```

It is necessary to perform type narrowing first:

```ts
function printId(id: string | number) {
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id.toFixed(0));
  }
}
```

For arrays, you can use `Array.isArray()`:

```ts
function welcome(value: string | string[]) {
  if (Array.isArray(value)) {
    console.log(value.join(", "));
  } else {
    console.log(value.toUpperCase());
  }
}
```

If all members in the union type support a certain operation, you can use it directly:

```ts
function firstThree(value: string | number[]) {
  return value.slice(0, 3);
}
```

Both `string` and arrays contain `slice()`, so there is no need to reduce them first.

***

### 7. Type aliases `type`

Type aliases can give any type a name:

```ts
type Point = {
  x: number;
  y: number;
};

type ID = string | number;

type Status = "loading" | "success" | "error";
```

Using type aliases can reduce redundancy:

```ts
function printPoint(point: Point) {
  console.log(point.x, point.y);
}
```

However, aliases do not create a completely new runtime type:

```ts
type SanitizedString = string;

let value: SanitizedString = "ordinary string"; // Still legal.
```

`SanitizedString` is essentially just another name for `string`.

***

### 8. Interface `interface`

The interface is specifically used to describe the object structure:

```ts
interface User {
  name: string;
  age: number;
}

function printUser(user: User) {
  console.log(user.name);
}
```

#### The difference between `type` and `interface`

Both descriptions describe ordinary objects very similarly:

```ts
type UserType = {
  name: string;
};

interface UserInterface {
  name: string;
}
```

The main difference is as follows:

| **Capability** | **`interface`** | **`type`** |
| --------------- | --------------- | ---------- |
| Describe the object | Support | Support |
| Describe the combined type. | Not supported | Support |
| Describe the alias for basic types. | Not supported | Support |
| Use `extends` to inherit | Support              | Use intersection type to achieve   |
| Merge of declarations with the same name | Support | Not supported |

Interface inheritance:

```ts
interface Animal {
  name: string;
}

interface Bear extends Animal {
  honey: boolean;
}
```

Type intersection:

```ts
type Animal = {
  name: string;
};

type Bear = Animal & {
  honey: boolean;
};
```

The interface can be declared for merging:

```ts
interface WindowConfig {
  title: string;
}

interface WindowConfig {
  width: number;
}

// Finally, it has both title and width properties.
```

Practical selection principles:

* Ordinary, scalable object model: Prioritize `interface`.
* For combined types such as unions, tuples, mappings, etc.: Use `type`.
* The team already has a unified style: they follow the project's agreements.
* Do not dwell on them for the sake of choice.

***

### 9. Type assertion

Type assertion means: “I know the type of this value better than the compiler.”

```ts
const canvas = document.getElementById(
  "main-canvas",
) as HTMLCanvasElement;
```

There is also another way of writing it:

```ts
const canvas =
  <HTMLCanvasElement>document.getElementById("main-canvas");
```

However, the angle-bracket notation cannot be used normally in `.tsx`. Therefore, it is generally recommended to use `as`.

#### Assert that it is not a type conversion.

```ts
const value = "123" as unknown as number;
```

Runtime `value` remains a string and does not become a number.

The actual conversion of data should be done using:

```ts
const value = Number("123");
```

In other words:

* `as number`: Affects only the compiler.
* `Number(value)`: The actual values that affect runtime data.

Avoid abusing double assertions just to eliminate errors:

```ts
value as unknown as User;
```

This writing usually means that there is a problem with the type design or runtime verification.

***

### 10. Literal types

Literal types represent a specific value:

```ts
let direction: "left";

direction = "left";  // Correct.
direction = "right"; // Error
```

It doesn’t make much sense to use it alone, but it’s very useful when combined with other types:

```ts
type Direction = "left" | "right" | "center";

function align(direction: Direction) {
  // ...
}

align("left");
align("center");
align("top"); // Error
```

You can also use numerical literals:

```ts
function compare(a: string, b: string): -1 | 0 | 1 {
  return a === b ? 0 : a > b ? 1 : -1;
}
```

Literal union types are often lighter in terms of overhead compared to enums:

```ts
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type Theme = "light" | "dark";
type RequestState = "idle" | "loading" | "success" | "error";
```

***

### 11. Literal value inference and `as const`

Note the following objects:

```ts
const request = {
  url: "/users",
  method: "GET",
};
```

Although the variable uses `const`, the object properties can still be modified:

```ts
request.method = "DELETE";
```

So, TypeScript infers that `request.method` is `string`, rather than the literal value `"GET"`.

If the function only accepts fixed methods:

```ts
function send(method: "GET" | "POST") {}

send(request.method); // Possible error: request.method is a string.
```

Available at `as const`:

```ts
const request = {
  url: "/users",
  method: "GET",
} as const;
```

At this point, it can be roughly inferred that:

```ts
{
  readonly url: "/users";
  readonly method: "GET";
}
```

Note:

> `const` prevents the variable from being reassigned; `as const` makes the object properties read-only at the type level.

#### Extension: `satisfies`

If you want to check whether an object conforms to a certain structure while still maintaining precise inference, you can use `satisfies`.

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

`satisfies` focuses more on “checking” than `as RequestConfig` and does not simply cover the original inferences with the target type.

***

### 12. `null` and `undefined`

They all indicate that there is no value available, but their meanings are usually different:

* `undefined`: Not provided yet; the attribute does not exist.
* `null`: Explicitly indicates that there is no value.

After enabling `strictNullChecks`, it is necessary to handle it explicitly:

```ts
function printName(name: string | null) {
  if (name === null) {
    console.log("No name");
  } else {
    console.log(name.toUpperCase());
  }
}
```

You can also use null coalescing:

```ts
function displayName(name: string | null | undefined) {
  return name ?? "Anonymous";
}
```

`??` is not exactly the same as `||`:

```ts
0 || 10; // 10
0 ?? 10; // 0

"" || "default"; // "default"
"" ?? "default"; // ""
```

`??` Only treats `null` and `undefined` as missing values.

#### Non-empty assertion `!`

```ts
const element = document.getElementById("app");

element!.textContent = "Hello";
```

`!` tells TypeScript: “It definitely isn’t `null` or `undefined`.”

It does not add runtime checks. If the element does not exist, the program will still crash. A safer way to write it would be:

```ts
const element = document.getElementById("app");

if (element !== null) {
  element.textContent = "Hello";
}
```

Use `!` only when it can be strictly guaranteed to be non-empty by the program logic.

***

### 13. Enums

```ts
enum Direction {
  Up,
  Down,
  Left,
  Right,
}
```

Unlike most TypeScript types, `enum` is typically generated as runtime code. The official documentation advises that you should be aware of its existence, but don’t rush to use it right away.

In many scenarios, literal combinations can be used instead:

```ts
type Direction = "up" | "down" | "left" | "right";
```

You can also use constant objects:

```ts
const Direction = {
  Up: "up",
  Down: "down",
  Left: "left",
  Right: "right",
} as const;

type Direction = typeof Direction[keyof typeof Direction];
```

Suggestions for beginners:

* Only limit the value of the string: use literal combination.
* It is necessary to provide a runtime object or to follow existing conventions for the project. Consider using `enum` for that purpose.

***

### 14. `bigint` and `symbol`

#### `bigint`

Used to represent large integers that exceed the normal `number` safe integer range:

```ts
const amount1: bigint = BigInt(100);
const amount2: bigint = 100n;
```

Can't mix `number` and `bigint` directly:

```ts
1n + 1;  // Error
1n + 1n; // Correct.
```

When using `bigint` literal, the compiler usually needs to support the ES2020 or higher version.

#### `symbol`

Each `Symbol()` is a unique value:

```ts
const first = Symbol("name");
const second = Symbol("name");

console.log(first === second); // false
```

Even if the descriptive text is the same, they are not the same value. `symbol` is often used to create object keys that do not cause naming conflicts.

***

### 15. Comprehensive Example

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

This example also uses:

* Object type
* `interface`
* Combined types
* Literal types
* Optional properties
* Optional chain `?.`
* Null values are merged together. `??`
* Return value type
* `satisfies`

### 16. Quick Reference Table

| **Write** | **Meaning** |
| ------------------ | ---------- |
| `string`           | String        |
| `number`           | Numbers         |
| `boolean`          | Boolean values        |
| `string[]`         | Array of strings      |
| `Array<string>`    | Array of strings      |
| `name?: string`    | Optional properties       |
| `string \| number` | Combined types       |
| `"GET" \| "POST"`  | Literal combination      |
| `type A = ...`     | I'm sorry, type alas.       |
| `interface A {}`   | Object interface       |
| `value as T`       | Type assertion       |
| `value!`           | Non-empty assertions.       |
| `as const`         | Keep the literals as they are, and set them to read-only. |
| `unknown`          | Unknown type. Check before use. |
| `any`              | Disable type checking.     |

The three things that are most worth remembering are:

1. **Priority is given to type inference, without having to hand-write the type for each variable.**
2. **unit type only directly uses the capabilities shared by all members, and other operations need to be reduced.**
3. **type assessment and non-empty assertion that rantime checks will not be performed and cannot be considered data conversion or security validation.**

The next chapter is [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html). It will explain systematically how to reduce the combined type through `typeof`, checking for null values, `in`, `instanceof`, and flow analysis.
