---
translation_id: javascript-basics
description: "JavaScript 的動態型別、作用域、函式、原型、模組和非同步程式設計。"
---

# JavaScript 基礎知識

## 一、**JavaScript 的執行階段世界**

### 1.1、 JavaScript 的動態型別

JavaScript 的“動態型別”是指：**變數本身不固定型別，型別由執行階段變數當前存放的值決定。**

```js
let value = 10;       // 當前是 number
value = "hello";       // 現在是 string
value = true;         // 現在是 boolean
```

同一個變數可以先後儲存不同型別的值，不需要提前宣告型別。可以用 `typeof` 在執行階段檢視：

```js
console.log(typeof 10);      // "number"
console.log(typeof "hello");  // "string"
console.log(typeof true);    // "boolean"
```

需要注意，“動態型別”不等於“沒有型別”。JavaScript 中的**值仍然有明確型別**，例如 `number`、`string`、`boolean`、`object` 等；只是變數和型別之間沒有永久繫結。

這很靈活，但也可能讓錯誤在執行階段才暴露：

```js
function add(a, b) {
  return a + b;
}

add(1, 2);     // 3
add("1", 2);   // "12"，因為發生了型別轉換
```

因此實際開發中常用 TypeScript，在 JavaScript 之上增加靜態型別檢查。



### 1.2、JavaScript 的八種值型別

JavaScript 共有七種基本型別和一種物件型別。

* 基本型別：undefined、null、boolean、number、bigint、string、symbol
* 物件型別：object

下面這些物件的型別都屬於object：

```js
{}
[]
new Date()

new Map()
new Set()
```

但是函式比較特殊：

```js
typeof function test() {} // "function"
```

從語言模型上說，函式仍然屬於物件；但 `typeof` 專門為函式返回 `"function"`。

常見的 `typeof` 結果：

```js
typeof 123          // "number"
typeof "hello"      // "string"
typeof true         // "boolean"
typeof undefined    // "undefined"
typeof 10n          // "bigint"
typeof Symbol()     // "symbol"
typeof {}           // "object"
typeof []           // "object"
typeof function(){} // "function"
```

一個歷史遺留陷阱：typeof null 的返回值是 "object"，這不代表 `null` 真的是物件。它是 JavaScript 早期設計遺留下來的行為。

因此，判斷 `null` 通常直接寫：value === null。

判斷陣列則使用：Array.isArray(value)，不要使用：typeof value === "array" ，這個判斷條件永遠不會成立。



（1）、undefined和null的區別

其中，undefined和null 都可以表達“沒有值”，但是他們的語義不同。

undefined：通常表示“尚未提供”或“尚未賦值”。具體參考下面的程式碼範例：

```js
let result;
console.log(result); // undefined

function greet(name) {
  console.log(name);
}

greet(); // undefined
```

null：通常是開發者主動設定的空值：

```js
const selectedUser = null;
```

總結來說，可以理解為：

* undefined：這裡暫時沒有值，或者值沒有被提供。
* null：這裡被明確設定為空。



### 1.3、const和let的區別

`const` 和 `let` 都用來宣告變數，核心區別是：**變數能否被重新賦值**。

```js
let age = 18;
age = 19; // 可以

const name = "小明";
name = "小红"; // 報錯：不能重新賦值
```

但 `const` 宣告的物件或陣列，其**內容仍然可以修改**：

```js
const user = { name: "小明" };
user.name = "小红"; // 可以

const numbers = [1, 2];
numbers.push(3); // 可以
```

不能把整個變數換成另一個物件或陣列：

```js
user = { name: "小刚" }; // 報錯
numbers = [4, 5];        // 報錯
```

簡單理解：

* `let`：變數之後需要重新賦值時使用。
* `const`：變數不會重新賦值時使用。

通常優先使用 `const`，確定需要重新賦值時再使用 `let`。

兩者還有一些共同點：

* 都是塊級作用域。
* 都不能在同一作用域內重複宣告。
* 宣告前訪問都會報錯。
* `const` 宣告時必須立即賦值：

```js
let value;    // 可以
const value;  // 報錯
```



### 1.4、===和==的區別

核心區別：

* `==`：寬鬆相等，比較前可能自動轉換型別。
* `===`：嚴格相等，不轉換型別，同時比較型別和值。

```js
5 == "5"   // true，字串 "5" 被轉換成數字
5 === "5"  // false，型別不同
```

更多例子：

```js
0 == false        // true
0 === false       // false

"" == false       // true
"" === false      // false

null == undefined   // true
null === undefined  // false
```

物件和陣列比較的是“引用是否為同一個”：

```js
[1, 2] === [1, 2] // false，兩個不同的陣列物件

const a = [1, 2];
const b = a;

a === b // true，指向同一個陣列
```

實際開發中，建議預設使用 `===` 和 `!==`，結果更明確，也能避免隱式型別轉換帶來的意外。

```js
if (age === 18) {
  // ...
}
```

只有確實需要寬鬆比較規則，並且清楚型別轉換結果時，才考慮使用 `==`。



## 二、作用域與閉包

### 2.1、作用域是什麼

作用域決定了一個變數可以在哪些位置被訪問。

```js
const appName = "Demo";

function start() {
  const version = "1.0";

  console.log(appName);
  console.log(version);
}

start();

console.log(appName);
// console.log(version); // ReferenceError
```

這裡：

* `appName` 位於外層作用域，內部函式可以訪問它。
* `version` 位於 `start` 的函式作用域，函式外部不能訪問它。

可以畫成：

```text
全域性作用域
├── appName
└── start
    └── 函式作用域
        └── version
```

當 JavaScript 查詢一個變數時，會從當前位置開始逐層向外查詢：

```text
當前作用域 → 外層作用域 → 更外層作用域 → 全域性作用域
```

這個查詢關係稱為**作用域鏈**。



（1）、JavaScript 中常見的作用域

* 全域性作用域，在普通指令碼的最外層宣告：

```js
const appName = "My App";
```

真實專案通常會使用模組，因此每個模組擁有自己的頂層作用域，而不是讓所有變數真正進入全域性環境。

* 函式作用域，函式引數和函式內部宣告的變數屬於函式：

```js
function calculate(price, count) {
  const total = price * count;
  return total;
}
```

這裡的 `price`、`count` 和 `total` 都只能在 `calculate` 內部訪問。

* 塊級作用域，由一對花括號形成，例如：

```js
if (true) {
  const message = "hello";
  let count = 1;
}

// message 和 count 在這裡不可訪問
```



（2）、變數遮蔽

內層作用域可以宣告與外層同名的變數：

```js
const config = "global config";

function initialize() {
  const config = "local config";
  console.log(config);
}

initialize();
console.log(config);
```

輸出：

```text
local config
global config
```

函式內部的 `config` 遮蔽了外層的 `config`。這叫作變數遮蔽，也稱 shadowing。



（3）、`var`、`let` 和 `const` 的作用域差異

現代專案主要使用 `const` 和 `let`，但舊專案、編譯輸出以及依賴程式碼中仍可能出現 `var`。

`let` 和 `const` 是塊級作用域

```js
if (true) {
  let count = 1;
  const name = "Alice";
}

// 這裡不能訪問 count 和 name
```

`var` 是函式作用域

```js
function test() {
  if (true) {
    var count = 1;
  }

  console.log(count);
}

test();
```

輸出結果：1

`if` 的花括號沒有限制 `var`。在這個例子中，`count` 屬於整個 `test` 函式。

如果沒有函式包圍它：

```js
if (true) {
  var value = 10;
}

console.log(value); // 10
```

這也是為什麼現代程式碼通常避免使用 `var`：它的作用域邊界不夠直觀。



### 2.2、變數提升

JavaScript 在執行一個作用域之前，會先處理該作用域中的宣告。

因此某些宣告看起來可以在程式碼出現之前使用。這種現象通常稱為**提升**，即 hoisting。

不過，不同宣告的提升行為不一樣。

（1）、函式宣告的提升

使用函式宣告時，可以在宣告之前呼叫：

```js
greet();

function greet() {
  console.log("hello");
}
```

可以將其粗略理解成：進入作用域時，JavaScript 已經建立好了 `greet` 函式。

這種行為經常被用於把主要邏輯放在檔案上方，把輔助函式放在檔案下方：

```js
export function processData(data) {
  const normalized = normalize(data);
  return validate(normalized);
}

function normalize(data) {
  return data.trim();
}

function validate(data) {
  return data.length > 0;
}
```

即使輔助函式寫在後面，前面的 `processData` 仍然可以呼叫它們。

（2）、函式表示式不會像函式宣告一樣工作

下面的程式碼會報錯：

```js
greet();

const greet = function () {
  console.log("hello");
};
```

箭頭函式也是如此：

```js
greet();

const greet = () => {
  console.log("hello");
};
```

因為這裡提升的是變數宣告，而不是把函式值提前賦給變數。

這兩個寫法的本質都是：

```js
const greet = 某个函数值;
```

只有執行到賦值語句之後，`greet` 才真正儲存了函式。

所以需要寫成：

```js
const greet = () => {
  console.log("hello");
};

greet();
```



### 2.3、閉包是什麼

先看一個函式返回函式的例子：

```js
function createCounter() {
  let count = 0;

  return function increment() {
    count += 1;
    return count;
  };
}

const counter = createCounter();

console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3
```

按照普通直覺，`createCounter()` 已經執行完了，它的區域性變數 `count` 似乎也應該消失。

但是返回的 `increment` 函式仍然引用了 `count`，因此 `count` 會繼續存在。

這就是閉包：函式 + 函式定義時能夠訪問的外層詞法環境。

可以想象為：

```text
counter
  │
  ▼
increment 函式
  │
  └── 引用 createCounter 作用域中的 count
```

只要 `counter` 還可以被訪問，這個閉包及其需要的外層變數就仍然可以被訪問。

（1）、每次函式呼叫都會產生新的詞法環境

```js
function createCounter() {
  let count = 0;

  return function () {
    count += 1;
    return count;
  };
}

const first = createCounter();
const second = createCounter();

console.log(first());  // 1
console.log(first());  // 2
console.log(second()); // 1
```

`first` 和 `second` 並不共享 `count`。

因為 `createCounter()` 被呼叫了兩次，每次都會產生一個新的區域性環境：

```text
first  → count: 2
second → count: 1
```

也就是說，每次呼叫都產生獨立狀態。

（2）、`var` 在迴圈中的經典閉包問題

```js
const functions = [];

for (var i = 0; i < 3; i++) {
  functions.push(function () {
    console.log(i);
  });
}

functions[0]();
functions[1]();
functions[2]();
```

輸出的結果是3，3，3

原因是：

* `var` 是函式作用域，不是塊級作用域。
* 三個函式閉包引用的是同一個 `i`。
* 迴圈結束後，這個 `i` 已經變成 `3`。
* 呼叫函式時，它們讀取到的都是當前的 `i`，不是建立函式時的快照。

使用 `let`：

```js
const functions = [];

for (let i = 0; i < 3; i++) {
  functions.push(function () {
    console.log(i);
  });
}
```

輸出的結果是：0，1，2

在 `for` 迴圈中使用 `let` 時，JavaScript 會為每次迭代建立對應的迴圈變數繫結。



## 三、函式

### 3.1、建立函式的方式

（1）、函式宣告

```js
function add(a, b) {
  return a + b;
}
```

（2）、函式表示式

```js
const add = function (a, b) {
  return a + b;
};
```

這裡先建立了一個函式值，再把它賦給變數 `add`。

因為 `add` 是 `const` 變數，所以不能在賦值前呼叫：

```js
add(2, 3); // ReferenceError

const add = function (a, b) {
  return a + b;
};
```

（3）、箭頭函式

```js
const add = (a, b) => {
  return a + b;
};
```

如果函式體只有一個表示式，可以省略花括號和 `return`：

```js
const add = (a, b) => a + b;
```

當只有一個引數時，可以省略引數括號：

```js
const double = value => value * 2;
```

沒有引數或有多個引數時，必須保留括號：

```js
const getTime = () => Date.now();

const add = (a, b) => a + b;
```



### 3.2、剩餘引數 `...args`

剩餘引數可以把多餘的實參收集到一個陣列中：

```js
function sum(...numbers) {
  let total = 0;

  for (const number of numbers) {
    total += number;
  }

  return total;
}

sum(1, 2, 3);       // 6
sum(1, 2, 3, 4, 5); // 15
```

`numbers` 是一個真正的陣列：

```js
Array.isArray(numbers) // true
```

剩餘引數也可以和普通引數一起使用：

```js
function log(level, ...messages) {
  console.log(level, messages);
}

log("info", "Server started", "Port:", 3000);
```

level和messages接收到的引數，分別如下：

```text
level    → "info"
messages → ["Server started", "Port:", 3000]
```

剩餘引數必須是最後一個引數。



### 3.3、函式沒有顯式返回值時返回 `undefined`

```js
function greet() {
  console.log("Hello");
}

const result = greet();

console.log(result); // undefined
```



### 3.4、回撥函式

作為引數傳給另一個函式的函式，通常稱為回撥函式。

```js
function execute(callback) {
  callback();
}

execute(() => {
  console.log("Executed");
});
```

`execute` 是接收函式，箭頭函式是回撥函式。



## 四、this的指向

`this` 是 JavaScript 中最容易被誤解的機制之一。

先記住重要的一句話：普通函式的 this 通常由呼叫方式決定，箭頭函式的this是由定義位置決定。

### 4.1、普通函式的this

考慮一個物件：

```js
const user = {
  name: "Alice",

  introduce() {
    console.log(this.name);
  }
};

user.introduce(); // "Alice"
```

呼叫點左側是 `user`，因此這次呼叫中的：

```js
this === user
```

可以近似理解成：

```js
introduce.call(user);
```

但 `introduce` 函式並不永久屬於 `user`。

```js
const anotherUser = {
  name: "Bob",
  introduce: user.introduce
};

anotherUser.introduce(); // "Bob"
```

同一個函式被不同物件呼叫時，this的指向也是不一樣的：

```text
user.introduce()        → this 是 user
anotherUser.introduce() → this 是 anotherUser
```

### 4.2、箭頭函式的this

箭頭函式里最關鍵的一句話是：

> 箭頭函式沒有自己的 `this`，它使用定義時所在外層作用域的 `this`。

```js
function createArrow() {
  return () => {
    console.log(this.name);
  };
}

const user = {
  name: "小明",
  createArrow
};

const fn = user.createArrow();

fn(); // 小明
```

執行過程是：

1. 呼叫 `user.createArrow()`
2. `createArrow` 是普通函式，因此它的 `this` 是 `user`
3. 箭頭函式建立時，捕獲了 `createArrow` 中的 `this`
4. 即使後來單獨執行 `fn()`，它仍然使用之前捕獲的 `user`



（1）、物件方法中使用箭頭函式的坑

```js
const user = {
  name: "小明",

  sayName: () => {
    console.log(this.name);
  }
};

user.sayName();
```

物件字面量 `{}` 不會建立一個新的 `this` 作用域。這個箭頭函式會捕獲物件外層的 `this`，而不是捕獲 `user`。

可以近似理解為：

```js
const outerThis = this;

const user = {
  name: "小明",

  sayName: () => {
    console.log(outerThis.name);
  }
};
```

正確寫法應該使用普通方法：

```js
const user = {
  name: "小明",

  sayName() {
    console.log(this.name);
  }
};

user.sayName(); // 小明
```

或者：

```js
const user = {
  name: "小明",

  sayName: function () {
    console.log(this.name);
  }
};
```



（2）、箭頭函式適合巢狀回撥

箭頭函式最初解決的一個重要問題，就是回撥函式會丟失外層 `this`。

普通函式回撥的問題，參見如下的程式碼：

```js
const user = {
  name: "小明",

  introduce() {
    setTimeout(function () {
      console.log(this.name);
    }, 1000);
  }
};

user.introduce();
```

呼叫 `user.introduce()` 時，`introduce` 裡的 `this` 是 `user`。

但傳給 `setTimeout` 的函式是另外一個普通函式。它被定時器呼叫時，並不是透過：

```js
user.someFunction();
```

呼叫，所以其 `this` 不再是 `user`。

但是使用箭頭函式就可以解決這個問題：

```js
const user = {
  name: "小明",

  introduce() {
    setTimeout(() => {
      console.log(this.name);
    }, 1000);
  }
};

user.introduce(); // 1 秒後輸出“小明”
```

這裡：

1. `introduce` 是普通方法
2. `user.introduce()` 使 `introduce` 中的 `this` 成為 `user`
3. 定時器箭頭函式捕獲 `introduce` 的 `this`
4. 因此回撥中仍然可以訪問 `user`

在沒有箭頭函式的時候，過去經常這樣寫：

```js
const user = {
  name: "小明",

  introduce() {
    const self = this;

    setTimeout(function () {
      console.log(self.name);
    }, 1000);
  }
};
```



## 五、原型、原型鏈和class

JavaScript 是一門“基於原型”的語言。即使使用 `class`，底層依然主要依靠原型和原型鏈完成屬性共享、方法複用與繼承。

先用一句話概括：

> 每個普通物件都可以關聯另一個物件作為自己的原型；訪問物件屬性時，如果物件本身沒有，JavaScript 就沿著原型繼續查詢，直到找到屬性或走到 `null`。這條查詢路徑就是原型鏈。

### 5.1、原型是什麼？

每個普通物件通常都有一個內部原型連結。

```js
const user = {
  name: "Alice"
};
```

可以近似畫成：

```text
user
├── 自身屬性：name
└── [[Prototype]] ──→ Object.prototype
                         ├── toString
                         ├── valueOf
                         ├── hasOwnProperty
                         └── ...
```

`[[Prototype]]` 是規範中使用的內部概念，不是普通程式碼直接使用的屬性名。

可以透過：

```js
Object.getPrototypeOf(user)
```

讀取物件的原型：

```js
Object.getPrototypeOf(user) === Object.prototype
// true
```

#### (1)、屬性的查詢過程

當執行：

```js
user.name
```

JavaScript 會：

1. 檢查 `user` 自己是否有 `name`
2. 找到後直接返回 `"Alice"`

當執行：

```js
user.toString
```

JavaScript 會：

1. 檢查 `user` 自己是否有 `toString`
2. 沒找到
3. 前往 `user` 的原型
4. 在 `Object.prototype` 上找到 `toString`
5. 返回這個函式

這就是原型鏈屬性查詢。

如果當前原型也沒有，則繼續向上查詢，直到遇到：

```js
null
```

完整路徑大致是：

```text
當前物件
   ↓
當前物件的原型
   ↓
原型的原型
   ↓
...
   ↓
null
```

到達 `null` 後仍然沒找到，就返回：

```js
undefined
```



#### (2)、`in` 和 `Object.hasOwn()` 的區別

請先看下面的這段範例程式碼：

```js
const parent = {
  type: "父对象"
};

const child = Object.create(parent);
child.name = "子对象";

console.log("name" in child); // true
console.log("type" in child); // true
console.log("toString" in child); // true

console.log(Object.hasOwn(child, "name")); // true
console.log(Object.hasOwn(child, "type")); // false
console.log(Object.hasOwn(child, "toString")); // false
```

* 使用 `in` 會檢查：物件自身、整條原型鏈。
* 使用 `Object.hasOwn()`只檢查物件自身。

#### (3)、屬性遮蔽

物件可以定義一個與原型屬性同名的自身屬性：

```js
const user = {
  name: "Alice",

  toString() {
    return this.name;
  }
};

user.toString(); // "Alice"
```

查詢 `toString` 時：

1. 先在 `user` 自身找到
2. 不再繼續查詢 `Object.prototype.toString`

這叫作屬性遮蔽。

如果刪除自身屬性：

```js
delete user.toString;
```

再次訪問：

```js
user.toString
```

就會找到原型上的版本。

#### (4)、如何獲取物件的原型？

推薦使用：

```js
Object.getPrototypeOf(user);
```

例如：

```js
const user = {};

console.log(
  Object.getPrototypeOf(user) === Object.prototype
); // true
```

也能透過：

```js
user.__proto__
```

讀取，但 `__proto__` 是歷史遺留訪問方式，不推薦在正式程式碼中依賴它。

推薦寫法：

```js
Object.getPrototypeOf(obj);
Object.setPrototypeOf(obj, prototype);
```

不過頻繁使用 `Object.setPrototypeOf()` 修改現有物件的原型，可能影響 JavaScript 引擎最佳化。設計物件結構時，通常應當在建立階段確定原型。



### 5.2、手動建立原型關係

#### (1)、`Object.create`

**`Object.create()`** 的作用是：**建立一個新物件，並將新物件的 `__proto__`（內部原型指標）指向傳入的引數物件**。

參見下面的在這段程式碼：

```js
const animal = {
  breathe() {
    console.log("Breathing");
  }
};

const dog = Object.create(animal);

dog.name = "Lucky";
dog.bark = function () {
  console.log("Woof");
};
```

原型關係：

```text
dog
├── name
├── bark
└── [[Prototype]] ──→ animal
                       └── breathe
```



### 5.3、原型鏈

#### (1)、多層原型鏈

詳細參見下面這段程式碼：

```js
function User(name) {
  this.name = name;
}

User.prototype.introduce = function () {
  console.log(this.name);
};

const alice = new User("Alice");
```

原型鏈大致是：

```text
alice
  ↓ [[Prototype]]
User.prototype
  ↓ [[Prototype]]
Object.prototype
  ↓ [[Prototype]]
null
```

讀取：alice.name ，在 `alice` 自身找到。

讀取：alice.introduce，在 `User.prototype` 找到。

讀取：alice.toString，在：

```text
alice             沒找到
User.prototype    沒找到
Object.prototype  找到
```

#### (2)、陣列的原型鏈

```js
const items = [1, 2, 3];
```

`items` 自己並沒有儲存一份 `map`：

```js
Object.hasOwn(items, "map"); // false
```

但可以呼叫：

```js
items.map(item => item * 2);
```

因為原型鏈大致是：

```text
items
  ↓
Array.prototype
  ├── map
  ├── filter
  ├── reduce
  ├── push
  └── ...
  ↓
Object.prototype
  ├── toString
  └── ...
  ↓
null
```

驗證：

```js
Object.getPrototypeOf(items) === Array.prototype
  // true
```

這解釋了為什麼所有陣列都能共享陣列方法，而不需要每個陣列單獨儲存一份 `map`。

#### (3)、函式的原型鏈

```js
function greet() {
}
```

`greet` 本身是一個函式物件，因此：

```js
Object.getPrototypeOf(greet) === Function.prototype
   // true
```

這就是它為什麼能呼叫：

```js
greet.call(...)
greet.apply(...)
greet.bind(...)
```

因為這些方法通常來自：

```js
Function.prototype
```

關係大致是：

```text
greet 函式物件
  ↓
Function.prototype
  ↓
Object.prototype
  ↓
null
```

#### (4)、instanceof檢查原型鏈

```js
class Animal {
}

class Dog extends Animal {
}

const dog = new Dog();
```

結果：

```js
dog instanceof Dog;    // true
dog instanceof Animal; // true
dog instanceof Object; // true
```

`instanceof` 的核心問題是：建構函式的 prototype 是否出現在物件的原型鏈上？

例如：dog instanceof Animal

近似檢查：Animal.prototype 是否存在於 dog 的原型鏈？

因為：

```text
dog
↓
Dog.prototype
↓
Animal.prototype
```

所以結果為 `true`。



### 5.4、class

#### (1)、基本類定義

參見如下的範例程式碼：

```js
class User {
  //
负责初始化实例自身属性
  constructor(name) {
    this.name = name;
  }

  //introduce函式會被定義在：User.prototype
  introduce() {
    console.log(`I am ${this.name}`);
  }
}

const alice = new User("Alice");

alice.introduce();
```

可以驗證：

```js
Object.hasOwn(alice, "name"); // true

Object.hasOwn(alice, "introduce"); // false

Object.hasOwn(User.prototype, "introduce"); // true
```

所以：

```js
alice.introduce === User.prototype.introduce
  // true
```



#### (2)、extends

詳細參見如下的程式碼：

```js
class Animal {
  constructor(name) {
    this.name = name;
  }

  introduce() {
    console.log(`I am ${this.name}`);
  }

  move() {
    console.log(`${this.name} is moving`);
  }
}

class Dog extends Animal {
  bark() {
    console.log(`${this.name}: Woof`);
  }
}

const dog = new Dog("Lucky");

dog.introduce();
dog.move();
dog.bark();
```

`Dog` 沒有定義 `introduce` 和 `move`，但實例可以透過原型鏈找到它們。

原型關係大致是：

```text
dog
  ↓
Dog.prototype
  ├── bark
  ↓
Animal.prototype
  ├── introduce
  ├── move
  ↓
Object.prototype
  ↓
null
```

#### (3)、子類建構函式與super()

```js
class Dog extends Animal {
  constructor(name, breed) {
    super(name);
    this.breed = breed;
  }
}
```

子類建構函式必須在使用 `this` 前呼叫：

```js
super(...)
```

`super(name)` 呼叫父類建構函式，並讓父類初始化當前這個實例。

注意，它不是建立一個單獨的 `Animal` 實例再塞進 `Dog`。

`Dog` 實例仍然只有一個：

```text
同一個 dog 例項
├── name 由 Animal 建構函式初始化
└── breed 由 Dog 建構函式初始化
```

#### (4)、Getter和Setter

Getter函式的範例程式碼如下：

```js
class Rectangle {
  constructor(width, height) {
    this.width = width;
    this.height = height;
  }

  get area() {
    return this.width * this.height;
  }
}

const rectangle = new Rectangle(4, 5);

console.log(rectangle.area); // 20
```

訪問形式看起來是屬性：rectangle.area，但背後會執行 getter 函式。

不要寫成：rectangle.area()，Getter 適合計算派生屬性。



Setter函式的範例程式碼如下：

```js
class User {
  constructor(name) {
    this._name = name;
  }

  get name() {
    return this._name;
  }

  set name(value) {
    this._name = value.trim();
  }
}

const user = new User("Alice");

user.name = "  Bob  ";

console.log(user.name); // "Bob"
```

賦值：user.name = "Bob";   會呼叫 setter。

讀取：user.name，會呼叫 getter。

`_name` 只是命名約定，並不是真正私有。



## 六、陣列、集合、迭代器

### 6.1、陣列的基本型別

```js
const users = ["Alice", "Bob", "Charlie"];

// 陣列透過數字索引訪問元素：
users[0]; // "Alice"
users[1]; // "Bob"
users[2]; // "Charlie"

// 陣列也是物件：
typeof users // "object"

// 判斷一個值是否是陣列，應使用 Array.isArray
Array.isArray(users) // true
```

### 6.2、會修改原陣列的方法

#### (1)、 `push` 和 `pop`

push：在陣列尾部新增元素，並返回新長度：

```js
const items = ["a", "b"];
// 注意 push 返回的是長度，不是陣列
const length = items.push("c");

console.log(items);  // ["a", "b", "c"]
console.log(length); // 3
```

pop：刪除並返回最後一個元素：

```js
const items = ["a", "b", "c"];

const last = items.pop();

console.log(last);  // "c"
console.log(items); // ["a", "b"]
```

#### (2)、`unshift` 和 `shift`

unshift：向陣列開頭新增元素：

```js
const items = ["b", "c"];

items.unshift("a");

console.log(items); // ["a", "b", "c"]
```

shift：刪除並返回第一個元素：

```js
const items = ["a", "b", "c"];

const first = items.shift();

console.log(first); // "a"
console.log(items); // ["b", "c"]
```

因為開頭的其他元素通常需要重新調整索引，頻繁使用 `shift` 和 `unshift` 處理大陣列可能比尾部操作成本更高

#### (3)、`splice`

`splice` 可以刪除、插入或替換元素，並且會修改原陣列。

```js
array.splice(startIndex, deleteCount, ...newItems)
```

刪除：

```js
const items = ["a", "b", "c", "d"];

const removed = items.splice(1, 2);

console.log(removed); // ["b", "c"]
console.log(items);   // ["a", "d"]
```

插入：

```js
const items = ["a", "d"];

items.splice(1, 0, "b", "c");

console.log(items); // ["a", "b", "c", "d"]
```

替換：

```js
const items = ["a", "b", "c"];

items.splice(1, 1, "B");

console.log(items); // ["a", "B", "c"]
```

#### (4)、 `sort`

`sort` 會修改原陣列：

```js
const numbers = [3, 1, 2];

const result = numbers.sort();

console.log(numbers); // [1, 2, 3]
console.log(result === numbers); // true
```

數字排序應提供比較函式：

```js
numbers.sort((a, b) => a - b);
```

升序：

```js
(a, b) => a - b
```

降序：

```js
(a, b) => b - a
```

### 6.3、返回新陣列的方法

#### (1)、 `slice`

`slice` 擷取一部分元素，返回新陣列，不修改原陣列。

```js
const items = ["a", "b", "c", "d"];

const selected = items.slice(1, 3);

console.log(selected); // ["b", "c"]
console.log(items);    // ["a", "b", "c", "d"]
```

範圍是：包含開始索引，不包含結束索引。

#### (2)、 `concat`

```js
const first = [1, 2];
const second = [3, 4];

const combined = first.concat(second);

console.log(combined); // [1, 2, 3, 4]
```

也可以使用展開語法：

```js
const combined = [
  ...first,
  ...second
];
```

兩種方式都不會修改原陣列。



### 6.4、轉換陣列

#### (1)、 `map`

`map` 把每個元素轉換成一個新值，並返回新陣列。

```js
const numbers = [1, 2, 3];

const doubled = numbers.map(number => number * 2);

console.log(doubled); // [2, 4, 6]
```

轉換物件：

```js
const names = users.map(user => user.name);
```

轉換結構：

```js
const options = users.map(user => ({
  label: user.name,
  value: user.id
}));
```

`map` 回撥的返回值非常重要。

```js
// 錯誤範例
const names = users.map(user => {
  user.name;
});

// 因為沒有 return，結果是：
[undefined, undefined, ...]

// 正確範例
const names = users.map(user => {
  return user.name;
});
// 或者：
const names = users.map(user => user.name);
```

#### (2)、 `filter`

`filter` 保留回撥返回真值的元素：

```js
const activeUsers = users.filter(user => user.active);
```

原陣列不變，返回新陣列。

過濾空值的常見寫法：

```js
const values = [0, 1, null, 2, undefined, 3];

const result = values.filter(Boolean);
// 結果
[1, 2, 3]
```

#### (3)、 `flat`

```js
const nested = [
  [1, 2],
  [3, 4]
];

nested.flat(); // [1, 2, 3, 4]
```

預設只展開一層：

```js
[1, [2, [3]]].flat();
// [1, 2, [3]]
```

指定深度：

```js
[1, [2, [3]]].flat(2);
// [1, 2, 3]
```

完全展開常見寫法：

```js
nested.flat(Infinity);
```

但非常深或迴圈引用的結構需要謹慎。

#### (4)、 `flatMap`

`flatMap` 近似相當於先 `map`，再展開一層：

```js
const sentences = [
  "hello world",
  "javascript language"
];

const words = sentences.flatMap(
  sentence => sentence.split(" ")
);
```

結果：

```js
[
  "hello",
  "world",
  "javascript",
  "language"
]
```

近似等價：

```js
sentences
  .map(sentence => sentence.split(" "))
  .flat();
```

### 6.5、Map

#### (1)、`Map` 的基本方法

```js
const map = new Map();
```

新增或更新：

```js
map.set("name", "Alice");
map.set("age", 20);
```

讀取：

```js
map.get("name"); // "Alice"
```

判斷鍵是否存在：

```js
map.has("name"); // true
```

刪除：

```js
map.delete("name");
```

清空：

```js
map.clear();
```

數量：

```js
map.size
```

### 6.6、迭代器

#### (1)、迭代器的 `next()`

迭代器是一個擁有 `next()` 方法的物件。

每次呼叫返回：

```js
{
  value: 某个值,
  done: 是否结束
}
```

例如：

```js
const iterator = ["a", "b"][Symbol.iterator]();

iterator.next();
// { value: "a", done: false }

iterator.next();
// { value: "b", done: false }

iterator.next();
// { value: undefined, done: true }
```

`for...of` 內部會不斷呼叫 `next()`，直到：

```js
done === true
```

#### (2)、`Symbol.iterator`

一個物件如果擁有：

```js
object[Symbol.iterator]()
```

並且該方法返回迭代器，那麼它就是可迭代物件。

手動實現：

```js
const range = {
  start: 1,
  end: 3,

  [Symbol.iterator]() {
    let current = this.start;
    const end = this.end;

    return {
      next() {
        if (current <= end) {
          const value = current;
          current += 1;

          return {
            value,
            done: false
          };
        }

        return {
          value: undefined,
          done: true
        };
      }
    };
  }
};
```

現在可以：

```js
for (const number of range) {
  console.log(number);
}
```

#### (3)、可迭代物件和迭代器不是完全相同的概念

* 可迭代物件：能夠建立迭代器；
* 迭代器：透過 next() 逐個產生結果；

陣列是可迭代物件：

```js
const array = [1, 2, 3];
```

呼叫：

```js
array[Symbol.iterator]()
```

得到一個迭代器。

一個可迭代物件通常可以被多次遍歷，因為每次都會建立新迭代器：

```js
for (const value of array) {
}

for (const value of array) {
}
```

而某個具體迭代器通常是有狀態、一次性向前移動的：

```js
const iterator = array[Symbol.iterator]();

iterator.next();
iterator.next();
```

它記住了當前遍歷位置。



## 七、模組與專案組織方式

### 7.1、為什麼需要模組

如果所有程式碼都寫在一個檔案裡：

```js
const users = [];
const config = {};
const cache = new Map();

function createUser() {
}

function deleteUser() {
}

function startServer() {
}
```

隨著專案增大，會出現：

* 變數名衝突
* 內部實現暴露
* 檔案職責混亂
* 依賴關係難以理解
* 測試困難
* 修改影響範圍不清楚

模組把程式拆成若干檔案，並顯式定義：

```text
這個檔案向外提供什麼
這個檔案依賴什麼
```

例如：

```text
src/
├── config.js
├── user-service.js
├── user-repository.js
└── index.js
```

每個檔案擁有獨立的模組作用域。

```js
// config.js
const secret = "internal";

export const config = {
  port: 3000
};
```

其他模組只能訪問匯出的 `config`，不能直接訪問內部的 `secret`。

### 7.2、ES Modules

ES Modules，簡稱 ESM，是 JavaScript 標準模組系統，使用：import、export

Node.js 目前穩定支援 ESM，並同時保留 CommonJS 模組系統。[Node.js ESM 官方文件](https://nodejs.org/api/esm.html)

### 7.3、命名匯出

```js
// math.js
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}

export const PI = 3.14159;
```

匯入：

```js
// app.js
import {
  add,
  subtract,
  PI
} from "./math.js";

console.log(add(2, 3));
```

花括號中的名稱必須與匯出名稱對應：

```js
import {
  add
} from "./math.js";
```

以下名稱不存在時，模組載入通常會失敗：

```js
import {
  multiply
} from "./math.js";
```

#### (1)、先宣告，再統一匯出

下面兩種寫法作用相同。

直接匯出：

```js
export function add(a, b) {
  return a + b;
}

export const PI = 3.14159;
```

統一匯出：

```js
function add(a, b) {
  return a + b;
}

const PI = 3.14159;

export {
  add,
  PI
};
```

真實專案經常先定義實現，再在檔案底部集中匯出。

#### (2)、匯入時重新命名

```js
import {
  add as addNumbers
} from "./math.js";
```

這裡：

```text
原匯出名：add
當前檔案變數名：addNumbers
```

使用：

```js
addNumbers(2, 3);
```

常用於解決命名衝突：

```js
import {
  create as createUser
} from "./user.js";

import {
  create as createOrder
} from "./order.js";
```

#### (3)、匯出時重新命名

```js
function internalAdd(a, b) {
  return a + b;
}

export {
  internalAdd as add
};
```

其他檔案看到的是：

```js
import {
  add
} from "./math.js";
```

不會看到 `internalAdd` 這個名稱。

### 7.4、預設匯出

#### (1)、`export default`

一個模組最多有一個預設匯出：

```js
// logger.js
export default function createLogger() {
  return {
    log(message) {
      console.log(message);
    }
  };
}
```

匯入預設匯出時不使用花括號：

```js
import createLogger from "./logger.js";
```

預設匯入名稱由匯入方決定：

```js
import makeLogger from "./logger.js";
```

`makeLogger` 和 `createLogger` 都可以，因為預設匯出並不要求匯入方使用固定本地名稱。

#### (2)、預設匯出與命名匯出可以同時存在

```js
// logger.js
export const LOG_LEVEL = "info";

export function formatMessage(message) {
  return `[LOG] ${message}`;
}

export default function createLogger() {
}
```

匯入：

```js
import createLogger, {
  LOG_LEVEL,
  formatMessage
} from "./logger.js";
```

其中：

```text
createLogger               → 預設匯入
LOG_LEVEL、formatMessage   → 命名匯入
```

#### (3)、花括號的意義

```js
// 表示匯入預設匯出
import logger from "./logger.js";

// 表示匯入一個名字必須叫 logger 的命名匯出
import {
  logger
} from "./logger.js";
```

兩者完全不同。

假設：

```js
export default function logger() {
}
```

只能這樣匯入：

```js
import logger from "./logger.js";
```

### 7.5、名稱空間匯入

`import * as`

```js
import * as math from "./math.js";
```

假設 `math.js` 匯出：

```js
export function add() {
}

export function subtract() {
}

export const PI = 3.14159;
```

那麼可以：

```js
math.add(2, 3);
math.subtract(5, 2);
console.log(math.PI);
```

`math` 是模組名稱空間物件，包含該模組的匯出。

這種寫法在工具模組中很常見：

```js
import * as path from "node:path";
```

不過名稱空間物件不是普通的、任意可修改配置物件。匯入方不能把模組匯出重新賦值。

### 7.6、重新匯出

#### (1)、從另一個模組直接匯出

```js
// index.js
export {
  createUser,
  deleteUser
} from "./user-service.js";
```

這同時完成了：從 user-service.js 獲取匯出，再從 index.js 對外匯出。

如果當前模組自己不需要使用 `createUser`，就不必先匯入再匯出。

#### (2)、`export *`

```js
export * from "./user-service.js";
export * from "./order-service.js";
```

它會重新匯出目標模組的命名匯出。但是預設匯出通常不會被 `export *` 自動重新匯出。

預設匯出需要顯式處理：

```js
export {
  default as createLogger
} from "./logger.js";
```

#### (3)、Barrel 檔案

下面這種聚合匯出的檔案經常叫 barrel：

```js
// services/index.js
export {
  UserService
} from "./user-service.js";

export {
  OrderService
} from "./order-service.js";

export {
  PaymentService
} from "./payment-service.js";
```

其他檔案可以：

```js
import {
  UserService,
  OrderService
} from "./services/index.js";
```

或者根據解析配置：

```js
import {
  UserService,
  OrderService
} from "./services";
```

### 7.7、靜態匯入與動態匯入

#### (1)、靜態 `import`

```js
import {
  createClient
} from "./client.js";
```

靜態匯入具有固定語法結構，它不能直接寫在普通條件語句中：

```js
if (condition) {
  import {
    createClient
  } from "./client.js";
}
```

這不是合法的靜態匯入寫法，靜態匯入通常必須位於模組頂層。

#### (2)、動態 `import()`

動態匯入是一個表示式，它返回 Promise。

```js
const module = await import("./client.js");
```

匯入命名匯出：

```js
const module = await import("./math.js");

module.add(2, 3);
```

也可以解構：

```js
const {
  add
} = await import("./math.js");
```

匯入預設匯出：

```js
const {
  default: createLogger
} = await import("./logger.js");
```

#### (3)、條件載入

```js
if (config.enableAnalytics) {
  const {
    initializeAnalytics
  } = await import("./analytics.js");

  initializeAnalytics();
}
```

只有條件成立時才載入。例如：

```js
async function loadDatabase(driver) {
  if (driver === "postgres") {
    return import("./postgres-driver.js");
  }

  if (driver === "mysql") {
    return import("./mysql-driver.js");
  }

  throw new Error(`Unsupported driver: ${driver}`);
}
```

### 7.8、package.json

`package.json` 可以理解為一個前端專案的“身份證 + 依賴清單 + 命令入口 + 工具配置”。

npm、pnpm、Yarn、Node.js、Vite、Webpack，以及各種工程化工具，都會讀取它。它必須是嚴格的 JSON：不能寫註釋、不能有尾逗號、屬性名必須使用雙引號。npm 官方完整欄位說明可參考 [package.json 文件](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/)。

下面按照實際前端專案中的重要程度講解。

#### (1)、一個典型的前端專案配置

以 Vue 3 + Vite + TypeScript 專案為例：

```json
{
  "name": "my-vue-app",
  "version": "1.0.0",
  "private": true,
  "description": "一个基于 Vue 3 和 Vite 的后台管理系统",
  "type": "module",

  "scripts": {
    "dev": "vite",
    "build": "vue-tsc -b && vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "test": "vitest run",
    "test:watch": "vitest",
    "type-check": "vue-tsc --noEmit"
  },

  "dependencies": {
    "axios": "^1.7.0",
    "pinia": "^2.2.0",
    "vue": "^3.5.0",
    "vue-router": "^4.4.0"
  },

  "devDependencies": {
    "@vitejs/plugin-vue": "^5.1.0",
    "@vue/tsconfig": "^0.5.0",
    "eslint": "^9.0.0",
    "typescript": "^5.6.0",
    "vite": "^5.4.0",
    "vitest": "^2.0.0",
    "vue-tsc": "^2.1.0"
  },

  "engines": {
    "node": ">=20.0.0",
    "npm": ">=10.0.0"
  },

  "packageManager": "pnpm@9.12.0"
}
```

實際專案不一定包含所有欄位，但其中最常見的是：

* `name`
* `version`
* `private`
* `scripts`
* `dependencies`
* `devDependencies`



#### (2)、專案基本資訊

##### 1. `name`

專案或 npm 包的名稱：

```json
{
  "name": "my-admin-system"
}
```

如果準備釋出到 npm，它必須遵守 npm 包命名規則，一般使用小寫字母和連字元。

帶作用域的包名：

```json
{
  "name": "@my-company/ui-components"
}
```

這裡的 `@my-company` 是組織或作用域名稱。

對於只在公司內部開發、不釋出到 npm 的普通前端應用，名稱主要用於：

* 標識專案；
* 顯示在 npm/pnpm 命令輸出中；
* Monorepo 工作區引用；
* 生成構建資訊。

##### 2. `version`

專案版本：

```json
{
  "version": "1.2.3"
}
```

通常遵循語義化版本，即：

```text
主版本.次版本.修訂版本
 MAJOR.MINOR.PATCH
```

例如：

* `1.0.0`：第一個正式版本；
* `1.0.1`：修復 Bug；
* `1.1.0`：增加向後相容的新功能；
* `2.0.0`：出現不相容的重大變化；
* `2.0.0-beta.1`：測試版本。

如果需要釋出 npm 包，`name` 和 `version` 是最重要的標識欄位，版本必須滿足語義化版本格式。[npm 官方說明](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/)

##### 3. `private`

```json
{
  "private": true
}
```

表示這是一個私有專案，不允許執行 `npm publish` 釋出到 npm 公共倉庫。

普通業務前端專案建議新增：

```json
"private": true
```

它可以避免開發人員誤釋出公司專案。

注意：這裡的“私有”不代表程式碼會自動加密，也不代表別人無法訪問程式碼；它只是阻止 npm 釋出。

##### 4. `description`

```json
{
  "description": "企业内部订单管理系统前端"
}
```

用於描述專案功能。釋出 npm 包時，它也會顯示在 npm 搜尋結果中。

##### 5. `keywords`

```json
{
  "keywords": [
    "vue",
    "admin",
    "dashboard",
    "typescript"
  ]
}
```

主要用於 npm 包搜尋。普通業務專案可以不寫。

##### 6. `author`

```json
{
  "author": "Zhang San <zhangsan@example.com>"
}
```

也可以使用物件：

```json
{
  "author": {
    "name": "Zhang San",
    "email": "zhangsan@example.com",
    "url": "https://example.com"
  }
}
```

團隊專案有時會使用：

```json
{
  "contributors": [
    {
      "name": "Zhang San"
    },
    {
      "name": "Li Si"
    }
  ]
}
```

##### 7. `license`

```json
{
  "license": "MIT"
}
```

常見許可證：

* `MIT`
* `Apache-2.0`
* `GPL-3.0`
* `ISC`
* `UNLICENSED`

公司內部、不允許公開使用的專案可以寫：

```json
{
  "license": "UNLICENSED",
  "private": true
}
```



#### (3)、`scripts`：專案命令入口

`scripts` 用來定義專案可執行命令：

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "lint": "eslint ."
  }
}
```

執行方式：

```bash
npm run dev
npm run build
npm run lint
```

或者使用 pnpm：

```bash
pnpm dev
pnpm build
pnpm lint
```

npm 會自動把 `node_modules/.bin` 新增到指令碼的命令搜尋路徑，所以可以直接寫：

```json
"dev": "vite"
```

不需要寫：

```json
"dev": "./node_modules/.bin/vite"
```

npm 支援任意自定義指令碼，以及 `pre`、`post` 前後置指令碼。[npm Scripts 文件](https://docs.npmjs.com/cli/using-npm/scripts/)



常見前端指令碼

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "build:test": "vite build --mode test",
    "build:prod": "vite build --mode production",
    "preview": "vite preview",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test"
  }
}
```

這裡的冒號沒有特殊語法意義，只是一種命名習慣：

```text
build:test
build:prod
lint:fix
test:e2e
```

讓相關命令看起來更有層次。



生命週期指令碼

例如：

```json
{
  "scripts": {
    "prebuild": "npm run lint",
    "build": "vite build",
    "postbuild": "node scripts/report-build.js"
  }
}
```

執行：

```bash
npm run build
```

npm 會按照下面的順序執行：

```text
prebuild → build → postbuild
```

需要謹慎使用 `preinstall`、`install` 和 `postinstall`，因為它們會在安裝依賴時自動執行，可能造成：

* 安裝速度變慢；
* 跨平臺相容問題；
* CI 構建失敗；
* 潛在供應鏈安全風險。



#### (4)、`dependencies`：生產依賴

```json
{
  "dependencies": {
    "axios": "^1.7.0",
    "vue": "^3.5.0",
    "vue-router": "^4.4.0"
  }
}
```

這裡通常放應用執行階段需要的包，例如：

* Vue、React；
* Vue Router、React Router；
* Axios；
* Pinia、Redux；
* 日期處理庫；
* UI 元件庫；
* 表單驗證庫。

安裝生產依賴：

```bash
npm install axios
```

或者：

```bash
pnpm add axios
```

包管理器會自動更新 `package.json`，通常不建議手工新增版本號。

判斷標準是：

> 刪除這個依賴後，最終執行的應用是否會缺失必要功能？

如果會，就通常應該放到 `dependencies`。



#### (5)、`devDependencies`：開發依賴

```json
{
  "devDependencies": {
    "eslint": "^9.0.0",
    "prettier": "^3.3.0",
    "typescript": "^5.6.0",
    "vite": "^5.4.0",
    "vitest": "^2.0.0"
  }
}
```

這裡放只在開發、編譯、測試階段使用的工具，例如：

* Vite、Webpack；
* TypeScript；
* ESLint；
* Prettier；
* Vitest、Jest；
* Playwright；
* Babel；
* 各種編譯外掛；
* 型別宣告包。

安裝開發依賴：

```bash
npm install eslint --save-dev
```

簡寫：

```bash
npm install eslint -D
```

pnpm 對應：

```bash
pnpm add eslint -D
```

npm 官方的基本定義是：

* `dependencies`：應用生產執行需要；
* `devDependencies`：本地開發和測試需要。

詳見 [npm 依賴分類說明](https://docs.npmjs.com/specifying-dependencies-and-devdependencies-in-a-package-json-file/)。



一個容易誤解的地方

對於 Vite 構建的純前端應用，`vue`、`axios` 最終也會被打包進靜態資源，並不會原樣保留在伺服器的 `node_modules` 中。

但它們仍然屬於應用的功能依賴，通常放在：

```json
"dependencies"
```

而 Vite、ESLint、TypeScript 屬於構建工具，放在：

```json
"devDependencies"
```



#### (6)、依賴版本符號

例如：

```json
{
  "dependencies": {
    "vue": "^3.5.0",
    "axios": "~1.7.2",
    "dayjs": "1.11.13"
  }
}
```



精確版本

```json
"dayjs": "1.11.13"
```

只接受這個版本。

優點是結果更可控；缺點是不會自動獲得修訂版本更新。



`^`：相容的次版本和修訂版本

```json
"vue": "^3.5.0"
```

對於正常的 `1.0.0` 以上版本，大致相當於：

```text
>=3.5.0 且 <4.0.0
```

可以升級：

```text
3.5.1
3.6.0
3.9.9
```

不會升級到：

```text
4.0.0
```



`~`：通常只允许修订版本变化

```json
"axios": "~1.7.2"
```

大致相當於：

```text
>=1.7.2 且 <1.8.0
```

可以升級：

```text
1.7.3
1.7.9
```

不能升級到：

```text
1.8.0
```



`*` 或 `latest`

```json
"some-package": "*"
```

或者安裝時使用：

```bash
npm install some-package@latest
```

不建議在正式專案中把依賴寫成 `*`，因為每次安裝可能得到差異很大的版本。



版本範圍不等於實際安裝版本

假設 `package.json` 中寫的是：

```json
"axios": "^1.7.0"
```

它表示“允許安裝的版本範圍”，而 `package-lock.json`、`pnpm-lock.yaml` 或 `yarn.lock` 記錄實際解析出來的版本。

因此：

* `package.json`：宣告專案需要什麼；
* 鎖檔案：記錄這一次具體安裝了什麼。

團隊專案通常應該提交鎖檔案。



#### (7)、`type`：模組型別

```json
{
  "type": "module"
}
```

它主要影響 Node.js 如何解釋 `.js` 檔案。



ES Module

```json
{
  "type": "module"
}
```

此時 `.js` 檔案預設使用 ESM：

```js
import fs from "node:fs";

export function readFile() {}
```



CommonJS

```json
{
  "type": "commonjs"
}
```

或者不寫 `type`，Node.js 環境中通常會把 `.js` 按 CommonJS 處理：

```js
const fs = require("node:fs");

module.exports = {};
```

現代 Vite 前端專案通常使用：

```json
"type": "module"
```

注意，它不僅影響業務程式碼，還可能影響：

* `vite.config.js`
* `eslint.config.js`
* Node.js 構建指令碼
* 測試配置檔案

另外：

* `.mjs` 明確表示 ES Module；
* `.cjs` 明確表示 CommonJS。



#### (8)、Node 和包管理器版本

`engines`

```json
{
  "engines": {
    "node": ">=20.0.0",
    "npm": ">=10.0.0"
  }
}
```

表示專案期望使用的執行環境版本。

還可以限制版本區間：

```json
{
  "engines": {
    "node": ">=20.19.0 <23"
  }
}
```

需要注意：`engines` 在很多情況下主要起提示和約束宣告作用，不一定會預設阻止安裝；具體是否嚴格失敗還受包管理器配置影響。



`packageManager`

```json
{
  "packageManager": "pnpm@9.12.0"
}
```

用於說明專案應該使用什麼包管理器及其版本。

常見寫法：

```json
"packageManager": "npm@10.8.2"
```

```json
"packageManager": "pnpm@9.12.0"
```

```json
"packageManager": "yarn@4.5.0"
```

它可以減少團隊成員混用 npm、pnpm 和 Yarn 導致的鎖檔案衝突。

建議一個專案只保留一種鎖檔案：

```text
npm   → package-lock.json
pnpm  → pnpm-lock.yaml
Yarn  → yarn.lock
```

不要同時提交三種鎖檔案。



## 八、非同步 JavaScript

### 8.1、Promise

#### (1)、Promise 表示未來結果

```js
const promise = fetchUser();
```

`promise` 不是終端使用者資料，而是一個代表未來結果的物件。

Promise 有三種狀態：

```text
pending    等待中
fulfilled  已成功
rejected   已失敗
```

狀態轉換隻能發生一次：

```text
pending → fulfilled
pending → rejected
```

完成後不能再次改變。

#### (2)、Promise executor 同步執行

`new Promise` 接收的函式通常稱為 executor。

```js
console.log("A");

const promise = new Promise(resolve => {
  console.log("B");
  resolve("done");
});

console.log("C");
```

輸出：

```text
A
B
C
```

executor 在建立 Promise 時立即同步執行。

非同步的是之後註冊的 Promise 處理函式：

```js
promise.then(value => {
  console.log(value);
});
```

### 8.2、`async` 函式

#### (1)、`async` 函式總是返回 Promise

```js
async function getValue() {
  return 42;
}

// result 是 Promise，不是數字 42
const result = getValue();


```

近似相當於：

```js
function getValue() {
  return Promise.resolve(42);
}
```

讀取結果：

```js
getValue().then(value => {
  console.log(value);
});
```

或者：

```js
const value = await getValue();
```

### 8.3、`await`

#### (1)、`await` 等待 Promise 的結果

```js
async function loadUser() {
  const user = await fetchUser();
  return user;
}
```

可以近似理解為：

```js
function loadUser() {
  return fetchUser().then(user => {
    return user;
  });
}
```

但 `async/await` 通常更接近同步程式碼的閱讀方式。
