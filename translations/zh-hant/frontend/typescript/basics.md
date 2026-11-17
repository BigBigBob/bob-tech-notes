---
translation_id: typescript-basics
description: "TypeScript 的型別推斷、結構型別系統、模組、編譯與常用型別。"
---

# TypeScript 基礎知識



官方文件地址：[~https://www.typescriptlang.org/zh/docs/~](https://www.typescriptlang.org/zh/docs/)



## 一、為 JavaScript 程式設計師準備的 TypeScript

原文地址：[https://www.typescriptlang.org/zh/docs/handbook/typescript-in-5-minutes.html](https://www.typescriptlang.org/zh/docs/handbook/typescript-in-5-minutes.html)

內容總結及知識拓展。

***

這篇文件的核心是：**TypeScript = JavaScript + 靜態型別系統**。它不會取代 JavaScript，而是在程式碼執行前檢查型別錯誤，併為編輯器提供更可靠的補全、跳轉與重構能力。[TypeScript 官方文件](https://www.typescriptlang.org/zh/docs/handbook/typescript-in-5-minutes.html)

### 1、頁面內容總結

#### 1.1. 型別推斷

TypeScript 經常能根據賦值自動判斷型別，不需要處處手寫型別：

```ts
let message = "Hello";
// TypeScript 推斷 message 為 string

message = 123;
// 錯誤：number 不能賦給 string
```

推薦原則：**能夠清晰推斷時，讓 TypeScript 自己推斷。**

```ts
const count = 10; // 不必寫 const count: number = 10
```

函式引數通常需要標註，因為 TypeScript 不知道呼叫者將傳入什麼：

```ts
function double(value: number) {
  return value * 2;
}
```

返回值 `number` 可以自動推斷。

***

#### 1.2. 使用介面描述物件

`interface` 用於描述物件應該具有什麼結構：

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

如果缺少屬性、屬性型別錯誤，或者直接寫入未知屬性，TypeScript 會提示：

```ts
const user: User = {
  name: "小明",
  id: "1", // 錯誤：應為 number
};
```

介面也能用於函式引數和返回值：

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

類只要具有介面要求的結構，也可以被視為該介面型別：

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

#### 1.3. 常見特殊型別

除了 JavaScript 中的 `string`、`number`、`boolean` 等型別，TypeScript 還提供：

| **型別**               | **含義**       |
| -------------------- | ------------ |
| `any`                | 放棄型別檢查，儘量少用  |
| `unknown`            | 型別未知，檢查後才能使用 |
| `void`               | 函式沒有有意義的返回值  |
| `never`              | 某個值不可能出現     |
| `null` / `undefined` | 空值或未定義       |

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
  // console.log(value.toUpperCase()); // 錯誤

  if (typeof value === "string") {
    console.log(value.toUpperCase()); // 安全
  }
}
```

***

#### 1.4. 聯合型別

聯合型別用 `|` 表示“可能是其中一種型別”：

```ts
let id: string | number;

id = 100;
id = "A100";
```

聯合型別也可以限制合法值：

```ts
type Status = "loading" | "success" | "error";

let status: Status = "loading";
// status = "finished"; // 錯誤
```

這稱為**字串字面量聯合型別**，比隨意使用 `string` 更嚴格。

***

#### 1.5. 型別縮小

如果一個值具有聯合型別，使用前經常需要確定它當前是哪一種型別：

```ts
function formatId(id: string | number): string {
  if (typeof id === "string") {
    return id.toUpperCase();
  }

  return id.toFixed(0);
}
```

在 `if` 分支中，TypeScript 知道 `id` 是 `string`；在剩餘路徑中，知道它是 `number`。這個過程叫做 **Narrowing（型別縮小）**。

常見檢查方式：

```ts
typeof value === "string"
typeof value === "number"
Array.isArray(value)
value instanceof Date
"property" in value
```

注意：檢查陣列不能使用 `typeof value === "array"`，因為 JavaScript 中陣列的 `typeof` 結果是 `"object"`。

***

#### 1.6. 泛型

泛型可以理解成“型別的引數”：

```ts
const names: Array<string> = ["小明", "小红"];
const scores: Array<number> = [90, 85];
```

也可以編寫自己的泛型：

```ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const name = first(["小明", "小红"]);
// 推斷為 string | undefined

const score = first([90, 85]);
// 推斷為 number | undefined
```

這裡的 `T` 會根據呼叫時傳入的資料確定。泛型的價值是：**在複用程式碼的同時，保留準確的型別資訊。**

***

#### 1.7. 結構化型別系統

TypeScript 主要看一個值“具有哪些屬性”，而不是看它是否明確宣告瞭某個型別：

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

雖然 `position` 沒有宣告為 `Point`，但它擁有 `x` 和 `y`，而且型別正確，因此可以使用。

這叫做**結構型別**，也常被形象地稱作“鴨子型別”：如果它具有所需的形狀和行為，就可以作為該型別使用。

### 2、初學者需要補充理解的知識

#### 2.1. TypeScript 只在開發階段檢查型別

TypeScript 最終會被編譯成 JavaScript：

```ts
const age: number = 18;
```

編譯後大致是：

```js
const age = 18;
```

型別標註不會保留到執行階段。因此 TypeScript 並不能自動驗證介面、表單或 JSON 中的外部資料：

```ts
const response = await fetch("/api/user");
const data = await response.json();
```

伺服器返回的內容仍然可能不符合預期。真實專案通常會使用執行階段判斷，或者 Zod 等資料驗證庫。

***

#### `2.2.interface` 和 `type` 怎麼選擇

兩者都能描述物件：

```ts
interface User {
  name: string;
}

type Product = {
  name: string;
};
```

簡單選擇方法：

* 描述物件或類的公共結構：優先考慮 `interface`
* 聯合型別、元組或組合型別：使用 `type`
* 團隊已有統一規範：遵循團隊規範

```ts
type Result =
  | { success: true; data: string }
  | { success: false; error: string };
```

不要把它們理解成競爭關係，它們各有擅長的場景。

***

#### 2.3. 可選屬性與只讀屬性

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
// user.id = 2; // 錯誤：id 是隻讀屬性
```

* `email?`：屬性可以不存在
* `readonly`：透過該型別引用時不能重新賦值

***

#### 2.4. 陣列、元組和普通物件

```ts
const numbers: number[] = [1, 2, 3];

const coordinate: [number, number] = [10, 20];

const scores: Record<string, number> = {
  Alice: 95,
  Bob: 88,
};
```

* 陣列：元素型別相同，長度通常不固定
* 元組：位置和長度具有明確含義
* `Record<K, V>`：鍵和值分別具有統一型別

***

#### 2.5. 儘早開啟嚴格檢查

學習和新專案建議啟用嚴格模式：

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

它能開啟更嚴格的空值、函式引數和屬性檢查。剛開始錯誤會多一些，但能幫助你形成更可靠的型別習慣。

### 3、一個綜合範例

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

這個例子包含：

* 物件介面
* 函式引數和返回值
* 字面量聯合型別
* 可選屬性
* 只讀屬性
* 對 `undefined` 的型別縮小

### 4、推薦學習順序

1. JavaScript 基礎：變數、函式、物件、陣列和模組
2. TypeScript 基礎型別與型別推斷
3. 物件型別、`interface` 和 `type`
4. 聯合型別與型別縮小
5. 函式型別
6. 泛型
7. 類與模組
8. 工具型別：`Partial`、`Pick`、`Omit`、`Record`
9. `tsconfig.json` 和嚴格模式

學習 TypeScript 最重要的思維不是“給所有變數加型別”，而是：

> 用型別描述資料可能是什麼、不可能是什麼，以及不同資料之間有什麼關係。



typeof value === "string" 中的===是什麼意思？

***

`===` 是 JavaScript/TypeScript 中的**嚴格相等運算子**，用於判斷左右兩邊的值和型別是否都相等。

```ts
typeof value === "string"
```

可以分成兩步理解：

```ts
typeof value
```

獲取 `value` 在執行階段的型別名稱，例如 `"string"`、`"number"`。

```ts
typeof value === "string"
```

判斷這個型別名稱是否嚴格等於 `"string"`，也就是判斷 `value` 是否為字串。

```ts
const value = "你好";

console.log(typeof value);              // "string"
console.log(typeof value === "string"); // true
```

#### `===` 和 `==` 的區別

`===` 不會自動轉換型別，而 `==` 可能先轉換型別再比較：

```ts
5 === 5;   // true
5 === "5"; // false：型別不同

5 == "5";  // true：字串 "5" 被轉換後再比較
```

通常推薦使用 `===`，因為它的行為更明確、更不容易產生意外結果。

在 TypeScript 中，這種判斷還會觸發**型別縮小**：

```ts
function print(value: string | number) {
  if (typeof value === "string") {
    // 此處 TypeScript 知道 value 是 string
    console.log(value.toUpperCase());
  } else {
    // 此處 TypeScript 知道 value 是 number
    console.log(value.toFixed(2));
  }
}
```



## 二、為 Java/C# 程式設計師準備的 TypeScript

[：https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html)

總結頁面內容，並進行知識拓展

***

這篇文章主要面向熟悉 Java/C# 的程式設計師，但對初學者也很有價值。它強調的不是 TypeScript 語法，而是一個關鍵觀念：

> TypeScript 雖然擁有類、介面和靜態型別，但它的底層仍然是 JavaScript，不能完全套用 Java/C# 的思維。

以下內容根據 [TypeScript 官方文件：TypeScript for Java/C# Programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html) 整理。

### 1、先學一點 JavaScript

TypeScript 不會改變 JavaScript 的執行方式。

例如：

* 字串如何轉數字
* 陣列如何遍歷
* 非同步請求如何執行
* 檔案如何讀取
* 物件和原型如何工作

這些仍然屬於 JavaScript 的知識。

```ts
const text: string = "123";
const value: number = Number(text);
```

`: string` 和 `: number` 是 TypeScript 型別標註；真正把字串轉換成數字的是 JavaScript 的 `Number()`。

編譯後，型別會消失：

```js
const text = "123";
const value = Number(text);
```

因此，學習 TypeScript 時也要學習 JavaScript，尤其是：

* 物件和陣列
* 函式
* 模組
* 閉包
* `this`
* Promise 和 `async/await`
* JavaScript 的型別轉換規則

### 2、重新思考“類”

Java/C# 的常見思維

在 Java/C# 中，資料和函式通常放在類中：

```java
class MathUtils {
    static int add(int a, int b) {
        return a + b;
    }
}
```

TypeScript/JavaScript 的常見寫法

JavaScript 允許函式獨立存在，不必為了組織程式碼而建立類：

```ts
export function add(a: number, b: number): number {
  return a + b;
}
```

資料也可以是普通物件：

```ts
interface User {
  name: string;
  age: number;
}

function introduce(user: User): string {
  return `我是${user.name}，今年${user.age}岁`;
}
```

這裡不需要 `UserService`、`UserUtils` 或其他包裝類。

靜態工具類通常沒有必要

不推薦為了模仿 Java 而這樣寫：

```ts
class StringUtils {
  static capitalize(value: string): string {
    return value[0].toUpperCase() + value.slice(1);
  }
}
```

直接匯出函式通常更簡單：

```ts
export function capitalize(value: string): string {
  return value[0].toUpperCase() + value.slice(1);
}
```

JavaScript 模組本身已經能提供：

* 名稱空間
* 私有作用域
* 單例式載入
* 匯入和匯出

但類並不是不能用

當問題本身適合用物件表達狀態和行為時，類依然很合適：

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

TypeScript 支援熟悉的物件導向功能：

* `class`
* `extends`
* `implements`
* `public`
* `protected`
* `private`
* `abstract`
* `static`

核心原則是：**根據問題選擇類，而不是為了組織程式碼而強行建立類。**

### 3、把型別理解為“值的集合”

這是文章中最重要的思想之一。

```ts
type Text = string;
```

可以理解為：`Text` 是所有字串組成的集合。

```ts
type Id = string | number;
```

`Id` 則是字串集合與數字集合的並集：

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
id = true; // 錯誤
```

因為 `true` 不屬於 `string | number` 這個集合。

一個值可以屬於多個型別

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

`person` 同時符合：

* `Named`
* `Employee`
* `{ name: string; employeeId: number }`

所以一個值不一定只有一個唯一的 TypeScript 型別。

### 4、結構型別系統

Java/C# 主要採用**名義型別系統**：型別之間通常需要明確宣告關係。

例如：

```java
class Dog implements Animal {}
```

TypeScript 主要採用**結構型別系統**：重點是物件擁有哪些屬性，而不是它宣告自己屬於哪個型別。

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

`position` 沒有顯式宣告為 `Point`，但是它擁有符合要求的：

```ts
x: number;
y: number;
```

所以可以傳給 `printPoint()`。

可以把它簡單理解成：

> 不在乎你叫什麼型別，只在乎你是否具備我需要的結構。

### 5、結構型別帶來的特殊現象

#### 1. 空型別幾乎接受任何物件

```ts
class Empty {}

function handle(value: Empty): void {}

handle({ name: "小明" }); // 可以
handle({ count: 10 });    // 也可以
```

為什麼？

`Empty` 沒有要求任何屬性。任何物件都擁有它所要求的全部屬性——因為它什麼都沒要求。

所以空介面也沒有“任意物件必須顯式實現它”的效果：

```ts
interface Empty {}

const value: Empty = { anything: 123 };
```

因此不要把空介面當作 Java 中的標記介面。

***

#### 2. 結構相同的類可能相互相容

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

雖然業務含義完全不同，但 TypeScript 看到的結構都是：

```ts
{
  drive(): void;
}
```

所以兩者相容。

不過，如果類包含 `private` 或 `protected` 成員，相容規則會更加嚴格：

```ts
class Car {
  private brand = "car";

  drive(): void {}
}

class Golfer {
  private brand = "golfer";

  drive(): void {}
}

// let car: Car = new Golfer(); // 錯誤
```

### 6、型別在執行階段會被刪除

TypeScript 的介面、型別別名和泛型主要用於編譯階段：

```ts
interface User {
  name: string;
}

const user: User = {
  name: "小明",
};
```

編譯成 JavaScript 後大致為：

```js
const user = {
  name: "小明",
};
```

執行階段不存在 `User` 這個介面。

所以這樣做是不可能的：

```ts
interface User {
  name: string;
}

// if (value instanceof User) {} // 錯誤：User 不是執行階段的值
```

`interface` 只存在於“型別空間”，不能傳給 `instanceof`。

### 7、`typeof` 和 `instanceof` 的能力有限

#### `typeof`

`typeof` 可以檢查 JavaScript 的基礎執行階段型別：

```ts
function print(value: string | number): void {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  } else {
    console.log(value.toFixed(2));
  }
}
```

常見結果包括：

```ts
typeof "hello";       // "string"
typeof 123;           // "number"
typeof true;          // "boolean"
typeof undefined;     // "undefined"
typeof (() => {});    // "function"
typeof {};            // "object"
typeof [];            // "object"
typeof null;          // "object"（JavaScript 的歷史遺留行為）
```

`typeof new Car()` 的結果也是 `"object"`，不會得到 `"Car"`。

#### `instanceof`

類在執行階段是真實存在的 JavaScript 值，因此可以使用 `instanceof`：

```ts
class Car {
  drive(): void {}
}

const value = new Car();

console.log(value instanceof Car); // true
```

但 `instanceof` 檢查的是物件的原型鏈，不是 TypeScript 介面結構。

### 8、執行階段如何判斷介面型別

如果資料來自介面、檔案或使用者輸入，不能只寫一個型別斷言：

```ts
const user = JSON.parse(text) as User;
```

`as User` 不會驗證資料，只是在告訴編譯器“請相信我”。

更安全的方式是編寫型別守衛：

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

真實專案中也常使用 Zod、Valibot 等執行階段驗證庫。

### 9、知識拓展：需要名義型別時怎麼辦

有時兩個值結構相同，但業務上絕不能混用，例如使用者 ID 和訂單 ID：

```ts
type UserId = string;
type OrderId = string;

const userId: UserId = "U100";
const orderId: OrderId = userId; // 可以，但業務上可能不合理
```

可以使用“品牌型別”模擬名義型別：

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

// const orderId: OrderId = userId; // 錯誤
```

這種寫法常用於：

* 不同種類的 ID
* 不同貨幣
* 已驗證與未驗證的資料
* 不同計量單位

### 10、知識拓展：用可辨識聯合表達物件型別

與其依賴複雜的類繼承，有時可以使用聯合型別：

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

`kind` 是識別不同型別的標籤。TypeScript 會根據它自動收窄型別。

這種模式非常適合：

* 請求狀態
* 操作結果
* 訊息型別
* UI 狀態
* Redux action
* API 成功與失敗響應

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





## 三、JavaScript 模組

這裡的“JavaScript 模組”主要指現代的 **ES Module（ESM）**。它透過 `export` 和 `import` 把程式碼拆分到不同檔案中。

假設專案結構如下：

```text
src/
├─ main.ts
├─ math.ts
└─ user.ts
```

只要檔案中出現頂層 `import` 或 `export`，TypeScript 通常就會把它視為模組：

```ts
export {};
```

即使沒有真正匯出內容，這句也可以明確告訴 TypeScript：“這是一個模組，不是全域性指令碼。”

***

### 1、模組提供名稱空間

“名稱空間”解決的是**名稱衝突和程式碼歸類**問題。

假設兩個檔案都定義了 `format()`：

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

它們雖然同名，但屬於不同模組，因此不會衝突。

匯入時可以改名：

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

這裡每個檔案天然形成一個獨立的名稱空間。

#### 1.1、整體匯入為模組物件

也可以把整個模組匯入為一個物件：

```ts
import * as DateUtils from "./date-utils.js";
import * as NumberUtils from "./number-utils.js";

DateUtils.format(new Date());
NumberUtils.format(3.14);
```

`DateUtils` 和 `NumberUtils` 被稱為**模組名稱空間物件**。

這看起來很像靜態工具類：

```ts
DateUtils.format(...)
```

但不需要建立：

```ts
class DateUtils {
  static format(...) {}
}
```

#### 1.2、與 TypeScript `namespace` 的區別

TypeScript 還有一個 `namespace` 關鍵字：

```ts
namespace DateUtils {
  export function format(date: Date) {
    return date.toISOString();
  }
}
```

不過在現代模組化專案中，通常優先使用檔案模組：

```ts
// date-utils.ts
export function format(date: Date) {
  return date.toISOString();
}
```

因為 ES Module：

* 是 JavaScript 標準
* 瀏覽器和 Node.js 原生支援
* 構建工具能夠分析
* 更容易進行 tree shaking
* 與 npm 包的組織方式一致

所以這裡所說的“模組提供名稱空間”，不是說必須使用 `namespace` 關鍵字，而是說：**每個模組天然隔離自己的名稱。**

***

### 2、模組提供私有作用域

預設情況下，模組中宣告的變數、函式和類只在當前模組內部可見。

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

這裡：

```ts
count
validateAmount
```

沒有被匯出，因此屬於模組內部實現。

其他檔案只能使用匯出的成員：

```ts
import {
  increment,
  getCount,
} from "./counter.js";

increment(2);
console.log(getCount());

// count;          // 錯誤：不可見
// validateAmount; // 錯誤：不可見
```

這就是模組級私有作用域。

#### 2.1、“私有”不等於 `private`

它與類的 `private` 是兩個不同層面的概念。

類私有成員：

```ts
class Counter {
  private count = 0;
}
```

模組私有成員：

```ts
let count = 0;

export function increment() {
  count++;
}
```

區別是：

* 類的 `private` 保護某個物件或類的內部成員
* 模組作用域保護整個檔案或模組的內部實現
* 模組私有不需要額外關鍵字
* 只要不 `export`，其他模組就不能直接匯入

#### 2.2、可以隱藏具體實現，只暴露公共介面

```ts
// password.ts

function hashInternal(password: string): string {
  // 內部演算法
  return `hashed:${password}`;
}

export function createPassword(password: string): string {
  if (password.length < 8) {
    throw new Error("密码至少需要 8 个字符");
  }

  return hashInternal(password);
}
```

使用者只能呼叫：

```ts
import { createPassword } from "./password.js";
```

以後即使更換 `hashInternal()` 的實現，只要 `createPassword()` 的使用方式不變，其他檔案通常就不需要修改。

這就是所謂的**封裝**。

#### 2.3、瀏覽器中也不會自動汙染全域性變數

傳統普通指令碼：

```html
<script src="a.js"></script>
<script src="b.js"></script>
```

如果兩個指令碼都在頂層宣告同名變數，可能發生衝突。

模組指令碼：

```html
<script type="module" src="./main.js"></script>
```

模組內部的頂層宣告不會自動成為 `window` 的屬性：

```js
const message = "hello";

console.log(window.message); // undefined
```

***

### 3、模組提供“單例式載入”

模組第一次被載入時，頂層程式碼會執行一次。之後再次匯入時，執行環境通常會複用已經載入過的模組實例。

考慮下面的模組：

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

兩個檔案分別匯入它：

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

如果 `page-a.ts` 和 `page-b.ts` 處於同一模組載入環境中，它們訪問的通常是同一個 `counter` 模組實例：

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

這意味著模組內部的：

```ts
let count = 0;
```

只初始化一次，並由所有匯入者共享。

因此它具有類似單例的效果。

***

### 4、模組提供匯出

`export` 決定模組願意向外公開什麼。

#### 4.1、命名匯出

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

也可以先宣告，最後統一匯出：

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

匯出時還可以改名：

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

#### 4.2、預設匯出

一個模組最多只能有一個預設匯出：

```ts
// UserService.ts

export default class UserService {
  findUser(id: number): void {
    console.log(id);
  }
}
```

匯入預設值時，可以自行選擇本地名稱：

```ts
import UserService from "./UserService.js";
```

也可以：

```ts
import Service from "./UserService.js";
```

因為預設匯入不依賴原來的名字。

#### 4.3、命名匯出與預設匯出怎麼選

命名匯出的優勢是名稱統一：

```ts
import { createUser } from "./user.js";
```

編輯器也更容易自動補全和批次重新命名。因此應用程式碼中，很多團隊更傾向命名匯出。

預設匯出常見於：

* 一個檔案主要匯出一個元件
* 某些框架規定的檔案結構
* 第三方庫的既有 API

兩者可以共存：

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

### 5、模組提供匯入

#### 5.1、匯入命名成員

```ts
import {
  add,
  PI,
} from "./math.js";

console.log(add(1, 2));
console.log(PI);
```

命名必須與匯出名稱匹配。

#### 5.2、匯入時改名

```ts
import {
  add as calculateTotal,
} from "./math.js";

calculateTotal(1, 2);
```

#### 5.3、匯入預設成員

```ts
import UserService from "./UserService.js";
```

預設匯入沒有花括號。

#### 5.4、匯入整個模組

```ts
import * as MathUtils from "./math.js";

MathUtils.add(1, 2);
console.log(MathUtils.PI);
```

#### 5.5、只執行模組，不匯入成員

```ts
import "./setup.js";
```

這種寫法用於模組的副作用。例如：

```ts
// setup.ts
console.log("正在初始化应用");
registerGlobalHandlers();
```

在入口檔案中：

```ts
import "./setup.js";
```

應該謹慎使用副作用匯入，因為它可能使程式行為依賴載入順序。



## 四、5分鐘瞭解TypeScript

原文地址：[https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html](https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html)

***

這篇官方教程透過一個簡單的網頁問候程式，展示 TypeScript 的核心工作方式：

> 編寫 `.ts` → 靜態型別檢查 → 編譯為 `.js` → 由瀏覽器或 Node.js 執行。

TypeScript 本身不是新的執行環境；最終執行的仍然是 JavaScript。[官方教程](https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html)

### 1. 頁面內容總結

#### 安裝與編譯

頁面使用全域性安裝：

```bash
npm install -g typescript
tsc greeter.ts
```

`tsc` 是 TypeScript 編譯器。它檢查 `greeter.ts`，然後生成瀏覽器能執行的 `greeter.js`。

實際專案中更建議本地安裝，避免不同專案之間版本衝突：

```bash
npm init -y
npm install --save-dev typescript
npx tsc --init
npx tsc
```

#### TypeScript 可以直接接受 JavaScript

最初的檔案雖然使用 `.ts` 副檔名，內容卻完全是 JavaScript：

```ts
function greeter(person) {
  return "Hello, " + person;
}

const user = "Jane User";

document.body.textContent = greeter(user);
```

這體現了 TypeScript 的重要特徵：它是 JavaScript 的超集，大量 JavaScript 程式碼可以直接遷移到 TypeScript。

#### 型別註解

給引數新增 `: string`：

```ts
function greeter(person: string) {
  return "Hello, " + person;
}
```

它表示函式要求呼叫者傳入字串。下面的程式碼會產生編譯錯誤：

```ts
greeter([0, 1, 2]);
// number[] 不能賦值給 string
```

型別註解可以理解為一份“呼叫契約”：

```ts
function add(a: number, b: number): number {
  return a + b;
}
```

* `a: number`：引數型別
* `b: number`：引數型別
* `): number`：返回值型別

不過並非處處都要手寫型別。TypeScript 經常能夠自動推斷：

```ts
const name = "Alice"; // 推斷為 string
const scores = [90, 85]; // 推斷為 number[]
```

官方也建議初學時不要新增過多多餘註解。[常用型別與型別推斷](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)

#### 介面與結構化型別

頁面定義了一個介面：

```ts
interface Person {
  firstName: string;
  lastName: string;
}
```

然後讓函式接收符合這個結構的物件：

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

`user` 沒有顯式宣告 `implements Person`，但它擁有介面要求的兩個屬性，所以可以傳入。

這叫作結構化型別系統，通俗地說：

> TypeScript 關心一個值“長什麼樣、能做什麼”，而不是它明確聲稱自己屬於哪個型別。

例如，多出屬性通常也沒有問題：

```ts
const employee = {
  firstName: "Jane",
  lastName: "User",
  department: "Engineering",
};

greeter(employee); // 可以
```

但直接傳物件字面量時，會觸發額外屬性檢查：

```ts
greeter({
  firstName: "Jane",
  lastName: "User",
  department: "Engineering", // 通常報錯：Person 中沒有該屬性
});
```

#### 類

頁面最後定義了一個 `Student` 類：

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

構造器引數前的 `public` 是一種簡寫：

```ts
constructor(public firstName: string) {}
```

大致等價於：

```ts
firstName: string;

constructor(firstName: string) {
  this.firstName = firstName;
}
```

`Student` 實例包含 `firstName` 和 `lastName`，因此符合 `Person` 的結構：

```ts
const user = new Student("Jane", "M.", "User");
greeter(user); // 可以
```

這裡沒有使用繼承。它展示的是“類的實例可以符合介面”。

#### 在瀏覽器執行

HTML 引入的不是 `.ts`，而是編譯後的 `.js`：

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

瀏覽器通常不會直接執行 TypeScript，因此完整流程是：

```text
greeter.ts
    ↓ tsc：型別檢查並轉換
greeter.js
    ↓ 瀏覽器載入
網頁執行
```

### 2. 最重要的知識擴充套件

#### 型別只存在於編譯階段

介面和大部分型別註解不會出現在最終 JavaScript 中：

```ts
interface User {
  name: string;
}

const user: User = { name: "Alice" };
```

編譯後大致只剩：

```js
const user = { name: "Alice" };
```

所以 TypeScript 型別不能自動驗證網路資料：

```ts
const response = await fetch("/api/user");
const data = await response.json();
```

`data` 來自執行階段，可能不符合你期望的結構。真正的專案需要自行校驗，或者使用 Zod 等執行階段驗證庫。

#### 型別錯誤不一定阻止生成 JavaScript

教程指出，即使發生型別錯誤，`tsc` 預設仍可能生成 JavaScript。這是因為 `noEmitOnError` 預設是 `false`。

專案中可以啟用：

```json
{
  "compilerOptions": {
    "noEmitOnError": true
  }
}
```

這樣存在型別錯誤時就不輸出 JavaScript。[官方配置說明](https://www.typescriptlang.org/tsconfig/noEmitOnError.html)

#### 建議開啟嚴格模式

初學時就開啟嚴格檢查，長期反而更容易形成正確習慣：

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict` 會同時啟用一組嚴格型別檢查規則，提供更強的正確性保證。[官方 strict 說明](https://www.typescriptlang.org/tsconfig/strict.html)

例如：

```ts
function greeter(person) {
  // strict 模式下，person 隱式為 any 會報錯
}
```

#### 儘量避免 `any`

`any` 相當於告訴 TypeScript：“不要檢查這個值”：

```ts
let value: any = "hello";

value.notExistingMethod(); // 編譯器不阻止，執行階段可能崩潰
```

不確定型別時，優先考慮 `unknown`：

```ts
function printValue(value: unknown) {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  }
}
```

`unknown` 會要求你先檢查型別，這個過程叫型別縮小。

#### `interface` 和 `type` 的簡單選擇

物件結構通常可以使用任意一種：

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

初學階段可以這樣記：

* 描述物件、類的公共結構：優先考慮 `interface`
* 聯合型別、元組或複雜組合：使用 `type`

例如：

```ts
type ID = string | number;
type Point = [number, number];
```

`interface` 可以宣告合併，而 `type` 能表達更廣泛的型別組合。[官方對比](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#differences-between-type-aliases-and-interfaces)

### 3. 更適合現在專案的完整範例

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

建議的 `tsconfig.json`：

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

注意：設定 `outDir: "dist"` 後，HTML 中應改為：

```html
<script src="dist/greeter.js" defer></script>
```

### 4. 推薦學習順序

學完這個頁面後，可以依次學習：

1. 基礎型別和型別推斷
2. 陣列、物件、函式型別
3. 可選屬性與聯合型別
4. 型別縮小
5. `interface` 與 `type`
6. 泛型
7. 模組：`import` / `export`
8. `tsconfig.json`
9. 非同步函式和 `Promise`
10. DOM 型別或 Node.js 型別

這篇頁面真正需要建立的核心認識是：

> TypeScript 利用靜態型別，在程式碼執行之前發現一部分錯誤，併為編輯器提供補全、跳轉、重構等能力；編譯後，程式仍然是 JavaScript。



## 五、The TypeScript Handbook

原文地址：[https://www.typescriptlang.org/docs/handbook/intro.html](https://www.typescriptlang.org/docs/handbook/intro.html)

***

這篇是 TypeScript Handbook 的“使用說明”，重點不是語法，而是回答三個問題：

1. TypeScript 為什麼存在？
2. Handbook 應該怎樣閱讀？
3. Handbook 不會教什麼？

[TypeScript Handbook 導言](https://www.typescriptlang.org/docs/handbook/intro.html)

### 1. TypeScript 為什麼出現？

JavaScript 最初主要用於給網頁增加簡單互動，後來逐漸擴充套件到：

* 大型前端應用
* Node.js 後端
* 桌面應用
* 移動應用
* 跨平臺工具

隨著專案變大，程式碼之間的關係越來越複雜，但原生 JavaScript 不容易直接表達這些關係。

例如：

```js
function calculatePrice(price, quantity) {
  return price * quantity;
}

calculatePrice("100", 2);
```

呼叫者到底應該傳入數字還是字串？單看函式名並不明確。JavaScript 通常要等程式碼執行後，才能發現某些問題。

TypeScript 可以明確表達約束：

```ts
function calculatePrice(
  price: number,
  quantity: number,
): number {
  return price * quantity;
}

calculatePrice("100", 2);
// 錯誤：string 不能傳給 number
```

因此，TypeScript 的核心目標是：

> 在 JavaScript 程式碼執行之前，對它進行靜態型別檢查。

“靜態”表示執行前，“型別檢查”表示檢查值的使用方式是否符合預期。[官方說明](https://www.typescriptlang.org/docs/handbook/intro.html#about-this-handbook)

### 2. TypeScript 主要防止什麼錯誤？

頁面指出，程式中很多常見錯誤都屬於型別錯誤，例如：

#### 拼寫錯誤

```ts
const user = {
  name: "Alice",
};

console.log(user.naem);
// 錯誤：不存在 naem，可能想寫 name
```

#### 誤解第三方 API

```ts
const names = ["Alice", "Bob"];

names.push(100);
// 錯誤：number 不能加入 string[]
```

#### 錯誤理解返回值

```ts
function findUser(): User | undefined {
  // ...
}

const user = findUser();
console.log(user.name);
// 錯誤：user 可能是 undefined
```

#### 使用了錯誤的引數

```ts
function setAge(age: number) {}

setAge("十八");
// 錯誤：string 不能傳給 number
```

這些錯誤不一定會立即導致程式崩潰，但往往代表程式設計師的假設和實際程式碼不一致。

### 3. 靜態檢查不等於執行階段檢查

這是導言背後最重要的知識擴充套件。

TypeScript 檢查的是原始碼，型別通常會在編譯時被刪除：

```ts
function greet(name: string): string {
  return `Hello, ${name}`;
}
```

編譯後大致為：

```js
function greet(name) {
  return `Hello, ${name}`;
}
```

因此 TypeScript 不能保證外部資料一定正確：

```ts
interface User {
  id: number;
  name: string;
}

const response = await fetch("/api/user");
const user = (await response.json()) as User;
```

這裡的 `as User` 只是告訴編譯器“把它當成 User”，不會真正驗證伺服器返回的資料。

如果伺服器返回：

```json
{
  "id": "not-a-number",
  "name": null
}
```

TypeScript 在執行階段不會自動阻止它。

所以應該區分：

| **檢查方式**        | **發生時間** | **範例**      |
| --------------- | -------- | ----------- |
| TypeScript 靜態檢查 | 執行前      | 引數型別、屬性拼寫   |
| 執行階段驗證           | 程式執行階段    | API 響應、使用者輸入 |
| 自動化測試           | 執行測試時    | 業務邏輯是否正確    |

簡單的執行階段驗證可以這樣寫：

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

### 4. Handbook 的結構

官方文件主要分成兩種內容。

#### Handbook

Handbook 是連續的學習材料，適合按照左側目錄從上往下閱讀。

完成後，讀者應該能夠：

* 閱讀常見的 TypeScript 語法
* 理解常見的 TypeScript 程式設計模式
* 解釋重要編譯器選項的作用
* 預測大部分型別系統行為

它是一份綜合指南，但不是完整的語言規範。[Handbook 結構說明](https://www.typescriptlang.org/docs/handbook/intro.html#how-is-this-handbook-structured)

#### Reference

Reference 是專題參考資料，例如：

* Utility Types
* 型別推斷
* 型別相容性
* 列舉
* 裝飾器
* 宣告合併

它不強調連續性，適合已經知道概念名稱之後查閱。

可以這樣理解：

* Handbook：像教材
* Reference：像詞典
* TSConfig Reference：像配置說明書
* Language Specification：偏向語言實現者的正式定義

初學時不要試圖從頭讀完 Reference。

### 5. Handbook 不教什麼？

#### 不繫統教授 JavaScript 基礎

Handbook 預設你對以下 JavaScript 概念有一定了解：

* 變數與作用域
* 條件語句和迴圈
* 函式
* 物件與陣列
* 類
* 閉包
* Promise 和非同步程式設計
* ES 模組

例如：

```ts
const double = (value: number) => value * 2;
```

TypeScript Handbook 會解釋 `value: number`，但不一定詳細解釋箭頭函式本身。

如果 TypeScript 是你的第一門語言，官方建議先學習 JavaScript 基礎。[官方初學建議](https://www.typescriptlang.org/docs/handbook/intro.html#about-this-handbook)

#### 不是完整語言規範

Handbook 以容易理解為目標，不會覆蓋所有邊界情況和形式化規則。

例如，初學時只需要知道結構符合就可能型別相容：

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

至於結構化型別系統的全部相容規則，應在需要時再查 Reference。

#### 不負責講解所有工具鏈

Handbook 不會系統教授 TypeScript 如何與這些工具整合：

* React、Vue、Angular、Svelte
* Vite、webpack、Rollup
* Babel
* npm、pnpm、Yarn
* 測試框架
* 單體倉庫工具

這些屬於生態和工程工具，不是 TypeScript 型別系統本身。

### 6. 根據背景選擇入口

官方給出了幾種入口：

* 完全沒有程式設計基礎：先學習 JavaScript
* 會 JavaScript：閱讀 TypeScript for JavaScript Programmers
* 會 Java/C#：閱讀 TypeScript for Java/C# Programmers
* 熟悉函數語言程式設計：閱讀對應介紹
* 已理解基本定位：直接進入 The Basics

如果你是 TypeScript 和 JavaScript 的初學者，我建議採用雙線學習：

```text
JavaScript 基礎
    ├─ 變數、函式、物件、陣列
    ├─ 作用域、閉包
    ├─ 類和原型
    ├─ Promise / async
    └─ import / export
              ↓
TypeScript 型別系統
    ├─ 基礎型別
    ├─ 函式和物件型別
    ├─ 聯合型別與型別縮小
    ├─ interface / type
    ├─ 泛型
    └─ 模組與編譯配置
```

不要等“徹底學完 JavaScript”再碰 TypeScript。可以學完一個 JavaScript 概念，緊接著學習它對應的 TypeScript型別表達。

### 7. 對“型別”的正確理解

初學者容易把型別理解成給變數貼標籤：

```ts
let age: number = 18;
```

更有價值的理解是：型別表達程式碼之間的關係。

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

這裡表達了三個關係：

* 輸入必須符合 `Product.id` 的型別
* 成功時返回 `Product`
* 查詢失敗時返回 `undefined`

呼叫者因此必須處理失敗情況：

```ts
const product = findProduct("p-001");

if (product) {
  console.log(product.price);
}
```

型別系統的真正價值不是讓程式碼顯得嚴格，而是讓函式、資料和模組之間的假設變得明確。

### 8. 推薦的 Handbook 閱讀順序

對於初學者，建議按下面的順序：

1. [The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html)
2. Everyday Types
3. Narrowing
4. More on Functions
5. Object Types
6. Generics
7. Classes
8. Modules

第一遍可以暫時跳過：

* Conditional Types
* Mapped Types
* Template Literal Types
* Declaration Merging
* Decorators
* 自己編寫 `.d.ts`

最後，用一句話總結這篇導言：

> TypeScript 是 JavaScript 的靜態型別檢查器；Handbook 教你理解和使用它的型別系統，但不會代替 JavaScript 基礎課程、完整語言規範或前端工程工具教程。



## 六、The Basics

原文地址：[https://www.typescriptlang.org/docs/handbook/2/basic-types.html](https://www.typescriptlang.org/docs/handbook/2/basic-types.html)

***

這篇 [TypeScript Handbook：The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) 並不是在羅列 `string`、`number` 等基礎型別，而是在解釋 TypeScript 的核心工作方式：**在 JavaScript 執行之前，透過靜態型別分析提前發現錯誤。**

### 1、頁面核心內容

#### 1.1. TypeScript 是 JavaScript 的靜態型別檢查器

JavaScript 通常要執行程式碼後，才能發現某些錯誤：

```js
const message = "Hello World";

message(); // 執行階段報錯：message 不是函式
```

TypeScript 可以在執行前發現它：

```ts
const message = "Hello World";

message();
// 編譯錯誤：This expression is not callable.
```

可以這樣理解：

* JavaScript：執行階段才檢查值能做什麼。
* TypeScript：編寫和編譯時預測值能做什麼。
* TypeScript 最終仍然生成 JavaScript，由瀏覽器或 Node.js 執行。

型別描述的其實是一個值具有哪些“能力”。例如：

* `string` 可以呼叫 `toLowerCase()`。
* 函式可以被呼叫。
* `Date` 可以呼叫 `toDateString()`。
* 普通物件只能訪問其型別中存在的屬性。

***

#### 1.2. TypeScript 還能發現“不一定立即報錯”的問題

下面的 JavaScript 可以執行，但很可能是程式錯誤：

```js
const user = {
  name: "Daniel",
  age: 26,
};

console.log(user.location); // undefined
```

TypeScript 會提前指出：

```ts
user.location;
// Property 'location' does not exist
```

它還能發現：

##### 拼寫錯誤

```ts
const announcement = "Hello";

announcement.toLocalLowerCase(); // 方法名寫錯
announcement.toLocaleLowerCase(); // 正確
```

##### 忘記呼叫函式

```ts
Math.random < 0.5;   // 錯誤：比較的是函式本身
Math.random() < 0.5; // 正確：比較函式返回值
```

##### 不可能成立的邏輯

```ts
const value = Math.random() < 0.5 ? "a" : "b";

if (value !== "a") {
  // 這裡 value 已經只能是 "b"
} else if (value === "b") {
  // 永遠無法到達
}
```

這體現了 TypeScript 一個重要能力：它不僅檢查型別名稱，還會根據程式流程分析變數當前可能的取值。

***

#### 1.3. 型別也能增強編輯器功能

型別資訊不僅用來報錯，也能支援：

* 自動補全
* 引數提示
* 跳轉到定義
* 查詢所有引用
* 自動重構
* 快速修復
* 滑鼠懸停檢視型別

因此，TypeScript 的價值不只是“少出錯”，也包括“更容易閱讀、修改和重構程式碼”。

***

#### 1.4. `tsc` 編譯器

`tsc` 是 TypeScript 官方編譯器。頁面展示的是全域性安裝方式；實際專案中更推薦把它安裝為專案開發依賴：

```bash
npm init -y
npm install --save-dev typescript
npx tsc --init
```

建立 `hello.ts`：

```ts
console.log("Hello world!");
```

編譯：

```bash
npx tsc hello.ts
```

通常會生成：

```text
hello.ts
hello.js
```

執行的是生成後的 JavaScript：

```bash
node hello.js
```

完整流程是：

```text
hello.ts
   ↓ TypeScript 型別檢查與轉換
hello.js
   ↓ JavaScript 執行環境
程式結果
```

***

#### 1.5. 預設情況下，有型別錯誤也可能生成 JavaScript

例如：

```ts
function greet(person: string, date: Date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}

greet("Alice"); // 缺少第二個引數
```

`tsc` 會報告錯誤，但預設情況下仍可能輸出 JavaScript。這是為了方便舊 JavaScript 專案逐步遷移到 TypeScript。

新專案通常應該禁止這種行為：

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

如果專案使用其他工具負責生成 JavaScript，還可以只做檢查：

```bash
npx tsc --noEmit
```

***

#### 1.6. 顯式型別標註

型別標註寫在變數或引數名稱之後：

```ts
function greet(person: string, date: Date): void {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}
```

含義分別是：

* `person: string`：引數必須是字串。
* `date: Date`：引數必須是 `Date` 物件。
* `: void`：函式不返回有意義的值。

注意 `Date()` 和 `new Date()` 不一樣：

```ts
Date();     // 返回 string
new Date(); // 返回 Date 物件
```

所以：

```ts
greet("Alice", Date());     // 錯誤
greet("Alice", new Date()); // 正確
```

***

#### 1.7. 型別推斷

並非所有地方都需要手動寫型別：

```ts
let message = "hello";
// TypeScript 推斷 message 為 string
```

下面的寫法通常沒有必要：

```ts
let message: string = "hello";
```

比較實用的原則是：

* 函式引數通常寫型別。
* 公共函式的返回值可以顯式標註。
* 普通區域性變數儘量讓 TypeScript 推斷。
* 推斷結果不夠準確時再補充型別。

例如：

```ts
function add(a: number, b: number): number {
  return a + b;
}

const result = add(10, 20); // 自動推斷為 number
```

***

#### 1.8. 型別會在編譯後被擦除

下面的 TypeScript：

```ts
function greet(person: string): string {
  return `Hello ${person}`;
}
```

編譯成 JavaScript 後大致是：

```js
function greet(person) {
  return `Hello ${person}`;
}
```

`string` 等型別資訊消失了。官方文件強調：**型別標註不會改變程式的執行階段行為。**

這會帶來一個非常重要的結論：

```ts
type User = {
  name: string;
};

const data = JSON.parse(input) as User;
```

寫成 `as User` 並不會檢查輸入中是否真的存在 `name`。它只是告訴編譯器“請把它當作 `User`”。

對於 API、JSON、表單等外部資料，仍然需要執行階段校驗：

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

#### 1.9. 降級編譯（downleveling）

TypeScript 可以把較新的 JavaScript 語法轉換為較舊的語法。

例如：

```ts
const message = `Hello ${name}`;
```

面向舊環境時可能轉換為：

```js
var message = "Hello ".concat(name);
```

由 `target` 決定輸出哪個版本的 JavaScript：

```json
{
  "compilerOptions": {
    "target": "ES2022"
  }
}
```

需要區分兩個概念：

* `target`：生成什麼版本的 JavaScript。
* `lib`：型別檢查時允許使用哪些平臺 API。

例如，能否使用 `document` 不只是由 `target` 決定，還取決於是否包含 DOM 型別庫。

***

#### 1.10. 嚴格模式

新專案建議啟用：

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict` 是一組嚴格檢查選項的總開關，其中頁面重點介紹了兩個。

##### `noImplicitAny`

如果 TypeScript 無法推斷引數型別，寬鬆模式下可能退化為 `any`：

```ts
function printName(name) {
  console.log(name.toUpperCase());
}
```

開啟嚴格檢查後，必須明確說明型別：

```ts
function printName(name: string): void {
  console.log(name.toUpperCase());
}
```

##### `strictNullChecks`

開啟後，`null` 和 `undefined` 不再能隨意賦給其他型別：

```ts
function findUser(): string | undefined {
  return Math.random() > 0.5 ? "Alice" : undefined;
}

const user = findUser();
console.log(user.toUpperCase()); // 錯誤：user 可能是 undefined
```

必須先縮小型別範圍：

```ts
if (user !== undefined) {
  console.log(user.toUpperCase());
}
```

或者在適合預設值的場景使用：

```ts
console.log((user ?? "Guest").toUpperCase());
```

### 2、知識擴充套件

#### 2.1. `any` 和 `unknown` 的區別

`any` 基本等於關閉型別檢查：

```ts
let value: any = "hello";

value.notExist();
value();
value.foo.bar;
```

這些操作編譯器可能都不阻止。

`unknown` 表示“型別暫時不知道”，使用前必須檢查：

```ts
let value: unknown = "hello";

if (typeof value === "string") {
  console.log(value.toUpperCase());
}
```

處理外部資料時，優先使用 `unknown`，儘量避免 `any`。

***

#### 2.2. TypeScript 採用結構型別系統

TypeScript 主要關心物件“長什麼樣”，而不是它叫什麼名字：

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

greet(employee); // 合法，因為 employee 至少具有 name: string
```

這種機制稱為結構型別（structural typing），也可以簡單理解成“鴨子型別的靜態版本”。

***

#### 2.3. 型別縮小（narrowing）

TypeScript 會根據條件判斷，把寬泛型別縮小成更具體的型別：

```ts
function format(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // 此處是 string
  }

  return value.toFixed(2); // 此處是 number
}
```

常見的縮小方式包括：

* `typeof`
* `instanceof`
* `in`
* 判空
* 字面量比較
* 自定義型別守衛

這是學完基礎後最值得繼續掌握的能力之一。

***

#### 2.4. TypeScript 不能保證程式絕對安全

TypeScript 擅長髮現：

* 引數型別不匹配
* 屬性不存在
* 可能為空
* 拼寫錯誤
* 某些不可能成立的邏輯

但它通常不能獨立發現：

* API 返回了錯誤格式的資料
* 使用者輸入不合法
* 資料庫內容不符合預期
* 網路錯誤
* 業務規則錯誤
* 陣列訪問越界等執行階段問題

所以正確認識是：

> TypeScript 提高了程式的靜態可靠性，但不能替代執行階段校驗、測試和錯誤處理。





## 七、Everyday Types

原文地址：[https://www.typescriptlang.org/docs/handbook/2/everyday-types.html](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)

***

這篇 [TypeScript Handbook：Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) 介紹開發中最常用的型別，是後續學習型別縮小、函式、泛型的基礎。

核心思想是：

> TypeScript 使用基本型別描述資料，再透過陣列、物件、聯合型別、字面量型別等方式組合出複雜型別。

### 1、基本型別

#### 1. `string`、`number`、`boolean`

```ts
const username: string = "Alice";
const age: number = 20;
const active: boolean = true;
```

JavaScript 不區分整數和浮點數，統一使用 `number`：

```ts
const count: number = 10;
const price: number = 19.99;
```

型別名稱應該使用小寫：

```ts
let name: string;   // 推薦
let age: number;
let active: boolean;
```

不要使用包裝物件型別：

```ts
let name: String;   // 不推薦
let age: Number;
let active: Boolean;
```

`string` 表示普通字串值，而 `String` 表示 JavaScript 的字串包裝物件。日常開發幾乎總是使用小寫版本。

***

#### 2. 陣列

有兩種等價寫法：

```ts
const scores: number[] = [90, 85, 100];
const names: Array<string> = ["Alice", "Bob"];
```

通常簡單型別使用 `T[]` 更易讀：

```ts
string[]
number[]
User[]
```

複雜型別有時使用泛型形式更清楚：

```ts
Array<string | number>
```

注意：

```ts
number[] // 任意長度的數字陣列
[number] // 只能包含一個數字的元組
```

知識擴充套件：如果陣列不應該被修改，可以使用只讀陣列。

```ts
const names: readonly string[] = ["Alice", "Bob"];

names.push("Eve"); // 錯誤
```

***

### 2、`any`

`any` 會關閉相關值的型別檢查：

```ts
let value: any = { name: "Alice" };

value.foo.bar();
value();
value = 100;

const age: number = value;
```

上面的程式碼基本都不會產生編譯錯誤，但執行階段可能崩潰。

因此建議：

* 開啟 `strict` 或 `noImplicitAny`。
* 不知道型別時優先使用 `unknown`。
* 只有遷移舊專案或處理確實無法描述的第三方資料時，才臨時使用 `any`。

#### `any` 和 `unknown`

```ts
let input: unknown = "hello";

input.toUpperCase(); // 錯誤：還不知道 input 是什麼

if (typeof input === "string") {
  input.toUpperCase(); // 正確
}
```

區別可以簡單記成：

| **型別**    | **含義**        |
| --------- | ------------- |
| `any`     | 不檢查，我自己負責     |
| `unknown` | 暫時不知道，使用前必須檢查 |

***

### 3、型別標註和型別推斷

型別標註寫在變數名稱後面：

```ts
let username: string = "Alice";
```

但如果 TypeScript 能夠推斷，就不必重複：

```ts
let username = "Alice"; // 推斷為 string
let age = 20;           // 推斷為 number
let active = true;      // 推斷為 boolean
```

推薦原則：

```ts
// 區域性變數：優先推斷
const price = 99;

// 函式引數：通常顯式標註
function double(value: number) {
  return value * 2;
}

// 公共函式返回值：可以顯式標註
function getUsername(): string {
  return "Alice";
}
```

型別推斷不等於型別永遠固定為初始值：

```ts
let status = "loading";
// status 被推斷為 string，而不是字面量 "loading"

status = "success"; // 合法
```

***

### 4、函式型別

#### 1. 引數型別

```ts
function greet(name: string) {
  console.log(name.toUpperCase());
}

greet("Alice"); // 正確
greet(42);      // 錯誤
```

即使引數沒有型別標註，TypeScript 仍然會檢查引數數量：

```ts
function add(a, b) {
  return a + b;
}

add(1); // 缺少一個引數
```

不過在嚴格模式下，`a` 和 `b` 會產生隱式 `any` 錯誤，因此應寫成：

```ts
function add(a: number, b: number): number {
  return a + b;
}
```

#### 2. 返回值型別

```ts
function getAge(): number {
  return 20;
}
```

返回值通常也能自動推斷：

```ts
function getAge() {
  return 20; // 推斷返回 number
}
```

顯式標註返回值的優點是能防止函式實現被意外修改：

```ts
function getAge(): number {
  return "20"; // 立即報錯
}
```

#### 3. 非同步函式

`async` 函式的返回型別是 `Promise<T>`：

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
// 錯誤：async 函式返回 Promise
```

#### 4. 上下文型別推斷

```ts
const names = ["Alice", "Bob", "Eve"];

names.forEach((name) => {
  console.log(name.toUpperCase());
});
```

雖然沒有給 `name` 新增型別標註，TypeScript 根據 `names` 是 `string[]`，推斷出回撥引數是 `string`。

這種根據程式碼所在位置推斷型別的方式稱為上下文型別推斷。

***

### 5、物件型別

可以直接描述物件的結構：

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

TypeScript 採用結構型別系統：只關心物件是否具有需要的屬性，而不關心它是如何建立的。

```ts
const employee = {
  name: "Bob",
  age: 30,
  department: "Development",
};

printUser(employee); // 合法
```

`employee` 多出一個 `department` 屬性沒有關係，因為它已經擁有 `name` 和 `age`。

#### 可選屬性

屬性名後新增 `?`：

```ts
type User = {
  name: string;
  nickname?: string;
};
```

下面兩種物件都合法：

```ts
const alice: User = {
  name: "Alice",
};

const bob: User = {
  name: "Bob",
  nickname: "Bobby",
};
```

讀取可選屬性時，它可能是 `undefined`：

```ts
function printNickname(user: User) {
  user.nickname.toUpperCase();
  // 錯誤：nickname 可能是 undefined
}
```

安全處理方式：

```ts
function printNickname(user: User) {
  if (user.nickname !== undefined) {
    console.log(user.nickname.toUpperCase());
  }
}
```

或者使用可選鏈和預設值：

```ts
console.log(user.nickname?.toUpperCase());
console.log(user.nickname?.toUpperCase() ?? "NO NICKNAME");
```

需要區分：

```ts
nickname?: string;
```

表示屬性可以不存在。

```ts
nickname: string | undefined;
```

表示屬性必須存在，但值可以是 `undefined`。

啟用 `exactOptionalPropertyTypes` 後，這種區別會更加嚴格。

***

### 6、聯合型別

聯合型別表示一個值可能屬於多個型別中的任意一個：

```ts
type ID = string | number;

function printId(id: ID) {
  console.log(id);
}

printId(100);
printId("USER-100");
```

#### 只能直接使用共有能力

```ts
function printId(id: string | number) {
  id.toUpperCase();
  // 錯誤：number 沒有 toUpperCase
}
```

必須先進行型別縮小：

```ts
function printId(id: string | number) {
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id.toFixed(0));
  }
}
```

對於陣列可以使用 `Array.isArray()`：

```ts
function welcome(value: string | string[]) {
  if (Array.isArray(value)) {
    console.log(value.join(", "));
  } else {
    console.log(value.toUpperCase());
  }
}
```

如果聯合型別中的所有成員都支援某個操作，可以直接使用：

```ts
function firstThree(value: string | number[]) {
  return value.slice(0, 3);
}
```

`string` 和陣列都有 `slice()`，因此不需要先縮小。

***

### 7、型別別名 `type`

型別別名可以給任意型別起一個名字：

```ts
type Point = {
  x: number;
  y: number;
};

type ID = string | number;

type Status = "loading" | "success" | "error";
```

使用型別別名能減少重複：

```ts
function printPoint(point: Point) {
  console.log(point.x, point.y);
}
```

但別名不會創造一個全新的執行階段型別：

```ts
type SanitizedString = string;

let value: SanitizedString = "ordinary string"; // 仍然合法
```

`SanitizedString` 本質上仍然只是 `string` 的另一個名字。

***

### 8、介面 `interface`

介面專門用於描述物件結構：

```ts
interface User {
  name: string;
  age: number;
}

function printUser(user: User) {
  console.log(user.name);
}
```

#### `type` 和 `interface` 的區別

兩者描述普通物件時非常相似：

```ts
type UserType = {
  name: string;
};

interface UserInterface {
  name: string;
}
```

主要區別：

| **能力**          | **`interface`** | **`type`** |
| --------------- | --------------- | ---------- |
| 描述物件            | 支援              | 支援         |
| 描述聯合型別          | 不支援             | 支援         |
| 描述基本型別別名        | 不支援             | 支援         |
| 使用 `extends` 繼承 | 支援              | 可用交叉型別實現   |
| 同名宣告合併          | 支援              | 不支援        |

介面繼承：

```ts
interface Animal {
  name: string;
}

interface Bear extends Animal {
  honey: boolean;
}
```

型別交叉：

```ts
type Animal = {
  name: string;
};

type Bear = Animal & {
  honey: boolean;
};
```

介面可以宣告合併：

```ts
interface WindowConfig {
  title: string;
}

interface WindowConfig {
  width: number;
}

// 最終同時具有 title 和 width
```

實用選擇原則：

* 普通、可擴充套件的物件模型：優先考慮 `interface`。
* 聯合型別、元組、對映型別等組合型別：使用 `type`。
* 團隊已有統一風格：遵循專案約定。
* 不要為了選擇它們而過度糾結。

***

### 9、型別斷言

型別斷言表示：“我比編譯器更清楚這個值的型別。”

```ts
const canvas = document.getElementById(
  "main-canvas",
) as HTMLCanvasElement;
```

也有另一種寫法：

```ts
const canvas =
  <HTMLCanvasElement>document.getElementById("main-canvas");
```

但尖括號寫法不能在 `.tsx` 中正常使用，因此通常統一使用 `as`。

#### 斷言不是型別轉換

```ts
const value = "123" as unknown as number;
```

執行階段的 `value` 仍然是字串，不會變成數字。

真正轉換資料應使用：

```ts
const value = Number("123");
```

也就是說：

* `as number`：隻影響編譯器。
* `Number(value)`：真正影響執行階段資料。

避免為了消除錯誤而濫用雙重斷言：

```ts
value as unknown as User;
```

這種寫法通常意味著型別設計或執行階段校驗存在問題。

***

### 10、字面量型別

字面量型別表示某一個具體值：

```ts
let direction: "left";

direction = "left";  // 正確
direction = "right"; // 錯誤
```

單獨使用意義不大，但與聯合型別結合非常實用：

```ts
type Direction = "left" | "right" | "center";

function align(direction: Direction) {
  // ...
}

align("left");
align("center");
align("top"); // 錯誤
```

也可以使用數字字面量：

```ts
function compare(a: string, b: string): -1 | 0 | 1 {
  return a === b ? 0 : a > b ? 1 : -1;
}
```

字面量聯合型別經常比列舉更加輕量：

```ts
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type Theme = "light" | "dark";
type RequestState = "idle" | "loading" | "success" | "error";
```

***

### 11、字面量推斷和 `as const`

注意下面的物件：

```ts
const request = {
  url: "/users",
  method: "GET",
};
```

雖然變數使用了 `const`，但物件屬性仍然可以修改：

```ts
request.method = "DELETE";
```

所以 TypeScript 把 `request.method` 推斷為 `string`，而不是字面量 `"GET"`。

如果函式只接受固定方法：

```ts
function send(method: "GET" | "POST") {}

send(request.method); // 可能報錯：request.method 是 string
```

可以使用 `as const`：

```ts
const request = {
  url: "/users",
  method: "GET",
} as const;
```

此時大致推斷為：

```ts
{
  readonly url: "/users";
  readonly method: "GET";
}
```

注意：

> `const` 防止變數重新賦值；`as const` 讓物件屬性在型別層面成為只讀字面量。

#### 延伸：`satisfies`

如果既想檢查物件是否符合某種結構，又想保留精確推斷，可以使用 `satisfies`：

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

與 `as RequestConfig` 相比，`satisfies` 更側重“檢查”，不會簡單地用目標型別覆蓋原有推斷。

***

### 12、`null` 和 `undefined`

它們都表示“缺少值”，但含義通常不同：

* `undefined`：尚未提供、屬性不存在。
* `null`：顯式表示沒有值。

開啟 `strictNullChecks` 後，必須顯式處理：

```ts
function printName(name: string | null) {
  if (name === null) {
    console.log("No name");
  } else {
    console.log(name.toUpperCase());
  }
}
```

也可以使用空值合併：

```ts
function displayName(name: string | null | undefined) {
  return name ?? "Anonymous";
}
```

`??` 與 `||` 不完全相同：

```ts
0 || 10; // 10
0 ?? 10; // 0

"" || "default"; // "default"
"" ?? "default"; // ""
```

`??` 只把 `null` 和 `undefined` 當成缺少值。

#### 非空斷言 `!`

```ts
const element = document.getElementById("app");

element!.textContent = "Hello";
```

`!` 告訴 TypeScript：“它絕對不是 `null` 或 `undefined`。”

但它不會新增執行階段檢查。如果元素不存在，程式仍然會崩潰。更安全的寫法是：

```ts
const element = document.getElementById("app");

if (element !== null) {
  element.textContent = "Hello";
}
```

只在能由程式邏輯嚴格保證非空時使用 `!`。

***

### 13、列舉 `enum`

```ts
enum Direction {
  Up,
  Down,
  Left,
  Right,
}
```

與大多數 TypeScript 型別不同，`enum` 通常會生成執行階段程式碼。官方文件建議知道它的存在，但不要急著使用。

很多場景可以使用字面量聯合代替：

```ts
type Direction = "up" | "down" | "left" | "right";
```

也可以使用常量物件：

```ts
const Direction = {
  Up: "up",
  Down: "down",
  Left: "left",
  Right: "right",
} as const;

type Direction = typeof Direction[keyof typeof Direction];
```

初學階段建議：

* 只需要限制字串取值：使用字面量聯合。
* 必須提供執行階段物件或專案已有約定：再考慮 `enum`。

***

### 14、`bigint` 和 `symbol`

#### `bigint`

用於表示超過普通 `number` 安全整數範圍的大整數：

```ts
const amount1: bigint = BigInt(100);
const amount2: bigint = 100n;
```

不能直接混合 `number` 和 `bigint`：

```ts
1n + 1;  // 錯誤
1n + 1n; // 正確
```

使用 `bigint` 字面量時，編譯目標通常需要支援 ES2020 或更高版本。

#### `symbol`

每個 `Symbol()` 都是唯一值：

```ts
const first = Symbol("name");
const second = Symbol("name");

console.log(first === second); // false
```

即使描述文字相同，它們也不是同一個值。`symbol` 常用於建立不會發生命名衝突的物件鍵。

***

### 15、綜合範例

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

這個例子同時使用了：

* 物件型別
* `interface`
* 聯合型別
* 字面量型別
* 可選屬性
* 可選鏈 `?.`
* 空值合併 `??`
* 返回值型別
* `satisfies`

### 16、速查表

| **寫法**             | **含義**     |
| ------------------ | ---------- |
| `string`           | 字串        |
| `number`           | 數字         |
| `boolean`          | 布林值        |
| `string[]`         | 字串陣列      |
| `Array<string>`    | 字串陣列      |
| `name?: string`    | 可選屬性       |
| `string \| number` | 聯合型別       |
| `"GET" \| "POST"`  | 字面量聯合      |
| `type A = ...`     | 型別別名       |
| `interface A {}`   | 物件介面       |
| `value as T`       | 型別斷言       |
| `value!`           | 非空斷言       |
| `as const`         | 保留字面量並設為只讀 |
| `unknown`          | 未知型別，使用前檢查 |
| `any`              | 關閉型別檢查     |

最值得牢牢記住的三點是：

1. **優先利用型別推斷，不必為每個變數手寫型別。**
2. **聯合型別只能直接使用所有成員共有的能力，其他操作需要先縮小型別。**
3. **型別斷言和非空斷言不會進行執行階段檢查，不能把它們當作資料轉換或安全驗證。**

下一章是 [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)，會系統講解如何透過 `typeof`、判空、`in`、`instanceof` 和控制流分析縮小聯合型別。
